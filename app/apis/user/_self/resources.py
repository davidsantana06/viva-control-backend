from flask_restx import Resource

from app.decorators import auth_required, get_resource, update_resource
from app.exceptions import UserNotFoundException
from app.services import SelfService
from app.dtos import CurrentUser

from .. import user_ns
from ..models import update_user_model, user_model


@user_ns.route("/_self")
class SelfResource(Resource):
    @get_resource(user_ns, user_model, UserNotFoundException)
    @auth_required()
    def get(self, current_user: CurrentUser):
        """Get own profile"""
        return SelfService.find_first_or_raise(current_user.id)

    @update_resource(user_ns, update_user_model, user_model, UserNotFoundException)
    @auth_required()
    def patch(self, current_user: CurrentUser):
        """Update own profile"""
        return SelfService.update(current_user.id, user_ns.payload)
