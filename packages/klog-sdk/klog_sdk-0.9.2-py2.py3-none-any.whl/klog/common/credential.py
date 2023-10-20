# -*- coding: utf-8 -*-
# Copyright 2022 Ksyun Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    # py3
    import configparser
    from urllib.parse import urlencode
    from urllib.request import urlopen
except ImportError:
    # py2
    import ConfigParser as configparser
    from urllib import urlencode
    from urllib import urlopen

from klog.common.exception.klog_exception import KlogException


class Credential(object):
    def __init__(self, access_key, secret_key, token=None):
        """Ksyun Credentials.
        :param access_key: The secret id of your credential.
        :type access_key: str
        :param secret_key: The secret key of your credential.
        :type secret_key: str
        :param token: The federation token of your credential, if this field
                      is specified, secret_id and secret_key should be set
        """
        if access_key is None or access_key.strip() == "":
            raise KlogException("InvalidCredential", "access key should not be none or empty")
        if access_key.strip() != access_key:
            raise KlogException("InvalidCredential", "access key should not contain spaces")
        self.access_key = access_key

        if secret_key is None or secret_key.strip() == "":
            raise KlogException("InvalidCredential", "secret key should not be none or empty")
        if secret_key.strip() != secret_key:
            raise KlogException("InvalidCredential", "secret key should not contain spaces")
        self.secret_key = secret_key

        self.token = token

    @property
    def secret_id(self):
        return self.access_key
