from flask_restx import Namespace
from flask_restx.reqparse import RequestParser
from typing import get_args

from app.types import FindAllParams, SortOrder


def set_find_all_parser(ns: Namespace) -> RequestParser:
    parser = ns.parser()
    parser.add_argument("q", location="args", help="Search term")
    parser.add_argument("sort", location="args", default="id", help="Field to sort by")
    parser.add_argument(
        "order",
        location="args",
        default="ASC",
        choices=get_args(SortOrder),
        help="Sort order",
    )
    parser.add_argument(
        "page",
        location="args",
        type=int,
        default=1,
        help="Page number",
    )
    parser.add_argument(
        "per_page",
        location="args",
        type=int,
        default=10,
        help="Items per page",
    )
    return parser


def parse_find_all_args(parser: RequestParser) -> FindAllParams:
    args = parser.parse_args()
    return FindAllParams(
        q=args.q,
        sort=args.sort,
        order=args.order,
        page=args.page,
        per_page=args.per_page,
    )
