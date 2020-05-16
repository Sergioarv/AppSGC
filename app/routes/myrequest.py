from app import app
from app.routes import *
from flask import request
from datetime import datetime
from sqlalchemy import exc

#Rutas de Solicitud
#Ruta Index solicitudes
@app.route('/request')
def request_index():
    if authentication():
        requests = Request.query.filter_by(state = 'Solicitado').all()
        return render_template('/request/index.html', listRequest = requests)
    else:
        return redirect('/login')

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
        order = datetime.now()
        date_input = datetime.now().strftime("%d/%m/%Y")
        hour_input = datetime.now().strftime("%H:%M:%S")
        state = 'Solicitado'
        obj_request = Request(name = name, address = address, email = email, phone = phone, destino = destino, origin = origin, description = description, dateI = date_input, hourI = hour_input, order = order, state = state)
        db.session.add(obj_request)
        db.session.commit()
        enviar_mensaje(obj_request, 1)
        flash ('Su solicitud está siendo procesada', 'success')
        return redirect('/')
    else:
        obj_flyer = Flyer.query.filter_by(id = id).first()
        return render_template('/request/create.html', myFlyer = obj_flyer)

#Ruta responder solicitudes
@app.route('/request/answer/<string:id>', methods=["GET", "POST"])
def request_answer(id):
    if authentication():
        obj_request = Request.query.filter_by(id = id).first()
        date = datetime.now().strftime("%d de %B del %Y")
        if obj_request != None:
            if request.method == 'POST':            
                para = request.form["inputTo"]
                asunto = request.form["asunto"]
                value = request.form["value"]
                num = request.form["num"]
                value_total = int(num) * int(value)
                delivery = datetime.now()
                date_output = datetime.now().strftime("%d/%m/%Y")
                hour_output = datetime.now().strftime("%H:%M:%S")
                try:
                    obj_quotation = Quotation(para = para, asunto = asunto, value = value, dateO = date_output,hourO = hour_output, delivery = delivery, valueT = value_total, numP = num, request_id = id)
                    db.session.add(obj_quotation)
                    db.session.commit()
                    for i in range(1, 13):
                        try:
                            item = request.form['item'+str(i)]
                            if i < 9:
                                obj_constraint = Constraint(constraint = item, tipe = 0, quotation_id = obj_quotation.id)
                                db.session.add(obj_constraint)
                                db.session.commit()
                            else:
                                obj_constraint = Constraint(constraint = item, tipe = 1, quotation_id = obj_quotation.id)
                                db.session.add(obj_constraint)
                                db.session.commit()
                        except:
                            pass
                    obj_request.state = 'Procesado'
                    db.session.commit()
                    return redirect('/quotation')
                except exc.SQLAlchemyError:
                    flash('Ya se ha respondido a esta Solicitud','danger')
            else:
                return render_template('/request/answer.html', myRequest = obj_request, date = date)
        flash('La Solicitud no existe o Ya fue Respondida','danger')
        return redirect('/request')
    else:
        return redirect('/login')