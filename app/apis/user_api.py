from flask_restx import Namespace, Resource


users_api = Namespace(
    "users",
    description="User related operations",
    path="/user",
    validate=True,
)


@users_api.route("/")
class UserList(Resource):
    pass


@users_api.route("/<int:id>")
@users_api.param("id", "The user identifier")
class User(Resource):
    pass
