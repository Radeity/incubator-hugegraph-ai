# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import json

from pyhugegraph.utils.exceptions import ServiceUnavailableException, NotAuthorizedError, NotFoundError


def create_exception(response_content):
    data = json.loads(response_content)
    if "ServiceUnavailableException" in data["exception"]:
        raise ServiceUnavailableException('ServiceUnavailableException, "message": "{}", "cause": "{}"'.
                                          format(data["message"], data["cause"]))
    else:
        raise Exception(response_content)


def check_if_authorized(response):
    if response.status_code == 401:
        raise NotAuthorizedError("Please check your username and password. {}".format(response.content))
    return True


def check_if_success(response, error=None):
    if (not str(response.status_code).startswith("20")) and check_if_authorized(response):
        if error is None:
            error = NotFoundError(response.content)
        raise error
    return True
