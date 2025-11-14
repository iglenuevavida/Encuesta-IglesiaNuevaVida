from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

app = Flask(__name__)
app.secret_key = "cambiame_por_una_secreta"

# --- Configuración de base de datos principal ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///miembros.db'
db = SQLAlchemy(app)

# --- MODELO SQLALCHEMY ---
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(100))
    edad = db.Column(db.Integer)
    telefono = db.Column(db.String(50))
    tiempo_asiste = db.Column(db.String(100))
    ministerio = db.Column(db.String(100))
    lider = db.Column(db.String(100))
    bautizado = db.Column(db.String(10))
    estudio = db.Column(db.String(50))

with app.app_context():
    db.create_all()

# --- RUTA PRINCIPAL ---
@app.route('/')
def index():
    return render_template('index.html')

# --- LOGIN DE PASTOR ---
@app.route('/pastor_login', methods=['GET', 'POST'])
def pastor_login():
    if request.method == 'POST':
        usuario = request.form['usuario'].strip()
        contraseña = request.form['contraseña'].strip()

        # Permitir que cualquier pastor/líder con contraseña INV1987 ingrese
        if contraseña == "INV1987" and usuario:
            # Guardamos el nombre ingresado para mostrarlo luego si querés
            flash(f"Bienvenido {usuario}", "success")
            return redirect(url_for('members_table'))
        else:
            flash("Nombre o contraseña incorrectos.", "danger")
            return render_template('pastor_login.html')

    return render_template('pastor_login.html')

# --- TABLA DE MIEMBROS (panel de pastores) ---
@app.route('/member_table')
def members_table():
    miembros = Member.query.all()
    return render_template('member_table.html', miembros=miembros)

# --- ENCUESTA PARA MIEMBROS ---
@app.route('/member_survey', methods=['GET', 'POST'])
def member_survey():
    if request.method == 'POST':
        nombre = request.form.get('nombre_completo', '').strip()
        edad = request.form.get('edad', '').strip()
        telefono = request.form.get('telefono', '').strip()
        tiempo_asiste = request.form.get('tiempo_asiste', '').strip()
        ministerio = request.form.get('ministerio', '').strip()
        lider = request.form.get('lider', '').strip()
        bautizado = request.form.get('bautizado', '').strip()
        estudio = request.form.get('estudio', '').strip()

        if not nombre:
            flash("Por favor ingresa tu nombre completo.", "warning")
            return redirect(url_for('member_survey'))

        nuevo_miembro = Member(
            nombre_completo=nombre,
            edad=int(edad) if edad else None,
            telefono=telefono,
            tiempo_asiste=tiempo_asiste,
            ministerio=ministerio,
            lider=lider,
            bautizado=bautizado,
            estudio=estudio
        )
        db.session.add(nuevo_miembro)
        db.session.commit()

        return redirect(url_for('gracias'))

    return render_template('member_survey.html')

# --- PÁGINA DE AGRADECIMIENTO ---
@app.route('/gracias')
def gracias():
    return render_template('gracias.html')

if __name__ == "__main__":
    app.run(debug=True)