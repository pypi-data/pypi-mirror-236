#  Copyright (c) 2018-2020 VMware, Inc. All rights reserved

from typing import Dict

import numpy as np
from math import sqrt
from scipy.special import logsumexp
from sklearn.metrics import mean_squared_error

from model_manager.common.serializable import Serializable


class ScoringParams(Serializable):
    """ Serializable Scoring Parameters """
    def __init__(self, method_name: str, method_params: Dict):
        """
        Scoring Parameters
        :param method_name: such as MEAN_SQUARED_ERR, etc.
        :param method_params: scoring method's sample_weights, multioutput, etc
        """
        self.method_name = method_name
        self.method_params = method_params


class ScoringMethod(Serializable):
    def __init__(self, params: Dict):
        """
        A class of Scoring method
        :param params: method_params
        """
        self.params = params

    def calc_loss(self, y_true, y_pred, features=None):
        raise NotImplementedError

    @staticmethod
    def get_method_name():
        raise NotImplementedError

    @classmethod
    def get_default_params(cls):
        raise NotImplementedError


class MeanSquaredScore(ScoringMethod):
    def calc_loss(self, y_true, y_pred, features=None):
        return mean_squared_error(y_true, y_pred, **self.params)

    @staticmethod
    def get_method_name():
        return "MEAN_SQUARED_ERR"

    @classmethod
    def get_default_params(cls):
        return {}


class RootMeanSquaredScore(ScoringMethod):
    def calc_loss(self, y_true, y_pred, features=None):
        return sqrt(mean_squared_error(y_true, y_pred, **self.params))

    @staticmethod
    def get_method_name():
        return "ROOT_MEAN_SQUARED_ERR"

    @classmethod
    def get_default_params(cls):
        return {}


class PredictiveNegativeLogLikelihoodScore(ScoringMethod):
    """test log-likelihood from paper Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning
    https://github.com/yaringal/DropoutUncertaintyExps/blob/master/net/net.py"""
    PARAM_NUM_SAMPLES = "T"

    def calc_loss(self, y_true, y_pred, features=None):
        num_samples = self.params.get(self.PARAM_NUM_SAMPLES)
        assert y_pred.shape[0] == num_samples
        assert y_true.ndim + 1 == y_pred.ndim and y_true.shape == y_pred.shape[1:], f"requires sampling: y_pred dimension should be (num_samples," \
                                                                                    f") + {y_true.shape} but is {y_pred.shape}"

        # we expect to work with normalized data (standard deviation = 1)
        ll = logsumexp(-0.5 * (y_true - y_pred) ** 2., 0) - np.log(num_samples) - 0.5 * np.log(2 * np.pi)
        test_ll = np.mean(ll)
        return - test_ll

    @staticmethod
    def get_method_name():
        return "PREDICTIVE_NEGATIVE_LOG_LIKELIHOOD"

    @classmethod
    def get_default_params(cls):
        return {cls.PARAM_NUM_SAMPLES: 100}


class MeanAbsolutePercentageErrorScore(ScoringMethod):
    PARAM_DENOMINATOR_DEFAULT = "D"
    PARAM_OVERRIDE_THRESHOLD_DEFAULT = "D_THRESHOLD"

    def calc_loss(self, y_true, y_pred, features=None):
        denominator_default = self.params.get(self.PARAM_DENOMINATOR_DEFAULT)
        denominator_override_default = self.params.get(self.PARAM_OVERRIDE_THRESHOLD_DEFAULT)
        y_true_non_zero = np.where((denominator_override_default[1] <= y_true) & (y_true < denominator_override_default[2]),
                                   denominator_default, y_true)
        y_true_non_zero = np.where((denominator_override_default[0] < y_true) & (y_true < denominator_override_default[1]), -denominator_default,
                                   y_true_non_zero)
        return np.mean(np.abs((y_true - y_pred) / y_true_non_zero)) * 100

    @staticmethod
    def get_method_name():
        return "MEAN_ABSOLUTE_PERCENTAGE_ERR"

    @classmethod
    def get_default_params(cls):
        return {cls.PARAM_DENOMINATOR_DEFAULT: 1,
                cls.PARAM_OVERRIDE_THRESHOLD_DEFAULT: (-1, 0, 1)}


class MeanDirectionalAccuracyScore(ScoringMethod):

    def calc_loss(self, y_true, y_pred, features=None):
        # MDA for multidimensional states needs to be investigated further.
        true_directions: np.ndarray = features > y_true
        pred_directions: np.ndarray = features > y_pred
        return np.sum(true_directions == pred_directions) / true_directions.size

    @staticmethod
    def get_method_name():
        return "MEAN_DIRECTIONAL_ACCURACY"

    @classmethod
    def get_default_params(cls):
        return {}
