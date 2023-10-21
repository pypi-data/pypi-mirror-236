#  Copyright (c) 2018-2020 VMware, Inc. All rights reserved

import logging
import typing

import numpy as np

from model_manager.models.scoring_utils import MeanSquaredScore
from model_manager.stores.model_store import TensorDef


class PredictiveModel(object):
    """
    This a general-purpose model - works with named tensors without any additional semantics behind what the tensors
    represent.
    """

    def __init__(self, input_defs: typing.List[TensorDef], output_defs: typing.List[TensorDef]):
        self._logger = logging.getLogger(__name__)
        self._input_defs = input_defs
        self._output_defs = output_defs

    @property
    def input_defs(self):
        return self._input_defs

    @property
    def output_defs(self):
        return self._output_defs

    def build_model(self):
        """
        build model object using the file and parameters
        Returns: the constructed model
        """
        raise NotImplementedError()

    def seed(self, seed: int):
        """
        Set the seed to use for deterministic predictions. Calling predict() with the same inputs, the same seed and
        deterministic set to True should result in the same output even for stochastic models.
        :param seed:
        """
        pass

    def reset(self):
        pass

    @classmethod
    def get_model_type(cls):
        """
        The type of the model
        :return:
        """
        raise NotImplementedError()

    def compute_mse_error(self, true_outputs: typing.Dict[str, np.ndarray], predicted_outputs: typing.Dict[str, np.ndarray], compare_keys=None) -> float:
        """
        Helper function to get standardized mse loss from the model
        :param true_outputs: the actual values as dictionary
        :param predicted_outputs: the predicted values as dictionary
        :param compare_keys: if specified the loss value will consider only the components provided here
        :return the average mse
        """
        losses = self.compute_mse_per_component(true_outputs, predicted_outputs, compare_keys)
        return float(np.mean(list(losses.values())))

    def compute_mse_per_component(self, true_outputs: typing.Dict[str, np.ndarray], predicted_outputs: typing.Dict[str, np.ndarray], compare_keys=None) -> typing.Dict[str, float]:
        """
        Helper function to get standardized mse loss from the model per component
        :param true_outputs: the actual values as dictionary
        :param predicted_outputs: the predicted values as dictionary
        :param compare_keys: if specified the loss value will consider only the components provided here
        :return the mse per component
        """
        compare_keys = predicted_outputs.keys() if not compare_keys else compare_keys

        if self.outputs_standardizer:
            std_t_out = self.outputs_standardizer.transform(true_outputs, inplace=False, fit=False)
            std_p_out = self.outputs_standardizer.transform(predicted_outputs, inplace=False, fit=False)
        else:
            std_t_out = true_outputs
            std_p_out = predicted_outputs

        mse_calculator = MeanSquaredScore({})
        losses = {k: mse_calculator.calc_loss(std_t_out[k], std_p_out[k]) for k in compare_keys}
        return losses
