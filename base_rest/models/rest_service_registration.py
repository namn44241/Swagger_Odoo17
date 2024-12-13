# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from odoo import models
from odoo.http import Controller

from ..core import (
    RestServicesRegistry,
    _rest_controllers_per_module,
    _rest_services_databases,
)

_logger = logging.getLogger(__name__)


class RestServiceRegistration(models.AbstractModel):
    _name = "rest.service.registration"
    _description = "REST Services Registration Model"

    def _register_hook(self):
        # This method is called by Odoo when the registry is built
        services_registry = self._init_global_registry()
        self._build_controllers_routes(services_registry)
        return super()._register_hook()

    def _build_controllers_routes(self, services_registry):
        """Build the controllers and routes for REST services"""
        for service, controller_def in services_registry.items():
            self._build_controller(service, controller_def)

    def _build_controller(self, service, controller_def):
        """Build a controller for the given service"""
        base_controller_cls = controller_def["controller_class"]
        addon_name = base_controller_cls._module
        
        # Register controller into available controllers
        if addon_name not in Controller.children_classes:
            Controller.children_classes[addon_name] = []
        Controller.children_classes[addon_name].append(base_controller_cls)

    def _init_global_registry(self):
        """Initialize the global registry for REST services"""
        services_registry = RestServicesRegistry()
        _rest_services_databases[self.env.cr.dbname] = services_registry
        return services_registry
