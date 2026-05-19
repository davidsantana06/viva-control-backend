from flask_restx import Namespace
from flask_restx.inputs import boolean
from flask_restx.reqparse import RequestParser
from typing import get_args

from app.dtos import FindAllParams, UserScopedFindAllParams
from app.types import SortOrder


class FindAllFactory:
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
        return FindAllParams(**args)

    @classmethod
    def build_user_scoped_find_all_parser(cls, ns: Namespace) -> RequestParser:
        parser = cls.build_find_all_parser(ns)
        parser.add_argument(
            "user_scoped",
            location="args",
            type=boolean,
            default=False,
            help="Restrict results to records created by the current user only",
        )
        return parser

    @staticmethod
    def build_user_scoped_find_all_params(
        request_parser: RequestParser,
    ) -> UserScopedFindAllParams:
        args = request_parser.parse_args()
        return UserScopedFindAllParams(**args)
