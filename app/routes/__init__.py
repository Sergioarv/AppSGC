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
    return render_template("home.html")

#Ruta alternativa
@app.route('/about')
def about():
    return render_template("about.html")

#Templates de Flyers

#Ruta de index Flyer
@app.route('/flyer')
def flyer_index():
    flyers = Flyer.query.all()
    return render_template('flyer_index.html', listFlyer = flyers)

#verificar tipos de imagenes
def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1] in ALLOWED_EXTENDSIONS

#ruta para crear un flyer
@app.route('/flyer/create', methods=["GET", "POST"])
def flyer_create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        f = request.files['archivo']
        if f and allowed_file(f.filename):
            img = f.filename
            #f.save(os.path.join(app.config['UPLOAD_FOLDER'], img))
            oFlyer = Flyer(name = nombre, description = descripcion, imagen = img)
            db.session.add(oFlyer)
            db.session.commit()
            flash("Se a agregado un Flyer")
            return redirect(url_for('flyer_index'))
        else:
            flash("No selecciono una imagen o no es una imagen")
            return redirect(url_for('flyer_create'))
    #retorno a templates Create Flyer
    else:
        return render_template('flyer_create.html')

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
                #os.remove(os.path.join(app.config['UPLOAD_FOLDER'], oFlyer.imagen))
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                img = filename
                oFlyer.imagen =  img
                db.session.commit()
        #Se actualiza nombre y descripcion
        oFlyer.name = nombre
        db.session.commit()
        oFlyer.description = descripcion
        db.session.commit()
        flash('Modifico con exito')
        return redirect('/flyer')
    oFlyer = Flyer.query.filter_by(id = id).first()
    return render_template('flyer_edit.html', myFlyer = oFlyer)