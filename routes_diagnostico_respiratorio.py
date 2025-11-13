from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import re
from se_diagnostico_respiratorio import EvaluacionClinica
from complementos_funcionalidades import orden_claves

app_dcr = Flask(__name__)
app_dcr.secret_key = 'super_clave_secreta_caroline_nelson_roberto'


@app_dcr.context_processor
def inject_user():
    return dict(nombre_usuario=session.get('username'))


def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            #flash("Para acceder a esta página debes iniciar sesión", "error")
            return redirect(url_for("iniciar_sesion"))
        return f(*args, **kwargs)
    return decorated_function


@app_dcr.route('/')
def inicio():
    return redirect(url_for('iniciar_sesion'))


@app_dcr.route('/iniciar-sesión', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        usuarios = {
            'Roberto': 'islascaiman',
            'Caroline': 'rioateña',
            'Nelson': 'enfermero',
            'Invitado': 'univdepanama'
        }

        usuario = request.form["username"]
        contrasena = request.form["password"]

        if usuario in usuarios and usuarios[usuario] == contrasena:
            session["username"] = usuario
            return redirect(url_for('sistema_experto'))

    return render_template('login.html')


@app_dcr.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("resultados", None)
    session.pop("datos_medicos", None)
    session.pop("datos_titulos", None)
    return redirect(url_for("iniciar_sesion"))


@app_dcr.route('/sistema-experto-diagnostico-clinico-respiratorio', methods=['GET', 'POST'])
@login_requerido
def sistema_experto():
    if request.method == 'POST':
        formulario = request.form.to_dict()
        datos_paciente = {}
        for datos in formulario:
            if re.match(r"^-?\d+$", formulario[datos]):
                datos_paciente[datos] = int(formulario[datos])
            elif re.match(r'^-?\d*\.?\d+(e[-+]?\d+)?$', formulario[datos]):
                datos_paciente[datos] = float(formulario[datos])
            else:
                datos_paciente[datos] = formulario[datos]

        diagnostico = EvaluacionClinica()
        resultados, datos_medicos, datos_titulos = diagnostico.ejecutar_reglas(datos_paciente)
        session['resultados'] = resultados
        session['datos_medicos'] = datos_medicos
        session['datos_titulos'] = datos_titulos

        return redirect(url_for('resultado_evaluacion'))
    return render_template('sistema_experto_dcr.html')


@app_dcr.route('/diagnostico', methods=['GET', 'POST'])
@login_requerido
def resultado_evaluacion():
    resultados = session.get('resultados', None)
    datos_recibidos = session.get('datos_medicos', None)
    titulos_recibidos = session.get('datos_titulos', None)

    datos = {clave: datos_recibidos[clave] for clave in orden_claves if clave in datos_recibidos}
    titulos_datos = {clave: titulos_recibidos[clave] for clave in orden_claves if clave in titulos_recibidos}

    datos_paciente = zip(titulos_datos.items(), datos.items())

    return render_template('resultado_sistema_experto.html',
                           resultados=resultados, datos_paciente=datos_paciente)
