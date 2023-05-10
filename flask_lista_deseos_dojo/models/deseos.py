import os
from flask import flash
from flask_lista_deseos_dojo.config.mysqlconnection import connectToMySQL
from flask_lista_deseos_dojo.models import modelo_base
from flask_lista_deseos_dojo.models import usuarios
from flask_lista_deseos_dojo.utils.regex import REGEX_CORREO_VALIDO
from datetime import datetime


class Deseo(modelo_base.ModeloBase):

    modelo = 'deseos'
    campos = ['id_item', 'id_usuario']

    def __init__(self, data):
        self.id_item = data['id_item']
        self.id_usuario = data['id_usuario']
        self.nombre_usuario = data['nombre_usuario']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def delete_item(cls,data):

        query = 'DELETE FROM deseos WHERE id_item = %(id_item)s and id_usuario = %(id_usuario)s'

        resultado = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)

        print("RESULTADO: ", resultado,flush=True)

        return resultado