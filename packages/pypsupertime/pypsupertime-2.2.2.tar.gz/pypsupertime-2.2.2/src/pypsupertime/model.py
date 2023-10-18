from abc import ABC, ABCMeta, abstractmethod
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
from scipy import sparse
import torch
from torch.optim import lr_scheduler
import anndata as ad
import numpy as np
import pandas as pd
from numpy.random import default_rng
import warnings

from .preprocessing import restructure_X_to_bin, restructure_y_to_bin, transform_labels


# Maximum positive number before numpy 64bit float overflows in np.exp()
MAX_EXP = 709


class BinaryLogisticRegression(torch.nn.Module):

    def __init__(self, input_dim):
        super(BinaryLogisticRegression, self).__init__()
        self.linear = torch.nn.Linear(input_dim, 1)
        #self.apply(self._init_weights_zero)

    def _init_weights_zero(self, module):
        if isinstance(module, torch.nn.Linear):
            module.weight.data.zero_()
            if module.bias is not None:
                module.bias.data.zero_()

    def forward(self, x):
        outputs = torch.sigmoid(self.linear(x))
        return outputs


class OptimalLR():
    """ 
    Implements the Learning Rate heuristic used in the scikit-learn implementation of SGDClassifier
    """

    def __init__(self, optimizer, alpha, n_samples=1, t0=0):

        self.optimizer = optimizer
        self.alpha = alpha
        self.t = t0

        # Updates are performed at every time step. In the sklearn
        # implementation there are a total of n_samples * n_iter time steps.
        # Since we update not per sample, but per batch (or all samples at once),
        # some samples have to be skipped.
        self.n_samples = n_samples

        self.t_init = self._init_optimal(self.alpha)
        self.lr_history = []

        self.step()

    def _init_optimal(self, alpha):
        typw = np.sqrt(1.0 / np.sqrt(alpha))
        opt_init = 1.0 / (typw * alpha)
        return opt_init

    def get_last_lr(self):
        return [self.lr_history[-1]]

    def step(self):
        lr = 1 / (self.alpha * (self.t_init + self.t))

        self.lr_history.append(lr)
        
        for param_group in self.optimizer.param_groups:
            param_group['lr'] = lr
        
        # increment by the number of samples that were seen
        self.t += self.n_samples


class AdaptiveLR():

    def __init__(self, optimizer, eta0, reduction_factor=0.2, min_lr=0.0001, t0=0):
        
        self.t = t0
        self.optimizer = optimizer
        self.eta0 = eta0
        self.reduction_factor = reduction_factor
        self.min_lr = min_lr
        self.lr_history = []
        self.step()

    def get_last_lr(self):
        return [self.lr_history[-1]]

    def step(self):
        self.t += 1
        lr = max(self.min_lr, self.eta0 * self.reduction_factor ** self.t)
        self.lr_history.append(lr)

        for param_group in self.optimizer.param_groups:
            param_group['lr'] = lr


class ConstantLR():
    def __init__(self, optimizer, eta0):
        self.eta = eta0

        for param_group in optimizer.param_groups:
            param_group['lr'] = self.eta
    
    def get_last_lr(self):
        return [self.eta]

    def step(self):
        pass



