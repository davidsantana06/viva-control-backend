from functools import wraps
from http import HTTPStatus

from flask_restx import Namespace
from flask_restx.model import Model
from flask_restx.reqparse import RequestParser

from app.exceptions import ApiException, InvalidPayload, RoleNotAllowed
from app.proxies import JwtProxy
from app.types import CurrentUser, UserRole
from app.utils import ApiUtils


def role_required(*roles: UserRole):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            JwtProxy.verify_or_raise()
            claims = JwtProxy.get_claims()

            role_not_allowed = claims["role"] not in roles
            if role_not_allowed:
                raise RoleNotAllowed()

            current_user = CurrentUser(JwtProxy.get_identity(), **claims)
            ApiUtils.bind_current_user(current_user)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def create_resource(
    ns: Namespace,
    input_model: Model,
    output_model: Model,
    *exception_classes: type[ApiException],
):
    def decorator(func):
        func = ns.doc(f"create_{ns.name}", security="Bearer")(func)
        func = ns.expect(input_model)(func)
        func = ns.marshal_with(output_model, code=HTTPStatus.CREATED)(func)
        func = ns.response(*InvalidPayload.get_specs())(func)
        for exc_class in exception_classes:
            func = ns.response(*exc_class.get_specs())(func)
        return func

    return decorator


def list_resource(ns: Namespace, request_parser: RequestParser, output_model: Model):
    def decorator(func):
        func = ns.doc(f"list_{ns.name}", security="Bearer")(func)
        func = ns.expect(request_parser)(func)
        func = ns.marshal_list_with(output_model)(func)
        return func

    return decorator


def get_resource(
    ns: Namespace,
    output_model: Model,
    *exception_classes: type[ApiException],
):
    def decorator(func):
        func = ns.doc(f"get_{ns.name}", security="Bearer")(func)
        func = ns.marshal_with(output_model)(func)
        for exc_class in exception_classes:
            func = ns.response(*exc_class.get_specs())(func)
        return func

    return decorator


def update_resource(
    ns: Namespace,
    input_model: Model,
    output_model: Model,
    *exception_classes: type[ApiException],
):
    def decorator(func):
        func = ns.doc(f"update_{ns.name}", security="Bearer")(func)
        func = ns.expect(input_model)(func)
        func = ns.marshal_with(output_model)(func)
        func = ns.response(*InvalidPayload.get_specs())(func)
        for exc_class in exception_classes:
            func = ns.response(*exc_class.get_specs())(func)
        return func

    return decorator


def deactivate_resource(ns: Namespace, *exception_classes: type[ApiException]):
    def decorator(func):
        func = ns.doc(f"deactivate_{ns.name}", security="Bearer")(func)
        func = ns.response(HTTPStatus.NO_CONTENT, "Success")(func)
        for exc_class in exception_classes:
            func = ns.response(*exc_class.get_specs())(func)
        return func

    return decorator
