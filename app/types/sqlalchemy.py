from sqlalchemy import ColumnElement, UnaryExpression


Filter = ColumnElement[bool]

Ordering = UnaryExpression[object]
