from flask import render_template, redirect, request, url_for, send_from_directory, flash, session
from app import app, db
from app.schemas.models import Flyer, Request, Admin
from datetime import date, datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os, smtplib, requests, pdfkit

#ruta estatica de imagenes
UPLOAD_FOLDER = os.path.abspath("./app/static/img/")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.permanent_session_lifetime = timedelta(minutes=3)

#formatos permitidos de imagen
ALLOWED_EXTENDSIONS = set (["png","jpge","jpg","gif"])

#verificar tipos de imagenes
def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1] in ALLOWED_EXTENDSIONS

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
    return render_template("home.html", listFlyer = flyers)

#Ruta alternativa
@app.route('/about')
def about():
    return render_template("about.html")

#Rutas de Flyer
#Ruta de index Flyer
@app.route('/flyer')
def flyer_index():
    if filtroS():
        flyers = Flyer.query.all()
        return render_template('/flyer/index.html', listFlyer = flyers)
    else:
        return redirect('/login')

#Ruta para crear un flyer
@app.route('/flyer/create', methods=["GET", "POST"])
def flyer_create():
    if filtroS():
        if request.method == 'POST':
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            f = request.files['archivo']
            if f and allowed_file(f.filename):
                img = f.filename
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], img))
                oFlyer = Flyer(name = nombre, description = descripcion, imagen = img)
                db.session.add(oFlyer)
                db.session.commit()
                flash("Se a agregado un Flyer", "success")
                return redirect(url_for('flyer_index'))
            else:
                flash("No selecciono una imagen o no es una imagen",'danger')
                return redirect(url_for('flyer_create'))
        #retorno a templates Create Flyer
        else:
            return render_template('/flyer/create.html')
    else:
        return redirect('/login')

#Ruta para eliminar un Flyer
@app.route('/flyer/delete/<string:id>')
def flyer_delete(id):
    if filtroS():
        oFlyer = Flyer.query.filter_by(id = id).first()
        db.session.delete(oFlyer)
        db.session.commit()
        flash('Se elimino exitosamente','success')
        return redirect('/flyer')
    else:
        return redirect('/login')

#Ruta para editar un Flyer
@app.route('/flyer/edit/<string:id>', methods=["GET", "POST"])
def flyer_edit(id):
    if filtroS():
        #se accede a base de base de datos
        if request.method == 'POST':
            oFlyer = Flyer.query.filter_by(id = id).first()
            nombre = request.form['name']
            descripcion = request.form['description']
            f = request.files['fileImagen']
            filename = f.filename
            print (filename)
            #Si hay una imagen se actualiza
            if filename:
                #Verifica que tengo un nombre y extension valida la imagen
                if f and allowed_file(filename):
                    #f.remove(app.root_path+'/static/img/'+filename))
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    img = filename
                    oFlyer.imagen =  img
                    db.session.commit()
                else:
                    flash('No selecciono una imagen o no es una imagen', 'danger')
                    return render_template('/flyer/edit.html', myFlyer = oFlyer)
            #Se actualiza nombre y descripcion
            oFlyer.name = nombre
            db.session.commit()
            oFlyer.description = descripcion
            db.session.commit()
            flash('Modifico con exito', 'success')
            return redirect('/flyer')
        else:
            oFlyer = Flyer.query.filter_by(id = id).first()
            return render_template('/flyer/edit.html', myFlyer = oFlyer)
    else:
        return redirect('/login')

#detalles del flyer
@app.route('/flyer/detail/<string:id>')
def flyer_detail(id):
    oFlyer = Flyer.query.filter_by(id = id).first()
    return render_template('/flyer/detail.html', myFlyer = oFlyer)

# Rutas de Solicitud
# Crear Solicitud
@app.route('/request/create/<string:id>', methods=["GET", "POST"])
def request_create(id):
    if request.method == 'POST':
        name = request.form['nameC']
        address = request.form['addressC']
        email = request.form['emailC']
        phone = request.form['phoneC']
        destino = request.form['destinoC']
        origin = request.form['originC']
        description = request.form['descriptionC']
        fecha = datetime.now()
        dateI = ''+fecha.strftime("%d-%m-%Y")
        state = 'Solicitado'
        oRequest = Request(name = name, address = address, email = email, phone = phone, destino = destino, origin = origin, description = description, dateI = dateI, state = state)
        db.session.add(oRequest)
        db.session.commit()
        enviarMensaje(oRequest)
        flash ('Su solicitud esta en espera', 'success')
        return redirect('/')
    else:
        oFlyer = Flyer.query.filter_by(id = id).first()
        return render_template('/request/create.html', myFlyer = oFlyer)

#Ruta Index solicitudes
@app.route('/request')
def request_index():
    if filtroS():
        requests = Request.query.filter_by(state = 'Solicitado').all()
        return render_template('/request/index.html', listRequest = requests)
    else:
        return redirect('/login')

#Ruta responder solicitudes
@app.route('/request/answer/<string:id>', methods=["GET", "POST"])
def request_answer(id):
    if filtroS():
        if request.method == 'POST':
            para = request.form["inputTo"]
            name = request.form["nameC"]
            city = request.form["city"]
            asunto = request.form["asunto"]
            value = request.form["value"]
            date = datetime.now().utcnow().strftime("%d de %m del %Y")
            itemA = request.form['itemA']
            itemR = request.form['itemR']
            html = render_template('/quotation/quotation.html', date = date, para = para, name = name, city = city, asunto = asunto, value = value, itemA = itemA, itemR = itemR)
            option = {
                'page-size': 'Letter',
                'encoding': 'UTF-8',
                'margin-top': '0.25in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
            }
            pdfkit.from_string(html, 'Cotizacion'+str(name)+'.pdf', options=option)
            return redirect('/')
        else:
            date = datetime.now().utcnow().strftime("%d de %B del %Y")
            oRequest = Request.query.filter_by(id = id).first()
            return render_template('/request/answer.html', myRequest = oRequest, date = date)
    else:
        return redirect('/login')

#Ruta responder Cotizacion
@app.route('/quotation')
def quotation():
    return redirect('/')

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
                flash('Bienvenido'+str(oAdmin.name), 'success')
                return redirect('/')
            else:
                flash('El correo o la contraseña no coinciden', 'danger')
                return render_template('/login.html')
        else:
            return render_template('/login.html')

@app.route('/login_out')
def login_out():
    if filtroS():
        session.pop("admin", None)
    return redirect('/login')

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
                recoveryPass(oAdmin)
                flash('Se le ha enviado la contraseña al correo','success')
                return render_template('/home.html')
        else:
            return render_template('/recovery.html')

def recoveryPass(oAdmin):
    msg = MIMEMultipart()
    message = """%s su contraseña es %s""" %(oAdmin.name, oAdmin.password)
    password = 'nxmgrqskcwbticku'
    msg['From'] = 'sarv9208@gmail.com'
    msg['To'] = oAdmin.email
    msg['Subject'] = "Recuperar cuenta"
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    print ("successfully sent email to %s:" %(msg['To']))    

def enviarMensaje(oRequest):
    msg = MIMEMultipart()
    message = """Señor %s %s su solicitud se encuentra en espera, le responderemos en breve.
Por favor no contestar este mensaje""" %(oRequest.name, oRequest.address)
    password = 'nxmgrqskcwbticku'
    msg['From'] = 'sarv9208@gmail.com'
    msg['To'] = oRequest.email
    msg['Subject'] = "Solicitud"
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    print ("successfully sent email to %s:" %(msg['To']))