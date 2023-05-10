import os
from flask import redirect, render_template, request, flash, session, url_for
from flask_lista_deseos_dojo import app
from flask_bcrypt import Bcrypt
from flask_lista_deseos_dojo.models.usuarios import Usuario
from flask_lista_deseos_dojo.models.items import Item
from flask_lista_deseos_dojo.models.deseos import Deseo
from datetime import datetime, timedelta

bcrypt = Bcrypt(app)

@app.route("/")
def index():

    if 'usuario' not in session:
        flash('Primero tienes que logearte', 'error')
        return redirect('/login')

    nombre_sistema = os.environ.get("NOMBRE_SISTEMA")

    datos_mis_items = []

    if 'idusuario' in session:
         data = {"id_usuario":int(session['idusuario'])}
         datos_mis_items = Item.get_all_mis_items(data)
         datos_otros_items = Item.get_all_otros_items(data)
         
         print(datos_otros_items,flush=True)

    return render_template("main.html", sistema=nombre_sistema, mis_items = datos_mis_items, otros_items = datos_otros_items)

@app.route("/login")
def login():

    if 'usuario' in session:
        flash('Ya estás LOGEADO!', 'warning')
        return redirect('/')

    #send now to login as start
    fecha_str = (datetime.today()).strftime("%Y-%m-%d")

    return render_template("login.html",fecha=fecha_str)

@app.route("/procesar_registro", methods=["POST"])
def procesar_registro():

    # fecha = request.form['fecha_contratacion_reg']
    
    date_format = '%Y-%m-%d %H:%M:%S'

    # if type(request.form['fecha_contratacion_reg']) is not str:
    fecha = datetime.strptime(request.form['fecha_contratacion_reg'] + " 00:00:00",date_format)

    print(fecha,flush=True)


    data_valid = {
        'user' : request.form['user'],
        'name' : request.form['name'],
        'last_name' : request.form['lastname'],
        'email' : request.form['email'],
        'password_reg' : request.form['password_reg'],
        'cpassword_reg' : request.form['cpassword_reg'],
        'fecha_contratacion':fecha
    }

    validar = Usuario.validar(data_valid)


    if not validar:
        return redirect('/login')

    pass_hash = bcrypt.generate_password_hash(request.form['password_reg'])

    data = {
        'usuario' : request.form['user'],
        'nombre' : request.form['name'],
        'apellido' : request.form['lastname'],
        'email' : request.form['email'],
        'password' : pass_hash,
        'fecha_contratacion':fecha
    }


    resultado = Usuario.save(data)

    if not resultado:
        flash("error al crear el usuario", "error")
        return redirect("/login")

    flash("Usuario creado correctamente", "success")
    return redirect("/login")


@app.route("/procesar_login", methods=["POST"])
def procesar_login():

    usuario = Usuario.buscar(request.form['identification'])

    if not usuario:
        flash("Usuario/Correo/Clave Invalidas", "error")
        return redirect("/login")

    if not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("Usuario/Correo/Clave Invalidas", "error")
        return redirect("/login")

    session['idusuario'] = usuario.id
    session['usuario'] = usuario.nombre + " " + usuario.apellido


    return redirect('/')

@app.route('/logout')
def logout():
    print("log out!")
    session.clear()
    return redirect('/login')