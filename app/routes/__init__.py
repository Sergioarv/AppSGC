from app import app, db
from flask import Flask, request, render_template, session, flash, redirect
from app.schemas.models import *
from datetime import timedelta
from base64 import b64encode
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

#Tiempo de Session
app.permanent_session_lifetime = timedelta(minutes=30)

#Administrador Principal
def adminF():
    oAdmin = Admin.query.filter_by(email = 'sarv9208@gmail.com').first()
    if oAdmin is None:
        oAdmin = Admin(name = 'Administrador', email = 'sarv9208@gmail.com', password = '920812')
        db.session.add(oAdmin)
        db.session.commit()
    else:
        pass

#Filtrar Session
def filtroS():
    if 'admin' in session:
        return True
    else:
        False

#Ruta principal
@app.route('/', methods = ['GET'])
def index():
    adminF()
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
    if filtroS():
        return redirect('/')
    else:
        if request.method == 'POST':
            user = request.form['emailC']
            password = request.form['passwordC']
            oAdmin = Admin.query.filter_by(email = user, password = password).first()
            if oAdmin:  
                session.permanent = True
                session['admin'] = oAdmin.name
                flash('Bienvenido '+str(oAdmin.name), 'success')
                return redirect('/')
            else:
                flash('El correo o la contraseña no coinciden', 'danger')
                return render_template('/login.html')
        else:
            return render_template('/login.html')

#Realizar Login out
@app.route('/login_out')
def login_out():
    if filtroS():
        session.pop("admin", None)
    return redirect('/login')

#Ruta de Recuperacion de Cuenta
@app.route('/recovery', methods = ["GET", "POST"])
def recovery():
    if filtroS():
        return redirect('/')
    else:
        if request.method == 'POST':
            email = request.form['emailC']
            oAdmin = Admin.query.filter_by(email = email).first()
            if oAdmin is None:
                flash('El correo no existe, verifique','danger')
                return render_template('/recovery.html')
            else:
                enviarMensaje(oAdmin, 2)
                flash('Se le ha enviado la contraseña al correo','success')
                return render_template('/home.html')
        else:
            return render_template('/recovery.html')  

#verificar tipos de imagenes
#Verificar formatos permitidos de imagen
ALLOWED_EXTENDSIONS = set (["png","PNG","jpge","JPEG","jpg","JPG","gif","GIF", "svg", "SVG"])
def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1] in ALLOWED_EXTENDSIONS

#Enviar Mensajes
def enviarMensaje(data, opc):
    msg = MIMEMultipart()
    password = 'nxmgrqskcwbticku'
    msg['From'] = 'sarv9208@gmail.com'
    msg['To'] = data.email
    if opc == 1:
        message = """Señor %s %s su solicitud se encuentra en espera, le responderemos en breve.
    Por favor no contestar este mensaje""" %(data.name, data.address)
        msg['Subject'] = "Solicitud"
        msg.attach(MIMEText(message, 'plain'))
    elif opc == 2:
        message = """%s su contraseña es %s""" %(data.name, data.password)
        msg['Subject'] = "Recuperar cuenta"
        msg.attach(MIMEText(message, 'plain'))
    else:
        print ('Ultimo Caso')
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()