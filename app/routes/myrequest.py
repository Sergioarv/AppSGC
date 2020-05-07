from app import app
from app.routes import *
from flask import request
from datetime import datetime
from sqlalchemy import exc

#Rutas de Solicitud
#Ruta Index solicitudes
@app.route('/request')
def request_index():
    if filtroS():
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
        dateI = datetime.now().strftime("%d/%m/%Y")
        hourI = datetime.now().strftime("%H:%M:%S")
        state = 'Solicitado'
        oRequest = Request(name = name, address = address, email = email, phone = phone, destino = destino, origin = origin, description = description, dateI = dateI, hourI = hourI, state = state)
        db.session.add(oRequest)
        db.session.commit()
        enviarMensaje(oRequest, 1)
        flash ('Su solicitud está siendo procesada', 'success')
        return redirect('/')
    else:
        oFlyer = Flyer.query.filter_by(id = id).first()
        return render_template('/request/create.html', myFlyer = oFlyer)

#Ruta responder solicitudes
@app.route('/request/answer/<string:id>', methods=["GET", "POST"])
def request_answer(id):
    if filtroS():
        oRequest = Request.query.filter_by(id = id).first()
        date = datetime.now().strftime("%d de %B del %Y")
        if request.method == 'POST':            
            para = request.form["inputTo"]
            asunto = request.form["asunto"]
            value = request.form["value"]
            num = request.form["num"]
            valueT = int(num) * int(value)
            dateO = datetime.now().strftime("%d/%m/%Y")
            hourO = datetime.now().strftime("%H:%M:%S")
            itemsA = []
            itemsR = []
            for i in range(1, 16):
                try:
                    item = request.form['item'+str(i)]
                    if i < 12:
                        itemsA.append(item)
                        oConstraint = Constraint(constraint = item, tipe = 0, quotation_id = oQuotation.id)
                        db.session.add(oConstraint)
                        db.session.commit()
                    else:
                        itemsR.append(item)
                        oConstraint = Constraint(constraint = item, tipe = 1, quotation_id = oQuotation.id)
                        db.session.add(oConstraint)
                        db.session.commit()
                except:
                    pass
            try:
                oRequest.state = 'Procesado'
                db.session.commit()
                oQuotation = Quotation(para = para, asunto = asunto, value = value, dateO = dateO,hourO = hourO, valueT = valueT, request_id = id)
                db.session.add(oQuotation)
                db.session.commit()
            except exc.SQLAlchemyError:
                flash('Ya se ha respondido a esta Solicitud','danger')
            return redirect('/quotation')
        else:
            return render_template('/request/answer.html', myRequest = oRequest, date = date)
    else:
        return redirect('/login')