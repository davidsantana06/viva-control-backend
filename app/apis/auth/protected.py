from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource

from . import auth_ns


@auth_ns.route("/protected")
class Protected(Resource):
    @auth_ns.doc("protected", security="Bearer")
    @jwt_required()
    def get(self):
        """Protected route example"""
        return {"logged_in_as": get_jwt_identity()}
