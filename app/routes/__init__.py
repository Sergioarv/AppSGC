from flask import render_template, redirect, request, url_for, send_from_directory, flash, abort
from app import app, db
from app.schemas.flyer import Flyer
import os

#ruta estatica de imagenes
UPLOAD_FOLDER = os.path.abspath("./app/static/img/")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#formatos permitidos de imagen
ALLOWED_EXTENDSIONS = set (["png","jpge","jpg","gif"])

#Ruta principal
@app.route('/', methods = ['GET'])
def index():
    flyers = Flyer.query.all()
    return render_template("home.html", listFlyer = flyers)

#Ruta alternativa
@app.route('/about')
def about():
    return render_template("about.html")

#Ruta de index Flyer
@app.route('/flyer')
def flyer_index():
    flyers = Flyer.query.all()
    return render_template('/flyer/flyer_index.html', listFlyer = flyers)

#verificar tipos de imagenes
def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1] in ALLOWED_EXTENDSIONS

#Verifica datos vacios
def validar(lst, datos):
    errores = []
    for l in range(len(lst)):
        if lst[l] == "":
            errores.append("Debe ingresar "+str(datos[l]))
    return errores

#ruta para crear un flyer
@app.route('/flyer/create', methods=["GET", "POST"])
def flyer_create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        f = request.files['archivo']
        lista = [nombre, descripcion, f.filename]
        datos = ['nombre', 'descripcion', 'imagen']
        errores = validar(lista, datos)
        if len(errores) == 0:
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
        for e in errores:
            flash (e,'danger')
        return redirect(url_for('flyer_create'))
    #retorno a templates Create Flyer
    else:
        return render_template('/flyer/create.html')

#Ruta para eliminar un Flyer
@app.route('/flyer/delete/<string:id>')
def flyer_delete(id):
    oFlyer = Flyer.query.filter_by(id = id).first()
    #os.remove(os.path.join(app.config['UPLOAD_FOLDER'], oFlyer.imagen))
    db.session.delete(oFlyer)
    db.session.commit()
    flash('Se elimino exitosamente')
    return redirect('/flyer')

#Ruta para editar un Flyer
@app.route('/flyer/edit/<string:id>', methods=["GET", "POST"])
def flyer_edit(id):
    #se accede a base de base de datos
    if request.method == 'POST':
        oFlyer = Flyer.query.filter_by(id = id).first()
        nombre = request.form['name']
        descripcion = request.form['description']
        f = request.files['fileImagen']
        #Si hay una imagen se actualiza
        if f != '':
            filename = f.filename
            #Verifica que tengo un nombre y extension valida la imagen
            if f and allowed_file(filename):
                #f.remove(app.root_path+'/static/img/'+filename))
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                img = filename
                oFlyer.imagen =  img
                db.session.commit()
            else:
                flash('Selecione una imagen', 'danger')
        #Se actualiza nombre y descripcion
        oFlyer.name = nombre
        db.session.commit()
        oFlyer.description = descripcion
        db.session.commit()
        flash('Modifico con exito', 'success')
        return redirect('/flyer')
    oFlyer = Flyer.query.filter_by(id = id).first()
    return render_template('/flyer/flyer_edit.html', myFlyer = oFlyer)

#detalles del flyer
@app.route('/flyer/detail/<string:id>')
def flyer_detail(id):
    oFlyer = Flyer.query.filter_by(id = id).first()
    return render_template('/flyer/flyer_detail.html', myFlyer = oFlyer)

# Rutas de Solicitud
@app.route('/request/create/<string:id>', methods=["GET", "POST"])
def request_create(id):
    if request.method == 'POST':
        name = request.form['nameC']
        address = request.form['addressC']
        email = request.form['emailC']
        phone = request.form['phoneC']
        destino = request.form['destinoC']
        origin = request.form['originC']
        return redirect('/')
    else:
        oFlyer = Flyer.query.filter_by(id = id).first()
        return render_template('request_create.html', myFlyer = oFlyer)
