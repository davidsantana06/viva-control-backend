from flask_restx import fields


timestamp_fields = {
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True),
}
