from functools import wraps
from http import HTTPStatus

from flask_restx import Namespace
from flask_restx.model import Model as ApiModel
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
            Security.require_access_token()
            identity, claims = Security.get_identity(), Security.get_claims()
            current_user = CurrentUser(id=identity, **claims["user"])

            role_not_allowed = allowed_roles and not current_user.has_any_role(*allowed_roles)
            if role_not_allowed:
                raise RoleNotAllowedException()

            return func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator


def create_resource(
    ns: Namespace,
    input_model: ApiModel,
    output_model: ApiModel,
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


def list_resource(ns: Namespace, request_parser: RequestParser, output_model: ApiModel):
    def decorator(func):
        func = ns.doc("list", security="Bearer")(func)
        func = ns.expect(request_parser)(func)
        func = ns.marshal_list_with(output_model)(func)
        return func
    return decorator


def get_resource(
    ns: Namespace,
    output_model: ApiModel,
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
    input_model: ApiModel,
    output_model: ApiModel,
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


def _no_content_resource(shortcut: str, ns: Namespace, *exception_classes: type[ApiException]):
    def decorator(func):
        func = ns.doc(shortcut, security="Bearer")(func)
        func = ns.response(HTTPStatus.NO_CONTENT, "Success")(func)
        for exc_class in exception_classes:
            func = ns.response(*exc_class.get_api_specs())(func)
        return func
    return decorator


def activate_resource(ns: Namespace, *exception_classes: type[ApiException]):
    return _no_content_resource("activate", ns, *exception_classes)


def deactivate_resource(ns: Namespace, *exception_classes: type[ApiException]):
    return _no_content_resource("deactivate", ns, *exception_classes)


def delete_resource(ns: Namespace, *exception_classes: type[ApiException]):
    return _no_content_resource("delete", ns, *exception_classes)
