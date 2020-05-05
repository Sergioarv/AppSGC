from app import app
from app.routes import *
from flask import request

#Rutas de Flyer
#Ruta de index Flyer
@app.route('/flyer')
def flyer_index():
    if filtroS():
        flyers = Flyer.query.all()
        for f in flyers:
            f.imagen = b64encode(f.imagen).decode("utf-8")
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
                img = f.read()
                print (len(img))
                oFlyer = Flyer(name = nombre, description = descripcion, imagen = img)
                db.session.add(oFlyer)
                db.session.commit()
                flash("Se a agregado un Flyer", "success")
                return redirect('/flyer')
            else:
                flash("No selecciono una imagen o no es una imagen",'danger')
                return redirect('/flyer/create')
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
            print (f)
            #Si hay una imagen se actualiza
            if f:
                #Verifica que tengo un nombre y extension valida la imagen
                if f and allowed_file(f.filename):
                    img = f.read()
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
    oFlyer.imagen = b64encode(oFlyer.imagen).decode("utf-8")
    return render_template('/flyer/detail.html', myFlyer = oFlyer)
