from app import app, db
from flask import render_template, session, flash, redirect
from app.schemas.models import *
from datetime import date, datetime, timedelta
from base64 import b64encode
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

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