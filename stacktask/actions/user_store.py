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

from openstack_clients import get_keystoneclient
from keystoneclient.openstack.common.apiclient import (
    exceptions as ks_exceptions
)


def get_managable_roles(user_roles):
    """
    Given a list of user role names, returns a list of names
    that the user is allowed to manage.
    """
    # hardcoded mapping between roles and managable roles
    # Todo: relocate to settings file.
    manage_mapping = {
        'admin': [
            'project_owner', 'project_mod', 'Member', 'heat_stack_owner',
            '_member_'
        ],
        'project_owner': [
            'project_mod', 'Member', 'heat_stack_owner', '_member_'
        ],
        'project_mod': [
            'Member', 'heat_stack_owner', '_member_'
        ],
    }
    # merge mapping lists to form a flat permitted roles list
    managable_role_names = [mrole for role_name in user_roles
                            if role_name in manage_mapping
                            for mrole in manage_mapping[role_name]]
    # a set has unique items
    managable_role_names = set(managable_role_names)
    return managable_role_names


class IdentityManager(object):
    """
    A wrapper object for the Keystone Client. Mainly setup as
    such for easier testing, but also so it can be replaced
    later with an LDAP + Keystone Client variant.
    """

    def __init__(self):
        self.ks_client = get_keystoneclient()

    def find_user(self, name):
        try:
            user = self.ks_client.users.find(name=name)
        except ks_exceptions.NotFound:
            user = None
        return user

    def get_user(self, user_id):
        try:
            user = self.ks_client.users.get(user_id)
        except ks_exceptions.NotFound:
            user = None
        return user

    def create_user(self, name, password, email, project_id):
        user = self.ks_client.users.create(
            name=name, password=password,
            email=email, tenant_id=project_id)
        return user

    def update_user_password(self, user, password):
        self.ks_client.users.update_password(user, password)

    def find_role(self, name):
        try:
            role = self.ks_client.roles.find(name=name)
        except ks_exceptions.NotFound:
            role = None
        return role

    def get_roles(self, user, project):
        return self.ks_client.roles.roles_for_user(user, tenant=project)

    def add_user_role(self, user, role, project_id):
        self.ks_client.roles.add_user_role(user, role, project_id)

    def remove_user_role(self, user, role, project_id):
        self.ks_client.roles.remove_user_role(user, role, project_id)

    def find_project(self, project_name):
        try:
            project = self.ks_client.tenants.find(name=project_name)
        except ks_exceptions.NotFound:
            project = None
        return project

    def get_project(self, project_id):
        try:
            project = self.ks_client.tenants.get(project_id)
        except ks_exceptions.NotFound:
            project = None
        return project

    def create_project(self, project_name, created_on):
        project = self.ks_client.tenants.create(project_name,
                                                created_on=created_on)
        return project