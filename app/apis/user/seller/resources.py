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
from app.factories import FindAllFactory, UserFilterFactory
from app.services import SellerService
from app.dtos import CurrentUser
from app.types import UserRole
from app.utils import DtoUtils

from .. import user_ns
from ..models import create_user_model, update_user_model, user_model


@user_ns.route("/seller")
class SellerListResource(Resource):
    __find_all_parser = FindAllFactory.build_find_all_parser(user_ns)

    @create_resource(
        user_ns,
        create_user_model,
        user_model,
        EmailAlreadyRegisteredException,
    )
    @auth_required(UserRole.ADMIN, UserRole.DISTRIBUTOR)
    def post(self, current_user: CurrentUser):
        """Create a new seller"""
        dto = {**user_ns.payload, "role": UserRole.SELLER}
        DtoUtils.inject_user_ids(dto, current_user)
        return SellerService.create(dto), HTTPStatus.CREATED

    @list_resource(user_ns, __find_all_parser, user_model)
    @auth_required(UserRole.ADMIN, UserRole.DISTRIBUTOR)
    def get(self, current_user: CurrentUser):
        """Get all sellers"""
        find_all_params = FindAllFactory.build_find_all_params(self.__find_all_parser)
        user_filter = UserFilterFactory.build_strict_distributor_filter(current_user)
        return SellerService.find_all(find_all_params, user_filter)


@user_ns.route("/seller/<int:id>")
@user_ns.param("id", "The seller identifier")
class SellerResource(Resource):
    @get_resource(user_ns, user_model, UserNotFoundException)
    @auth_required(UserRole.ADMIN, UserRole.DISTRIBUTOR)
    def get(self, id: int, current_user: CurrentUser):
        """Get a seller by ID"""
        user_filter = UserFilterFactory.build_strict_distributor_filter(current_user)
        return SellerService.find_first_or_raise(id, user_filter)

    @update_resource(
        user_ns,
        update_user_model,
        user_model,
        UserNotFoundException,
        EmailAlreadyRegisteredException,
    )
    @auth_required(UserRole.ADMIN, UserRole.DISTRIBUTOR)
    def patch(self, id: int, current_user: CurrentUser):
        """Update a seller by ID"""
        user_filter = UserFilterFactory.build_strict_distributor_filter(current_user)
        return SellerService.update(id, user_ns.payload, user_filter)


@user_ns.route("/seller/<int:id>/activate")
@user_ns.param("id", "The seller identifier")
class SellerActivateResource(Resource):
    @activate_resource(user_ns, UserNotFoundException)
    @auth_required(UserRole.ADMIN, UserRole.DISTRIBUTOR)
    def patch(self, id: int, current_user: CurrentUser):
        """Activate a seller"""
        user_filter = UserFilterFactory.build_strict_distributor_filter(current_user)
        SellerService.activate(id, user_filter)
        return "", HTTPStatus.NO_CONTENT


@user_ns.route("/seller/<int:id>/deactivate")
@user_ns.param("id", "The seller identifier")
class SellerDeactivateResource(Resource):
    @deactivate_resource(user_ns, UserNotFoundException)
    @auth_required(UserRole.ADMIN, UserRole.DISTRIBUTOR)
    def patch(self, id: int, current_user: CurrentUser):
        """Deactivate a seller"""
        user_filter = UserFilterFactory.build_strict_distributor_filter(current_user)
        SellerService.deactivate(id, user_filter)
        return "", HTTPStatus.NO_CONTENT
