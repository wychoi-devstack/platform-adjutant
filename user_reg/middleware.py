# Copyright (C) 2015 Catalyst IT Ltd
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from time import time
from logging import getLogger
from django.utils import timezone


class KeystoneHeaderUnwrapper(object):
    """"""
    def process_request(self, request):
        try:
            token_data = {
                'project_name': request.META['HTTP_X_PROJECT_NAME'],
                'project_id': request.META['HTTP_X_PROJECT_ID'],
                'roles': request.META['HTTP_X_ROLES'].split(','),
                'username': request.META['HTTP_X_USER_NAME'],
                'user_id': request.META['HTTP_X_USER_ID'],
                'authenticated': request.META['HTTP_X_IDENTITY_STATUS']
            }
        except KeyError:
            token_data = {}
        request.keystone_user = token_data


class TestingHeaderUnwrapper(object):
    """"""
    def process_request(self, request):
        try:
            token_data = {
                'project_name': request.META['headers']['project_name'],
                'project_id': request.META['headers']['project_id'],
                'roles': request.META['headers']['roles'].split(','),
                'username': request.META['headers']['username'],
                'user_id': request.META['headers']['user_id'],
                'authenticated': request.META['headers']['authenticated']
            }
        except KeyError:
            token_data = {}
        request.keystone_user = token_data


class RequestLoggingMiddleware(object):
    def __init__(self):
        self.logger = getLogger('django.request')

    def process_request(self, request):
        self.logger.info(
            '<%s> %s [%s] - (%s)',
            request.method,
            request.META['REMOTE_ADDR'],
            request.get_full_path(),
            timezone.now()
        )
        request.timer = time()

    def process_response(self, request, response):
        self.logger.info(
            '<%s> [%s] - (%.1fs)',
            response.status_code,
            request.get_full_path(),
            time() - request.timer
        )
        return response
