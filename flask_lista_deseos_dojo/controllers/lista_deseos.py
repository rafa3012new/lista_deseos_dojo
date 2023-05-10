import os
from flask import redirect, render_template, request, flash, session, url_for, Blueprint
from flask_lista_deseos_dojo import app
from flask_bcrypt import Bcrypt
from flask_lista_deseos_dojo.models.usuarios import Usuario
from flask_lista_deseos_dojo.models.items import Item
from flask_lista_deseos_dojo.models.deseos import Deseo
from datetime import datetime, timedelta

lista_deseos = Blueprint('lista_deseos', __name__)

bcrypt = Bcrypt(app)


@lista_deseos.route("/crearitem")
def crearitem():

    if 'usuario' not in session:
        flash('Primero tienes que logearte', 'error')
        return redirect('/login')

    operacion = "Nuevo Item"


    if 'rollback_nombre' in session:
        data = {
        'id':'',
        'nombre':session['rollback_nombre'],
        }
        session.pop('rollback_nombre')
    else:
        data = {
        'id':'',
        'nombre':'',
        }

    nombre_sistema = os.environ.get("NOMBRE_SISTEMA")

    return render_template('form.html',operacion=operacion,datos_item=data)




@lista_deseos.route("/procesar_item", methods=["POST"])
def procesar_item():


    data ={
            'nombre':request.form['nombre'],
            'creador':session['idusuario']
           }



    validar = Item.validar(data)



    if not validar:
        if request.form['operacion'] == 'Nuevo Item':
            session['rollback_nombre'] = request.form['nombre']
            return redirect('/lista_deseos/crearitem')

    try:
        if request.form['operacion'] == 'Nuevo Item':

            id_item = Item.save(data)
            print("id item guardado ", id_item,flush=True)

            data2={
            'id_usuario':int(session['idusuario']),
            'id_item':int(id_item)
            }

            Deseo.save(data2)
    
        flash("item almacenado con exito!","success")
        print("item guardado con exito!",flush=True)
    except Exception as error:
        print(f"error al guardar el item, valor del error : {error}",flush=True)

    return redirect('/')


@lista_deseos.route("/agregar_item_deseos/<id>")
def agregar_item_deseos(id):

    data={
       'id_usuario':int(session['idusuario']),
       'id_item':int(id)
         }

    Deseo.save(data)

    return redirect('/')


@lista_deseos.route("/quitar_item_deseos/<id>")
def quitar_item_deseos(id):

    data={
       'id_usuario':int(session['idusuario']),
       'id_item':int(id)
         }

    Deseo.delete_item(data)

    return redirect('/')


@lista_deseos.route("/eliminaritem/<id>")
def eliminaritem(id):

    try:
        Item.delete(int(id))
        flash('Se elimino el item con exito','success')
        print(f"Eliminacion de item con exito {id}",flush=True)
    except Exception as error:
        print("error al eliminar la item",flush=True)

    return redirect('/')


@lista_deseos.route("/detalle_item/<id_item>/<id_usuario>")
def detalle_item(id_item,id_usuario):

    if 'usuario' not in session:
        flash('Primero tienes que logearte', 'error')
        return redirect('/login')

    data = {"id_item":int(id_item),
            "id_usuario":int(id_usuario)
            }

    datos_item = Item.get_item_con_usuarios(data)

    nombre_sistema = os.environ.get("NOMBRE_SISTEMA")
    return render_template('detail.html',sistema=nombre_sistema, item=datos_item)


