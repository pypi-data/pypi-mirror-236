#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (c) 2018-2020 VMware, Inc. All rights reserved

import logging
from typing import Optional, Dict, List

from model_manager.stores.dataset_store import DatasetRef


class Dataset(object):
    """ General Dataset with environment specs interactions"""
    logger = logging.getLogger(__name__)

    def __init__(self,
                 org_id: Optional[str],
                 states,
                 dataset_ref: Optional[DatasetRef] = None,
                 ):
        """
        :param dataset_ref: The dataset ref, if the dataset is already stored
        :param org_id: the org_id owning the data, if there is one
        :param states:
        """
        self.org_id = org_id
        self.dataset_ref = dataset_ref
        self.states = states

