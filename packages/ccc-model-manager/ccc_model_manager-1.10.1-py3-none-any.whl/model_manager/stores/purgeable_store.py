#  Copyright (c) 2020 VMware, Inc. All rights reserved
from datetime import datetime
from typing import Tuple, List


class PurgeableStore(object):
    """
    Base class for stores that are purged periodically for unused artifacts
    It surfaces APIs related to the same (listing/purging artifacts)
    """

    def purge_non_accessed_data(self, purge_before_timestamp: datetime, dry_run: bool = False) -> Tuple[int, List]:
        """
        Purge records which have not been accessed since the given datetime
        :param purge_before_timestamp:
        :param dry_run:
        :return:
        """
        raise NotImplementedError()