class PsupertimeBaseModel(ClassifierMixin, BaseEstimator, ABC):
    """
    Abstract Base class to build scikit-learn compatible models for PyPsupertime derived from `sklearn.base.BaseEstimator` and 
    `sklearn.base.ClassifierMixin`.

    Provides methods for restructuring ordinal data into a binary representation and 
    for fitting a nested binary logistic classifier.
    
    Provides predict methods, that uses the fitted binary classifier to estimate the probabilities and labels of
    the ordinal multiclass problem.

    :ivar method: Statistical model used for ordinal logistic regression: One of `"proportional"`, `"forward"` 
     and `"backward"`, corresponding to cumulative proportional odds, forward continuation ratio and
     backward continuation ratio.
    :type method: str 
    :ivar regularization: parmeter controlling the sparsity of the model. Wrapper for the respective parameter
     of the nested `binary_estimator_`. Not necessary
    :type regularization: float
    :ivar k_: number of thresholds to be learned, equal to one less than the number of unique ordinal labels 
    :type k_: int
    :ivar random_state: Initialize the RNG for reproducibility
    :type random_state: int
    :ivar track_scores: Set to True to track training loss and degrees of freedom. In models that support early stopping, validation loss is also recorded
    :type track_scores: boolean
    """
    coef_: np.array
    intercept_: np.array
    k_: int = 0
    classes_: np.array
    is_fitted_: bool = False

    def __init__(self,
                 method="proportional",
                 regularization=0.1,
                 penalty="l1",
                 l1_ratio=1,
                 n_batches=1,
                 max_iter=100,
                 random_state=1234, 
                 learning_rate="optimal",
                 eta0=0.1,
                 shuffle=True, 
                 early_stopping=False,
                 early_stopping_batches=False,
                 tol=1e-3,
                 n_iter_no_change=5, 
                 validation_fraction=0.1,
                 track_scores=False,
                 verbosity=0):

        if not isinstance(method, str) or method not in ["proportional", "forward", "backward"]:
            raise ValueError('Parameter method must be one of "proportional", "forward", "backward". Received %s ' % method)

        if not isinstance(penalty, str) or penalty not in ["l1", "l2", "elasticnet"]:
            raise ValueError("Parameter penalty must be one of 'l1', 'l2', 'elasticnet'. received: %s" % penalty)
        
        if not isinstance(learning_rate, str) or learning_rate not in ["optimal", "constant", "adaptive", "exponential"]:
            raise ValueError('Parameter learning_rate must be one of "optimal", "constant", "adaptive". Received %s' % learning_rate)

        if penalty == "l1":
            if l1_ratio != 1:
                warnings.warn("Setting l1_ratio to 1, when using penalty='l1'")
            self.l1_ratio = 1
        elif penalty == "l2":
            self.l1_ratio = 0
        else:
            if not (0 <= l1_ratio and l1_ratio <= 1):
                raise ValueError("Parameter l1_ratio must be in the interval (0, 1). Received: %s" % l1_ratio)
            self.l1_ratio = l1_ratio

        # hyperparameters 
        self.method = method
        self.penalty = penalty
        self.regularization = regularization
        self.learning_rate = learning_rate
        self.eta0 = eta0
        self.max_iter = max_iter
        self.random_state = random_state  # TODO: currently not used in torch optimizer!
        self.regularization = regularization
        self.shuffle = shuffle
        self.verbosity = verbosity
        self.validation_fraction = validation_fraction
        self.early_stopping = early_stopping
        self.n_iter_no_change = n_iter_no_change
        self.tol = tol
        self.n_batches = n_batches
        self.early_stopping_batches = early_stopping_batches
        self.track_scores = track_scores

        self.rng_ = None
        self.model = None

        # training scores:
        self.train_losses_ = []
        self.train_dof_ = []
        self.test_losses_ = []

        # learned model parameters
        self.k_ = None
        self.is_fitted_ = False
        self.coef_ = None
        self.intercept_ = None

        # fitting parameters for early stopping
        self.train_epoch_ = None
        self.test_best_loss_ = None
        self.test_not_improved_for_ = None

    def _before_fit(self, X, y, sample_weights=None):

        self.rng_ = np.random.default_rng(self.random_state)

        self.is_fitted_ = False

        X, y = check_X_y(X, transform_labels(y), accept_sparse=True)
        self.classes_ = np.unique(y)
        self.k_ = len(self.classes_) - 1

        try:
            if sample_weights is not None:
                if not len(sample_weights) == len(y):
                    raise ValueError("The parameter sample_weight has incompatible weight with the target vector. Shape: %s Expected: %s" % (len(sample_weights), len(y)))

        except TypeError as e:
            print(e)
            raise ValueError("The parameter sample_weights has no length. Received: %s" % sample_weights)
        
        # Test split
        X_test, y_test = None, None
        if self.early_stopping:
            X, X_test, y, y_test = train_test_split(X, y, test_size=self.validation_fraction, stratify=y, random_state=self.rng_.integers(9999))

        return X, y, X_test, y_test

    def _init_training_loop(self):
        self.train_losses_ = []
        self.train_dof_ = []
        self.test_losses_ = []
        self.train_epoch_ = 1
        self.test_best_loss_ = np.inf
        self.test_not_improved_for_ = 0

    def _check_early_stopping(self, test_loss=None, greater_is_better=False):

        if greater_is_better:
            test_loss = -1 * test_loss

        if test_loss + self.tol < self.test_best_loss_:
            self.test_best_loss_ = test_loss
            self.test_not_improved_for_ = 0
        else:
            self.test_not_improved_for_ += 1
            if self.test_not_improved_for_ >= self.n_iter_no_change:
                if self.verbosity >= 2:
                    print("Stopped early at epoch ", self.train_epoch_, " Current score:", self.test_best_loss_)
                return True

    def _training_step(self, train_loss=None, test_loss=None, dof=None, do_early_stopping_check=True, **kwargs):
        
        if (self.train_epoch_ is None 
            or self.test_best_loss_ is None 
            or self.test_not_improved_for_ is None):
            self._init_training_loop()

        msg = "Epoch %s" % self.train_epoch_
        if self.track_scores:
            if train_loss is not None:
                msg += " training loss=%s" % train_loss
                self.train_losses_.append(train_loss)
            if test_loss is not None: 
                msg += " validation loss=%s" % test_loss
                self.test_losses_.append(test_loss)
            if dof is not None:
                msg += " dof=%s" % dof
                self.train_dof_.append(dof)

        # print status every 10 epochs
        if self.verbosity >= 3 and self.train_epoch_ % 10 == 0:
            print(msg)
        
        # print status every epoch
        if self.verbosity >= 4:
            print(msg)

        stop_condition_reached = False
        if self.train_epoch_ > self.max_iter:
            stop_condition_reached = True

        # early stopping based on loss calculated from dedicated validation split
        elif do_early_stopping_check and test_loss is not None:
            stop_condition_reached = self._check_early_stopping(test_loss, **kwargs)

        # early stopping based on training loss
        elif do_early_stopping_check and train_loss is not None:
            stop_condition_reached = self._check_early_stopping(train_loss, **kwargs)

        self.train_epoch_ += (not stop_condition_reached) *1
        self.is_fitted_ = stop_condition_reached
        return stop_condition_reached

    @abstractmethod
    def fit(self, data, targets, sample_weight=None):
        """Template fit function for derived models.

        :param data: 2d data
        :type data: numpy or numpy.sparse matrix
        :param targets: Array-like object with ordinal labels
        :type targets: Iterable
        :param sample_weight: label weights to be used for training and scoring, defaults to None
        :type sample_weight: Iterable, optional
        :return: fitted estimator
        :rtype: PsupertimeBaseModel
        """
        pass

    def predict_proba(self, X):
        warnings.filterwarnings("once")

        transform = X @ self.coef_        
        logit = np.zeros(X.shape[0] * (self.k_)).reshape(X.shape[0], self.k_)
        
        # calculate logit
        for i in range(self.k_):
            # Clip exponents that are larger than MAX_EXP before np.exp for numerical stability
            # this will cause warnings and nans otherwise!
            temp = self.intercept_[i] + transform
            temp = np.clip(temp, np.min(temp), MAX_EXP)
            exp = np.exp(temp)
            logit[:, i] = exp / (1 + exp)

        prob = np.zeros(X.shape[0] * (self.k_ + 1)).reshape(X.shape[0], self.k_ + 1)
        # calculate differences
        for i in range(self.k_ + 1):
            if i == 0:
                prob[:, i] = 1 - logit[:, i]
            elif i < self.k_:
                prob[:, i] = logit[:, i-1] - logit[:, i]
            elif i == self.k_:
                prob[:, i] = logit[:, i-1]
        
        warnings.filterwarnings("always")
        return prob
    
    def predict(self, X):
        return np.apply_along_axis(np.argmax, 1, self.predict_proba(X))

    def predict_psuper(self, anndata: ad.AnnData, inplace=True):
        
        transform = anndata.X @ self.coef_
        predicted_labels = self.predict(anndata.X)      

        if inplace:
            anndata.obs["psupertime"] = transform
            anndata.obs["predicted_label"] = predicted_labels
        
        else:
            obs_copy = anndata.obs.copy()
            obs_copy["psupertime"] = transform
            obs_copy["predicted_label"] = predicted_labels
            return obs_copy
    
    def gene_weights(self, anndata: ad.AnnData, inplace=True):
        if inplace:
            anndata.var["psupertime_weight"] = self.coef_
        else:
            return pd.DataFrame({"psupertime_weight": self.coef_},
                                index=anndata.var.index.copy())


