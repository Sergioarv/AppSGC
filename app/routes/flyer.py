from app import app
from app.routes import *
from flask import request
from PIL import Image

#Rutas de Flyer
#Ruta de index Flyer
@app.route('/flyer')
def flyer_index():
    if authentication():
        flyers = Flyer.query.all()
        for f in flyers:
            f.imagen = b64encode(f.imagen).decode("utf-8")
        return render_template('/flyer/index.html', listFlyer = flyers)
    else:
        return redirect(url_for('login_in'))

#Ruta para crear un flyer
@app.route('/flyer/create', methods=["GET", "POST"])
def flyer_create():
    if authentication():
        if request.method == 'POST':
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            f = request.files['archivo']
            img = f.read()
            if len(img) < 100000 or len(img) > 2000000:
                flash("Se le recomienda usar imagenes entre 100Kb y 2Mb de peso",'info')
                return redirect('/flyer/create')
            else:
                if f and allowed_file(f.filename):
                    obj_flyer = Flyer(name = nombre, description = descripcion, imagen = img)
                    db.session.add(obj_flyer)
                    db.session.commit()
                    flash("Se a agregado un Flyer", "success")
                    return redirect(url_for('flyer_index'))
                else:
                    flash("No selecciono una imagen o no es una imagen",'danger')
                    return redirect('/flyer/create')
        #retorno a templates Create Flyer
        else:
            return render_template('/flyer/create.html')
    else:
        return redirect(url_for('login_in'))

#Ruta para eliminar un Flyer
@app.route('/flyer/delete/<string:id>', methods=["GET", "POST"])
def flyer_delete(id):
    if authentication():
        if request.method == 'POST':
            obj_flyer = Flyer.query.filter_by(id = id).first()
            db.session.delete(obj_flyer)
            db.session.commit()
            flash('Se elimino exitosamente','success')
            return redirect(url_for('flyer_index'))
        else:
            obj_flyer = Flyer.query.filter_by(id = id).first()
            obj_flyer.imagen = b64encode(obj_flyer.imagen).decode("utf-8")
            return render_template('/flyer/delete.html', myFlyer = obj_flyer)
    else:
        return redirect('/login')

#Ruta para editar un Flyer
@app.route('/flyer/edit/<string:id>', methods=["GET", "POST"])
def flyer_edit(id):
    if authentication():
        #se accede a base de base de datos
        if request.method == 'POST':
            obj_flyer = Flyer.query.filter_by(id = id).first()
            nombre = request.form['name']
            descripcion = request.form['description']
            f = request.files['fileImagen']
            img = f.read()
            if f:
                if len(img) < 100000 or len(img) > 2000000:
                    flash("Se le recomienda usar imagenes entre 100Kb y 2Mb de peso",'info')
                    return redirect('/flyer/edit/'+id)
                else:
                    #Verifica que tengo un nombre y extension valida la imagen
                    if f and allowed_file(f.filename):
                        obj_flyer.imagen =  img
                        db.session.commit()
                    else:
                        flash('No selecciono una imagen o no es una imagen', 'danger')
                        return render_template('/flyer/edit.html', myFlyer = obj_flyer)
            #Se actualiza nombre y descripcion
            obj_flyer.name = nombre
            db.session.commit()
            obj_flyer.description = descripcion
            db.session.commit()
            flash('Modifico con exito', 'success')
            return redirect(url_for('flyer_index'))
        else:
            obj_flyer = Flyer.query.filter_by(id = id).first()
            return render_template('/flyer/edit.html', myFlyer = obj_flyer)
    else:
        return redirect('/login')

#detalles del flyer
@app.route('/flyer/detail/<string:id>')
def flyer_detail(id):
    obj_flyer = Flyer.query.filter_by(id = id).first()
    obj_flyer.imagen = b64encode(obj_flyer.imagen).decode("utf-8")
    return render_template('/flyer/detail.html', myFlyer = obj_flyer)