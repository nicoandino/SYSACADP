import os, sys
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