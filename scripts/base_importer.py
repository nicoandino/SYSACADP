import os
import sys
from xml.etree import ElementTree as ET
from sqlalchemy.exc import IntegrityError
from app import create_app, db

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


class BaseImporter:
    def __init__(self, model, xml_relative_path, root_tag, field_map, pk_field="id"):
        self.model = model
        self.ruta_xml = os.path.join(BASE_DIR, xml_relative_path)
        self.root_tag = root_tag
        self.field_map = field_map
        self.pk_field = pk_field

    def get_text(self, elem):
        return elem.text.strip() if (elem is not None and elem.text) else None

    def run(self):import os, sys
from xml.etree import ElementTree as ET
from app import create_app, db

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

class ImportadorXML:
    def __init__(self, modelo, archivo, tag, campos, pk="id"):
        self.modelo = modelo
        self.archivo = os.path.join(BASE_DIR, archivo)
        self.tag = tag
        self.campos = campos
        self.pk = pk

    def texto(self, elem):
        return elem.text.strip() if elem is not None and elem.text else None

    def correr(self):
        app = create_app()
        with app.app_context():
            db.create_all() 

            if not os.path.exists(self.archivo):
                print("No se encontró el archivo:", self.archivo)
                return

            root = ET.parse(self.archivo).getroot()
            ins, dup = 0, 0  
            for item in root.findall(self.tag):
                datos = {k: self.texto(item.find(v)) for k, v in self.campos.items()}
                clave = int(datos[self.pk])  
                if self.modelo.query.get(clave):
                    dup += 1
                    continue

                db.session.add(self.modelo(**datos))
                db.session.commit()
                ins += 1

            print(f"Listo. Insertados:{ins}, Duplicados:{dup}")
        app = create_app()
        with app.app_context():
            db.create_all()
            if not os.path.exists(self.xml_path):
                print(f"ERROR: No se encontró el archivo XML: {self.xml_path}")
                return
            print(f"Importando desde: {self.xml_path}")
            tree = ET.parse(self.xml_path)
            root = tree.getroot()



            for item in root.findall(self.root_tag):
                try:
                    data = {}
                    for field, tag in self.field_map.items():
                        data[field] = self.get_text(item.find(tag))

                    # PK debe ser int
                    pk_value = int(data[self.pk_field])

                    # Evitar duplicados
                    if self.model.query.get(pk_value):
                        print(f"Duplicado {self.pk_field}={pk_value}")
                        duplicados += 1
                        continue

                    # Construir instancia
                    obj = self.model(**data)
                    db.session.add(obj)
                    db.session.commit()
                    insertados += 1

                except (ValueError, IntegrityError) as e:
                    db.session.rollback()
                    print(f"Error en registro: {e}")
                    errores += 1
                except Exception as e:
                    db.session.rollback()
                    print(f"Error inesperado: {e}")
                    errores += 1

            print(f"""
Importación finalizada:
- Insertados: {insertados}
- Duplicados: {duplicados}
- Errores: {errores}
""")
