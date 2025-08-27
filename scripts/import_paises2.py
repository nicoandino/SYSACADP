# scripts/importar_paises.py
import os
import sys
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.models.pais import Pais
from scripts.base_importer import ImportadorXML

def importar_paises():
    importer = ImportadorXML(
        modelo=Pais,
        archivo ="archivados_xml/paises.xml",
        tag="_expxml",
        campos ={
            "id": "pais",
            "nombre": "nombre"
        },
        pk ="id"
    )
    importer.correr()


if __name__ == "__main__":
    importar_paises()
