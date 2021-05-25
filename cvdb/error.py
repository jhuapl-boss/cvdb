# Copyright 2021 The Johns Hopkins University Applied Physics Laboratory
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from enum import IntEnum


def logger(who):
    return logging.getLogger(__name__).getChild(who)


class ErrorCodes(IntEnum):
    """
    Enumeration of Error codes to support consistency

    CVDB errors are 701-799
    """

    CVDB_ERROR = 700
    DATATYPE_NOT_SUPPORTED = 701
    FUTURE = 702
    REDIS_ERROR = 703
    ASYNC_ERROR = 704
    SERIALIZATION_ERROR = 705
    DATATYPE_MISMATCH = 706
    OBJECT_STORE_ERROR = 707
    RESOURCE_LOCKED = 708
    RESOLUTION_MISMATCH = 709


class CVDBError(Exception):
    """
    Custom Error class that automatically logs the error for you

    When you reach a point in your code where you want to raise an exceptions

        raise SpdbError("The key already exists.  When trying to create key it must not exist", ErrorCodes.SPDB_ERROR)

    Attributes:
        message (string): Error message.
        error_code (ErrorCodes): spdb error code.
    """

    def __init__(self, *args):
        """
        Constructor.

        Args:
            *args: arg[0] should be message and arg[1] should be CVDBError.
        """

        if len(args) > 1:
            log = logger("CVDBError")
            log.error("CVDBError - Message: {0} - Code: {1}".format(args[0], args[1]))
            self.message = args[0]
            self.error_code = args[1]
            return

        if len(args) == 1:
            self.message = args[0]
            self.error_code = ErrorCodes.CVDB_ERROR
            return

        self.message = "No error message given."
        self.error_code = ErrorCodes.CVDB_ERROR