class SGDModel(PsupertimeBaseModel):
    """
    SGDModel is a classifier derived from `PsupertimBaseModel` that wraps an `SGDClassifier`
    as logistic binary estimator.
    
    It overwrites the superclass `fit()` methods. The latter is wrapping
    the `SGDClassifier.partial_fit()` function to fit the model in batches for a reduced memory footprint.
    
    """
    def __init__(self,
                 method="proportional",
                 regularization=0.01, 
                 n_batches=1,
                 max_iter=100, 
                 random_state=1234, 
                 learning_rate="optimal",
                 eta0=0,
                 power_t=0.5,
                 average=False,
                 early_stopping=False,
                 early_stopping_batches=False,
                 n_iter_no_change=5, 
                 tol=1e-3,
                 penalty='elasticnet', 
                 l1_ratio=1, 
                 shuffle=True, 
                 verbosity=0, 
                 epsilon=0.1, 
                 validation_fraction=0.1,
                 class_weight=None,
                 track_scores=False):

        super(SGDModel, self).__init__(method=method, penalty=penalty, l1_ratio=l1_ratio, n_batches=n_batches, max_iter=max_iter, random_state=random_state,
                                              regularization=regularization, learning_rate=learning_rate, eta0 = eta0, verbosity=verbosity, shuffle=shuffle,
                                              early_stopping=early_stopping, early_stopping_batches=early_stopping_batches, 
                                              n_iter_no_change=n_iter_no_change, tol=tol, validation_fraction=validation_fraction, track_scores=track_scores)
        self.power_t = power_t
        self.epsilon = epsilon
        self.average = average
        self.class_weight = class_weight
        self.model = None

    def _init_binary_model(self):
        return SGDClassifier(eta0 = self.eta0,
                            learning_rate = self.learning_rate,
                            max_iter = self.max_iter,
                            random_state = self.random_state,
                            alpha = self.regularization,
                            loss = "log_loss",
                            penalty = self.penalty,
                            l1_ratio = self.l1_ratio,
                            fit_intercept = True,
                            shuffle = self.shuffle,
                            verbose = self.verbosity >= 3,
                            epsilon = self.epsilon,
                            n_jobs = 1,
                            power_t = self.power_t,
                            validation_fraction = self.validation_fraction,
                            class_weight = self.class_weight,
                            average = self.average,
                            early_stopping = False,  # has to be false to use partial_fit
                            n_iter_no_change = self.n_iter_no_change,
                            tol = self.tol)

    def _collect_parameters(self):

        self.coef_ = self.model.coef_.flatten()[:-self.k_]
        self.intercept_ = self.model.coef_.flatten()[-self.k_:] +  self.model.intercept_

    def fit(self, X, y, sample_weight=None):
        """Fit ordinal logistic model. 
        Multiclass data is converted to binarized representation and one weight per feature, 
        as well as a threshold for each class is fitted with a binary logistic classifier.

        Derived from a `sklearn.linear.SGDClassifier`, fitted in batches according to `self.n_batches` 
        for reduced memory usage.
        

        :param X: Data as 2d-matrix
        :type X: numpy.array or scipy.sparse
        :param y: ordinal labels
        :type y: Iterable
        :param sample_weight: Label weights for fitting and scoring, defaults to None. Can be used for example for class balancing.
        :type sample_weight: Iterable, optional
        :return: fitted classifier
        :rtype: SGDModel
        """
        X, y, X_test, y_test = self._before_fit(X, y)
        n = X.shape[0]

        if X_test is not None and y_test is not None:
            X_test = restructure_X_to_bin(X_test, self.k_)
            y_test = restructure_y_to_bin(y_test)

        # binarize only the labels already
        y_bin = restructure_y_to_bin(y)
        
        # diagonal matrix, to construct the binarized X per batch
        thresholds = np.identity(self.k_)
        if sparse.issparse(X):
            thresholds = sparse.csr_matrix(thresholds)

        self.model = self._init_binary_model()
        # create an inex array and shuffle
        sampled_indices = self.rng_.integers(len(y_bin), size=len(y_bin))

        self._init_training_loop()
        while True:

            start = 0
            for i in range(1, self.n_batches+1):
                end = (i * len(y_bin) // self.n_batches)
                batch_idx = sampled_indices[start:end]
                batch_idx_mod_n = batch_idx % n
                
                if sparse.issparse(X):
                    X_batch = sparse.hstack((X[batch_idx_mod_n], thresholds[batch_idx // n]))
                else:
                    X_batch = np.hstack((X[batch_idx_mod_n,:], thresholds[batch_idx // n]))
                
                y_batch = y_bin[batch_idx]
                start = end
                weights = np.array(sample_weight)[batch_idx_mod_n] if sample_weight is not None else None
                self.model.partial_fit(X_batch, y_batch, classes=np.unique(y_batch), sample_weight=weights)
            
            train_loss = metrics.log_loss(y_batch, self.model.predict_proba(X_batch))
            dof = np.count_nonzero(self.model.coef_.flatten())
            test_loss = None
            if self.early_stopping:
                test_loss = metrics.log_loss(y_test, self.model.predict_proba(X_test))

            training_finished =  self._training_step(train_loss, test_loss, dof)
            if training_finished:
                break

            if self.shuffle:
                sampled_indices = self.rng_.integers(len(y_bin), size=len(y_bin))

        self._collect_parameters()
        return self


class CumulativePenaltySGDModel(PsupertimeBaseModel):
    """
    BatchSGDModel is a classifier derived from `PsupertimBaseModel` that wraps an `SGDClassifier`
    as logistic binary estimator.
    
    It overwrites the superclass `_binary_estimator_factory() and `fit()` methods. The latter is wrapping
    the `SGDClassifier.partial_fit()` function to fit the model in batches for a reduced memory footprint.
    
    """
    def __init__(self,
                 method="proportional",
                 early_stopping_batches=False,
                 n_batches=1,
                 max_iter=100, 
                 random_state=1234, 
                 regularization=0.01,
                 n_iter_no_change=15,
                 min_iter=1,
                 early_stopping=False,
                 tol=1e-3,
                 learning_rate="optimal",
                 eta0=0,
                 gamma=0.9,
                 penalty='elasticnet', 
                 l1_ratio=1, 
                 shuffle=True, 
                 verbosity=0, 
                 validation_fraction=0.1,
                 track_scores=False):

        super(CumulativePenaltySGDModel, self).__init__(method=method, penalty=penalty, l1_ratio=l1_ratio, n_batches=n_batches, max_iter=max_iter, random_state=random_state,
                                        regularization=regularization, learning_rate=learning_rate, eta0=eta0, verbosity=verbosity, shuffle=shuffle,
                                        early_stopping=early_stopping, early_stopping_batches=early_stopping_batches, 
                                        n_iter_no_change=n_iter_no_change,tol=tol, validation_fraction=validation_fraction, track_scores=track_scores)

        if learning_rate != "optimal":
            raise ValueError("Only learning_rate='optimal' implemented for CumulativePenaltySGDModel")

        self.min_iter = min_iter
        self.gamma = gamma

    def _collect_parameters(self):

        coef, intercept = tuple(self.model.parameters())
        coef = coef.detach().numpy().flatten()
        intercept = intercept.detach().numpy().flatten()
        self.coef_ = coef[:-self.k_]
        self.intercept_ = coef[-self.k_:] +  intercept

    def fit(self, X, y, sample_weights=None):
        """Fit ordinal logistic model. 
        Multiclass data is converted to binarized representation and one weight per feature, 
        as well as a threshold for each class is fitted with a binary logistic classifier.

        Extends the BianryLogisticRegression calss build with Pytorch, fitted in batches according to `self.n_batches` 
        for reduced memory usage.
        

        :param X: Data as 2d-matrix
        :type X: numpy.array or scipy.sparse
        :param y: ordinal labels
        :type y: Iterable
        :param sample_weight: Label weights for fitting and scoring, defaults to None. Can be used for example for class balancing.
        :type sample_weight: Iterable, optional
        :return: fitted classifier
        :rtype: BatchSGDModel
        """
        rng = np.random.default_rng(self.random_state)
        X, y, X_test, y_test = self._before_fit(X, y, sample_weights)
        n = X.shape[0]
        n_features = X.shape[1] + self.k_

        if self.early_stopping:
            X_test = torch.Tensor(restructure_X_to_bin(X_test, self.k_))
            y_test = torch.Tensor(restructure_y_to_bin(y_test))

        # binarize only the labels already
        y_bin = torch.Tensor(restructure_y_to_bin(y))
        
        # diagonal matrix, to construct the binarized X per batch
        thresholds = np.identity(self.k_)
        if sparse.issparse(X):
            thresholds = sparse.csr_matrix(thresholds)

        # Logistic regression model, defined as a perceptron
        torch.manual_seed(self.random_state)
        self.model = BinaryLogisticRegression(input_dim=n_features)
        
        # Loss function: Binary Cross Entropy = Log loss
        criterion = torch.nn.BCELoss(reduction="none")

        # Adaptive momentum SGD optimizer
        optimizer = torch.optim.SGD(self.model.parameters(), lr=self.eta0)

        # learning rate
        lr_schedule = OptimalLR(optimizer, self.regularization, n_samples=1)

        # Sample weight to balance classes of y
        if sample_weights is None:
            sample_weights = torch.Tensor(np.ones_like(y))
        else:
            sample_weights = torch.Tensor(sample_weights)

        # Mask for applying penalty: Only apply to gene features, don't apply to thresholds
        penalty_mask = torch.Tensor(np.concatenate((np.ones(X.shape[1]), np.zeros(self.k_))))

        # cumulative penalty tracking
        u = torch.tensor(0.)
        q = torch.zeros(n_features)
        z = torch.zeros(n_features)

        # create an index array and shuffle
        sampled_indices = rng.integers(len(y_bin), size=len(y_bin))

        self._init_training_loop()
        while True:

            start = 0
            for i in range(1, self.n_batches+1):
                end = (i * len(y_bin) // self.n_batches)
                batch_idx = sampled_indices[start:end]
                batch_idx_mod_n = batch_idx % n
                
                if sparse.issparse(X):
                    # TODO: Fix sparsity! Converting to dense format is a hack to get this to work
                    X_batch = torch.Tensor(sparse.hstack((X[batch_idx_mod_n], thresholds[batch_idx // n])).todense())
                else:
                    X_batch = torch.Tensor(np.hstack((X[batch_idx_mod_n,:], thresholds[batch_idx // n])))
                
                y_batch = y_bin[batch_idx]
                start = end
                sample_weights_batch = sample_weights[batch_idx_mod_n]

                # Set stored gradients to zero
                optimizer.zero_grad()
                
                # Forward pass
                outputs = self.model(X_batch)

                # calculate loss scaled by sample weights
                loss = (criterion(torch.squeeze(outputs), y_batch) * sample_weights_batch).mean()

                # backward pass and weight update
                loss.backward()
                optimizer.step()

                with torch.no_grad():
                    # Apply Cumulative penalty
                    weights, bias = tuple(self.model.parameters())

                    z = weights.data.squeeze().clone()
                    lr = torch.tensor(lr_schedule.get_last_lr()[0])
                    u = u + lr * self.regularization * self.l1_ratio + (1 - self.l1_ratio) * lr * self.regularization * z.abs()

                    idx_wpos = (weights > 0).squeeze() * penalty_mask > 0
                    idx_wneg = (weights < 0).squeeze() * penalty_mask > 0

                    weights.data[0, idx_wpos] = torch.max(torch.tensor(0), weights[:, idx_wpos].squeeze() - (u[idx_wpos] + q[idx_wpos]))
                    weights.data[0, idx_wneg] = torch.min(torch.tensor(0), weights[:, idx_wneg].squeeze() + (u[idx_wneg] - q[idx_wneg]))

                    q = q + (weights.squeeze() - z)

            test_loss = None
            if self.early_stopping:
                with torch.no_grad():
                    outputs = self.model(X_test)
                    test_loss = criterion(torch.squeeze(outputs), y_test).mean().tolist()

            training_finished = self._training_step(train_loss=loss.tolist(),
                                                    dof=weights.squeeze().count_nonzero().tolist(),
                                                    test_loss=test_loss,
                                                    do_early_stopping_check=self.train_epoch_ > self.min_iter)
            if training_finished:
                break

            lr_schedule.step()

            if self.shuffle:
                sampled_indices = rng.integers(len(y_bin), size=len(y_bin))
        
        self._collect_parameters()
        return self


class ThresholdSGDModel(PsupertimeBaseModel):
    def __init__(self,
                 sparsity_threshold=1e-3,
                 method="proportional",
                 early_stopping_batches=False,
                 n_batches=1,
                 max_iter=100, 
                 random_state=1234, 
                 regularization=0.01, 
                 n_iter_no_change=5, 
                 early_stopping=False,
                 tol=1e-4,
                 eta0=0.1,
                 gamma=0.95,
                 penalty='elasticnet', 
                 l1_ratio=1, 
                 shuffle=True, 
                 verbosity=0, 
                 validation_fraction=0.1,
                 track_scores=False):

        super(ThresholdSGDModel, self).__init__(method=method, penalty=penalty, l1_ratio=l1_ratio, n_batches=n_batches, max_iter=max_iter, random_state=random_state,
                                        regularization=regularization, learning_rate="exponential", eta0=eta0, verbosity=verbosity, shuffle=shuffle,
                                        early_stopping=early_stopping, early_stopping_batches=early_stopping_batches, 
                                        n_iter_no_change=n_iter_no_change,tol=tol, validation_fraction=validation_fraction, track_scores=track_scores)

        # defines the cutof, below weights will be set to 0 to inroduce sparsity
        self.sparsity_threshold=sparsity_threshold
       
        # gamma for exponential learning rate decay
        self.gamma = gamma

    def _apply_threshold(self, weights):
        """
        Applies the sparsity threshold to weights.
        :param weights: Weights of a logistic model
        :type weights: Needs to be a numpy array
        """
        weights[np.abs(weights) < self.sparsity_threshold] = 0
        return weights

    def _collect_parameters(self):

        coef, intercept = tuple(self.model.parameters())
        coef = coef.detach().numpy().flatten()
        intercept = intercept.detach().numpy().flatten()
        self.coef_ = self._apply_threshold(coef[:-self.k_])
        self.intercept_ = coef[-self.k_:] +  intercept

    def fit(self, X, y, sample_weights=None):
        """Fit ordinal logistic model. 
        Multiclass data is converted to binarized representation and one weight per feature, 
        as well as a threshold for each class is fitted with a binary logistic classifier.

        Derived from a `sklearn.linear.SGDClassifier`, fitted in batches according to `self.n_batches` 
        for reduced memory usage.
        

        :param X: Data as 2d-matrix
        :type X: numpy.array or scipy.sparse
        :param y: ordinal labels
        :type y: Iterable
        :param sample_weight: Label weights for fitting and scoring, defaults to None. Can be used for example for class balancing.
        :type sample_weight: Iterable, optional
        :return: fitted classifier
        :rtype: BatchSGDModel
        """
        rng = np.random.default_rng(self.random_state)
        X, y, X_test, y_test = self._before_fit(X, y, sample_weights)

        if self.early_stopping:
            X_test = torch.Tensor(restructure_X_to_bin(X_test, self.k_))
            y_test = torch.Tensor(restructure_y_to_bin(y_test))

        # diagonal matrix, to construct the binarized X per batch
        thresholds = np.identity(self.k_)
        if sparse.issparse(X):
            thresholds = sparse.csr_matrix(thresholds)

        n = X.shape[0]
        n_features = X.shape[1] + self.k_

        # Logistic regression model
        torch.manual_seed(self.random_state)
        self.model = BinaryLogisticRegression(input_dim=n_features)

        # Applies Gradients each epoch
        optimizer = torch.optim.SGD(self.model.parameters(), lr=self.eta0)

        # Adapts Learning rate each epoch
        lr_schedule = lr_scheduler.ExponentialLR(optimizer, gamma=self.gamma)
        
        # Loss function: Binary Cross Entropy = Log loss
        criterion = torch.nn.BCELoss(reduction="none")

        # Sample weight to balance classes of y
        if sample_weights is None:
            sample_weights = torch.Tensor(np.ones_like(y))
        else:
            sample_weights = torch.Tensor(sample_weights)

        # Mask for applying penalty: Only apply to gene features, don't apply to thresholds
        penalty_mask = torch.Tensor(np.concatenate((np.ones(X.shape[1]), np.zeros(self.k_))))
        
        # binarize only the labels already
        y_bin = torch.Tensor(restructure_y_to_bin(y))
        
        # create an index array and shuffle
        sampled_indices = rng.integers(len(y_bin), size=len(y_bin))

        while True:

            start = 0
            for i in range(1, self.n_batches+1):
                end = (i * len(y_bin) // self.n_batches)
                batch_idx = sampled_indices[start:end]
                batch_idx_mod_n = batch_idx % n
                
                if sparse.issparse(X):
                    # TODO: Fix sparsity! Converting to dense format is a hack to get this to work
                    X_batch = torch.Tensor(sparse.hstack((X[batch_idx_mod_n], thresholds[batch_idx // n])).todense())
                else:
                    X_batch = torch.Tensor(np.hstack((X[batch_idx_mod_n,:], thresholds[batch_idx // n])))
                
                y_batch = y_bin[batch_idx]
                start = end
                sample_weights_batch = sample_weights[batch_idx_mod_n]

                # Set stored gradients to zero
                optimizer.zero_grad()
                
                # Forward pass
                outputs = self.model(X_batch)

                # calculate parameter penalties
                weights, bias = tuple(self.model.parameters())
                l1_term = torch.linalg.vector_norm(penalty_mask * weights, 1)
                l2_term = torch.linalg.vector_norm(penalty_mask * weights, 2) ** 2

                # calculate loss with and without regularization
                loss = (criterion(torch.squeeze(outputs), y_batch) * sample_weights_batch).mean()
                loss = loss + self.regularization * (self.l1_ratio * l1_term + (1 - self.l1_ratio) * l2_term)

                # zerograd, backward pass and weight update WITH regularization
                loss.backward()
                optimizer.step() 

            lr_schedule.step()

            test_loss = None
            if self.early_stopping:
                with torch.no_grad():
                    outputs = self.model(X_test)
                    test_loss = criterion(torch.squeeze(outputs), y_test).mean().tolist()

            dof = np.count_nonzero(self._apply_threshold(weights.squeeze().tonumpy()))
            training_finished = self._training_step(train_loss=loss.tolist(), dof=dof, test_loss=test_loss)
            if training_finished:
                break

            if self.shuffle:
                sampled_indices = rng.integers(len(y_bin), size=len(y_bin))

        self._collect_parameters()
        return self
