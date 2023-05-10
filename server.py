import flask_lista_deseos_dojo.controllers.core
from flask_lista_deseos_dojo.controllers.lista_deseos import lista_deseos

from flask_lista_deseos_dojo import app

app.register_blueprint(lista_deseos, url_prefix='/lista_deseos')


if __name__ == "__main__":
    app.run(debug=True)