# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import collections
from odoo.http import Controller, request
from odoo.addons.component.core import WorkContext, _get_addon_name


class RestServicesDatabases(dict):
    """Holds a registry of REST services for each database"""


class RestServicesRegistry(dict):
    """Holds a registry of REST services where key is the root of the path on
    which the methods of your RestController are registered and value is the
    name of the collection on which your RestServiceComponent implementing
    the business logic of your service is registered."""


_rest_services_databases = RestServicesDatabases()
_rest_services_routes = collections.defaultdict(set)
_rest_controllers_per_module = collections.defaultdict(list)


class _PseudoCollection(object):
    """A collection that can be used by REST services"""
    __slots__ = "_name", "env"

    def __init__(self, name, env):
        self._name = name
        self.env = env


class RestController(Controller):
    """Base REST Controller"""
    _root_path = None
    _collection_name = None
    _default_auth = "user"

    @classmethod
    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls._root_path and cls._collection_name:
            # Register controller
            module = _get_addon_name(cls.__module__)
            _rest_controllers_per_module[module].append({
                'root_path': cls._root_path,
                'collection_name': cls._collection_name,
                'controller_class': cls,
            })

    def _get_component_context(self):
        """Get the component context"""
        collection = _PseudoCollection(self._collection_name, request.env)
        return {
            'collection': collection,
            'request': request,
            'controller': self,
        }

    def make_response(self, data):
        """Make the HTTP Response"""
        return request.make_json_response(data)


def _get_service_registry(env):
    """Get the service registry for the current database"""
    dbname = env.cr.dbname
    if dbname not in _rest_services_databases:
        _rest_services_databases[dbname] = RestServicesRegistry()
    return _rest_services_databases[dbname]
