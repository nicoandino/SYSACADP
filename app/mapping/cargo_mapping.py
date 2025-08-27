from marshmallow import fields, Schema, post_load, validate
from app.models import Cargo

class CargoMapping(Schema):
    id = fields.Integer(dump_only=True)
    descripcion = fields.String(required=True, validate=validate.Length(min=1, max=50))
    puntos = fields.Integer(allow_none=True)
    categoria_cargo_id = fields.Integer(required=True, load_only=True)
    tipo_dedicacion_id = fields.Integer(required=True, load_only=True)

    @post_load
    def nuevo_cargo(self, data, **kwargs):
        return Cargo(**data)
