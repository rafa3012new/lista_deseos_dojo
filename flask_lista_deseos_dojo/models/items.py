import os
from flask import flash
from flask_lista_deseos_dojo.config.mysqlconnection import connectToMySQL
from flask_lista_deseos_dojo.models import modelo_base
from flask_lista_deseos_dojo.models import usuarios
from flask_lista_deseos_dojo.models import deseos
from flask_lista_deseos_dojo.utils.regex import REGEX_CORREO_VALIDO
from datetime import datetime


class Item(modelo_base.ModeloBase):

    modelo = 'items'
    campos = ['nombre', 'creador']

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.creador= data['creador']
        self.nombre_creador = data['nombre_creador'] 
        self.nombre_usuario_que_desea = data['nombre_usuario_que_desea'] 
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.deseos = []


    #si da tiempo
    @classmethod
    def buscar(cls, dato):
        query = "select * from items where id = %(dato)s"
        data = { 'dato' : dato }
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)

        if len(results) < 1:
            return False
        return cls(results[0])


    #si da tiempo
    @classmethod
    def update(cls,data):
        query = 'UPDATE items SET nombre = %(nombre)s WHERE id = %(id)s;'
        resultado = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)
        return resultado


    @staticmethod
    def validar_largo(data, campo, largo):
        is_valid = True
        if len(data[campo]) <= largo:
            flash(f'El largo del campo {campo} no puede ser menor o igual a {largo}', 'error')
            is_valid = False
        return is_valid

    @classmethod
    def validar(cls, data):


        is_valid = True
        #se crea una variable no_create para evitar la sobre escritura de la variable is_valid
        #pero a la vez se vean todos los errores al crear el usuario
        #y no tener que hacer un return por cada error
        no_create = is_valid


        if 'nombre' in data:
            is_valid = cls.validar_largo(data, 'nombre', 3)
            if is_valid == False: no_create = False

        return no_create


    @classmethod
    def get_all_mis_items(cls,data):

        # print(data,flush=True)
        
        #SE ARMA LA CONSULTA
        query = "select *, CONCAT(uc.nombre, ' ', uc.apellido) as nombre_creador, CONCAT(ud.nombre, ' ', ud.apellido) as nombre_usuario_que_desea from items i left join deseos d on i.id = d.id_item left join usuarios uc on i.creador = uc.id left join usuarios ud on d.id_usuario = ud.id where d.id_usuario = %(id_usuario)s;"

        # print(query,flush=True)

        #SE EJECUTA LA CONSULTAs
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query,data)
        
        # print("all ",results, flush=True)

        #SE CONVIERTE EN OBJETO PYTHON TODA LA CONSULTA
        items = []
        if results:
            for result in results:
                items.append(cls(result))

        return items
 

    @classmethod
    def get_all_otros_items(cls,data):


        #SE ARMA LA CONSULTA
        query = "select *, CONCAT(uc.nombre, ' ', uc.apellido) as nombre_creador, CONCAT(ud.nombre, ' ', ud.apellido) as nombre_usuario_que_desea  from items i left join deseos d on i.id = d.id_item left join usuarios uc on i.creador = uc.id left join usuarios ud on d.id_usuario = ud.id where i.id not in (select id_item from deseos where id_usuario = %(id_usuario)s) group by i.id;"


        #SE EJECUTA LA CONSULTA
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)


        #SE CONVIERTE EN OBJETO PYTHON TODA LA CONSULTA
        items = []
        if results:
            for result in results:
                items.append(cls(result))

        return items


    @classmethod
    def get_item_con_usuarios(cls,data):
        #SE ARMA LA CONSULTA
        query = "select *, CONCAT(uc.nombre,\" \", uc.apellido) as nombre_creador, ('') as nombre_usuario_que_desea from items i left join usuarios uc on i.creador = uc.id where i.id =  %(id_item)s;"

        print("query items ",query,flush=True)


        #SE EJECUTA LA CONSULTA
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query,data)

        # print("query items ",results,flush=True)

        resultado = results[0]



        #SE CONVIERTE EN OBJETO PYTHON TODA LA CONSULTA
        item = cls(resultado)


        #SE ARMA LA CONSULTA del 1 a MUCHOS
        query1 = "select *, CONCAT(ud.nombre, \" \", ud.apellido) as nombre_usuario from deseos d left join usuarios ud on d.id_usuario = ud.id where d.id_item = %(id_item)s and d.id_usuario <> %(id_usuario)s;"


        #SE EJECUTA LA CONSULTA
        results1 = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query1, data)


        if results1:
             for result1 in results1:

                deseos_data = {
                      "id_item" : result1["id_item"],
                      "id_usuario" : result1["id_usuario"],
                      "nombre_usuario": result1["nombre_usuario"],
                      "created_at": result1["created_at"],
                      "updated_at": result1["updated_at"]
                }

                item.deseos.append(deseos.Deseo(deseos_data))


        return item