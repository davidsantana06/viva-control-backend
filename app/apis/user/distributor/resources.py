from flask_restx import Resource
from http import HTTPStatus

from app.decorators import (
    activate_resource,
    auth_required,
    create_resource,
    deactivate_resource,
    get_resource,
    list_resource,
    update_resource,
)
from app.exceptions import (
    EmailAlreadyRegisteredException,
    UserNotFoundException,
)
from app.factories import FindAllFactory
from app.services import DistributorService
from app.types import UserRole

from .. import user_ns
from ..models import create_user_model, update_user_model, user_model


@user_ns.route("/distributor")
class DistributorListResource(Resource):
    __find_all_parser = FindAllFactory.build_find_all_parser(user_ns)

    @create_resource(
        user_ns,
        create_user_model,
        user_model,
        EmailAlreadyRegisteredException,
    )
    @auth_required(UserRole.ADMIN)
    def post(self, **_):
        """Create a new distributor"""
        dto = {**user_ns.payload, "role": UserRole.DISTRIBUTOR}
        return DistributorService.create(dto), HTTPStatus.CREATED

    @list_resource(user_ns, __find_all_parser, user_model)
    @auth_required(UserRole.ADMIN)
    def get(self, **_):
        """Get all distributors"""
        find_all_params = FindAllFactory.build_find_all_params(self.__find_all_parser)
        return DistributorService.find_all(find_all_params)


@user_ns.route("/distributor/<int:id>")
@user_ns.param("id", "The distributor identifier")
class DistributorResource(Resource):
    @get_resource(user_ns, user_model, UserNotFoundException)
    @auth_required(UserRole.ADMIN)
    def get(self, id: int, **_):
        """Get a distributor by ID"""
        return DistributorService.find_first_or_raise(id)

    @update_resource(
        user_ns,
        update_user_model,
        user_model,
        UserNotFoundException,
        EmailAlreadyRegisteredException,
    )
    @auth_required(UserRole.ADMIN)
    def patch(self, id: int, **_):
        """Update a distributor by ID"""
        return DistributorService.update(id, user_ns.payload)


@user_ns.route("/distributor/<int:id>/activate")
@user_ns.param("id", "The distributor identifier")
class DistributorActivateResource(Resource):
    @activate_resource(user_ns, UserNotFoundException)
    @auth_required(UserRole.ADMIN)
    def patch(self, id: int, **_):
        """Activate a distributor"""
        DistributorService.activate(id)
        return "", HTTPStatus.NO_CONTENT


@user_ns.route("/distributor/<int:id>/deactivate")
@user_ns.param("id", "The distributor identifier")
class DistributorDeactivateResource(Resource):
    @deactivate_resource(user_ns, UserNotFoundException)
    @auth_required(UserRole.ADMIN)
    def patch(self, id: int, **_):
        """Deactivate a distributor"""
        DistributorService.deactivate(id)
        return "", HTTPStatus.NO_CONTENT
