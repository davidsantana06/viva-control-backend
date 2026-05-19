from functools import wraps
from http import HTTPStatus

from flask_restx import Namespace
from flask_restx.model import Model
from flask_restx.reqparse import RequestParser

from app.exceptions import (
    ApiException,
    InvalidPayloadException,
    RoleNotAllowedException,
)
from app.facades import Security
from app.dtos import CurrentUser
from app.types import UserRole


def auth_required(*allowed_roles: UserRole):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            Security.require_jwt()
            identity, claims = Security.get_jwt_identity(), Security.get_jwt_claims()
            current_user = CurrentUser(id=identity, **claims["user"])

            if not current_user.has_any_role(*allowed_roles):
                raise RoleNotAllowedException()

            return func(*args, current_user=current_user, **kwargs)

        return wrapper

    return decorator


def create_resource(
    ns: Namespace,
    input_model: Model,
    output_model: Model,
    *exception_classes: type[ApiException],
):
    def decorator(func):
        func = ns.doc("create", security="Bearer")(func)
        func = ns.expect(input_model)(func)
        func = ns.marshal_with(output_model, code=HTTPStatus.CREATED)(func)
        func = ns.response(*InvalidPayloadException.get_api_specs())(func)
        for exc_class in exception_classes:
            func = ns.response(*exc_class.get_api_specs())(func)
        return func

    return decorator


def list_resource(ns: Namespace, request_parser: RequestParser, output_model: Model):
    def decorator(func):
        func = ns.doc("list", security="Bearer")(func)
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
        func = ns.doc("get", security="Bearer")(func)
        func = ns.marshal_with(output_model)(func)
        for exc_class in exception_classes:
            func = ns.response(*exc_class.get_api_specs())(func)
        return func

    return decorator


def update_resource(
    ns: Namespace,
    input_model: Model,
    output_model: Model,
    *exception_classes: type[ApiException],
):
    def decorator(func):
        func = ns.doc("update", security="Bearer")(func)
        func = ns.expect(input_model)(func)
        func = ns.marshal_with(output_model)(func)
        func = ns.response(*InvalidPayloadException.get_api_specs())(func)
        for exc_class in exception_classes:
            func = ns.response(*exc_class.get_api_specs())(func)
        return func

    return decorator


def delete_resource(ns: Namespace, *exception_classes: type[ApiException]):
    def decorator(func):
        func = ns.doc("delete", security="Bearer")(func)
        func = ns.response(HTTPStatus.NO_CONTENT, "Success")(func)
        for exc_class in exception_classes:
            func = ns.response(*exc_class.get_api_specs())(func)
        return func

    return decorator
