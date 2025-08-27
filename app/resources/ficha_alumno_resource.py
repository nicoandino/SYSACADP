# app/resources/ficha_alumno_resource.py
from flask import Blueprint, jsonify, abort
from app.services.alumno_service import AlumnoService

ficha_bp = Blueprint("ficha", __name__)

@ficha_bp.route("/ficha/<int:nro_legajo>", methods=["GET"])
def ficha_alumno(nro_legajo: int):
    alumno = AlumnoService.buscar_por_id(nro_legajo)
    if not alumno:
        abort(404, description="Alumno no encontrado")

    data = {
        "nro_legajo": alumno.nro_legajo,
        "apellido": alumno.apellido,
        "nombre": alumno.nombre,
        "facultad": None,  # como no existe relación
    }
    return jsonify(data)
