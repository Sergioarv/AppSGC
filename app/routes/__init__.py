from app import app, db, email_emp, password_emp
from flask import Flask, request, render_template, session, flash, redirect, url_for
from app.schemas.models import Flyer, Admin, Quotation, Request, Constraint, Question, Survey
from datetime import timedelta
from base64 import b64encode
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

#Tiempo de Session
app.permanent_session_lifetime = timedelta(minutes=30)

#Administrador Principal
def admin_f():
    obj_admin = Admin.query.filter_by(email = email_emp).first()
    if obj_admin is None:
        obj_admin = Admin(name = 'Administrador', email = email_emp, password = '920812')
        db.session.add(obj_admin)
        db.session.commit()

#Filtrar Session
def authentication():
    if 'admin' in session:
        return True
    else:
        False

#Ruta principal
@app.route('/', methods = ['GET'])
def index():
    admin_f()
    flyers = Flyer.query.all()
    for f in flyers:
        f.imagen = b64encode(f.imagen).decode("utf-8")
    return render_template("home.html", listFlyer = flyers)

#Ruta contactos
@app.route('/contact')
def contact():
    return render_template("/about/contact.html")

#Ruta Quienes Somos
@app.route('/company')
def company():
    return render_template("/about/company.html")

#Ruta de Mision y Vision
@app.route('/mission_vision')
def mission_vision():
    return render_template("/about/mission_vision.html")

#Ruta de Valores
@app.route('/values')
def values():
    return render_template("/about/values.html")

#Realizar login
@app.route('/login', methods=["GET","POST"])
def login_in():
    if authentication():
        return redirect('/')
    else:
        if request.method == 'POST':
            user = request.form['emailC']
            password = request.form['passwordC']
            obj_admin = Admin.query.filter_by(email = user, password = password).first()
            if obj_admin:  
                session.permanent = True
                session['admin'] = obj_admin.name
                flash('Bienvenido '+str(obj_admin.name), 'success')
                return redirect('/')
            else:
                flash('El correo o la contraseña no coinciden', 'danger')
                return render_template('/login.html')
        else:
            return render_template('/login.html')

#Realizar Login out
@app.route('/login_out')
def login_out():
    if authentication():
        session.pop("admin", None)
    return redirect('/login')

#Ruta de Recuperacion de Cuenta
@app.route('/recovery', methods = ["GET", "POST"])
def recovery():
    if authentication():
        return redirect('/')
    else:
        if request.method == 'POST':
            email = request.form['emailC']
            obj_admin = Admin.query.filter_by(email = email).first()
            if obj_admin is None:
                flash('El correo no existe, verifique','danger')
                return render_template('/recovery.html')
            else:
                enviar_mensaje(obj_admin, 3)
                flash('Se le ha enviado la contraseña al correo','success')
                return render_template('/home.html')
        else:
            return render_template('/recovery.html')  

@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html'), 404

#verificar tipos de imagenes
#Verificar formatos permitidos de imagen
ALLOWED_EXTENDSIONS = set (["png","PNG","jpge","JPEG","jpg","JPG","gif","GIF", "svg", "SVG"])
def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1] in ALLOWED_EXTENDSIONS

#Enviar Mensajes
def enviar_mensaje(data, opc):
    msg = MIMEMultipart()
    password = password_emp
    msg['From'] = email_emp
    msg['To'] = data.email
    if opc == 1:
        message = """Señor %s %s su solicitud ha sido recibida, responderemos a ella a la mayor brevedad.
    Por favor no contestar este mensaje.
    Generado automaticamente""" %(data.name, data.address)
        msg['Subject'] = "Solicitud"
        msg.attach(MIMEText(message, 'plain'))
        data.email = email_emp
        enviar_mensaje(data, 2)
    elif opc == 2:
        message = """El señor %s %s ha solicitado una cotizacion, por favor dar pronta respuesta al usuario""" %(data.name, data.address)
        msg['Subject'] = "Nueva Solicitud"
        msg.attach(MIMEText(message, 'plain'))
    elif opc == 3:
        message = """%s su contraseña es %s""" %(data.name, data.password)
        msg['Subject'] = "Recuperar cuenta"
        msg.attach(MIMEText(message, 'plain'))
    elif opc == 4:
        obj_q = db.session.query(Quotation.id).filter(Quotation.request_id == data.id).first()
        message = """En La Casa Del Turismo queremos conocer como fue tu experiencia, ayududanos respondiendo estas preguntas.
        <a href='https://appsgc.herokuapp.com/survey/quality/%s'>Encuesta de Satisfaccion</a>""" %(obj_q)
        msg['Subject'] = "Cuentanos como te fue"
        msg.attach(MIMEText(message, 'html'))
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()