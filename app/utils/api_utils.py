from flask import g
from flask_restx import Namespace
from flask_restx.reqparse import RequestParser
from typing import get_args

from app.types import CurrentUser, FindAllParams, SortOrder


class ApiUtils:
    @staticmethod
    def bind_current_user(current_user: CurrentUser) -> None:
        g.current_user = current_user

    @staticmethod
    def resolve_current_user() -> CurrentUser:
        return g.current_user

    @staticmethod
    def build_find_all_parser(ns: Namespace) -> RequestParser:
        request_parser = ns.parser()
        request_parser.add_argument("q", location="args", help="Search term")
        request_parser.add_argument(
            "sort",
            location="args",
            default="id",
            help="Field to sort by",
        )
        request_parser.add_argument(
            "order",
            location="args",
            default="ASC",
            choices=get_args(SortOrder),
            help="Sort order",
        )
        request_parser.add_argument(
            "page",
            location="args",
            type=int,
            default=1,
            help="Page number",
        )
        request_parser.add_argument(
            "per_page",
            location="args",
            type=int,
            default=10,
            help="Items per page",
        )
        return request_parser

    @staticmethod
    def build_find_all_params(request_parser: RequestParser) -> FindAllParams:
        args = request_parser.parse_args()
        return FindAllParams(
            q=args.q,
            sort=args.sort,
            order=args.order,
            page=args.page,
            per_page=args.per_page,
        )
