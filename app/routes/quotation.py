from app import app
from app.routes import *
from sqlalchemy import or_, and_, distinct

#Rutas de Cotizacion
#Ruta Index cotizacion
@app.route('/quotation')
def quotation_index():
    if authentication():
        obj_request = db.session.query(Request, Quotation).filter(Request.id == Quotation.request_id).filter(Request.state != 'Solicitado').all()
        return render_template('/quotation/index.html', listRequest = obj_request)
    else:
        return redirect(url_for('login_in'))

#Ruta detalles de cotizacion
@app.route('/quotation/detail/<string:id>')
def quotation_detail(id):
    if authentication():
        q = db.session.query(Request.name, Request.address, Quotation.dateO, Request.origin, Quotation.para, Quotation.asunto, Quotation.value, Quotation.numP, Quotation.valueT).filter(Request.id == Quotation.request_id).filter(Request.id == id).first()
        items_a = db.session.query(Constraint.constraint).filter(id == Quotation.request_id).filter(Quotation.id == Constraint.quotation_id, Constraint.tipe == 0).all()
        items_r = db.session.query(Constraint.constraint).filter(id == Quotation.request_id).filter(Quotation.id == Constraint.quotation_id, Constraint.tipe == 1).all()
        return render_template('/quotation/quotation.html', data = q, itemsA = items_a, itemsR = items_r)
    else:
        return redirect(url_for('login_in'))

#ruta de cambiar estado de cotizacion
# Aceptar o Rechazar
@app.route('/quotation/answer/<string:id>,<string:new_state>')
def quotation_answer(id, new_state):
    if authentication():
        q = db.session.query(Request, Quotation).filter(Request.id == Quotation.request_id).filter(Request.id == id,).first()
        if q[0].state == 'Procesado':
            q[0].state = new_state
            db.session.commit()
            q[1].valueT = q[1].value * q[1].numP
            db.session.commit()
        return redirect('/quotation')
    else:
        return redirect('/login')
