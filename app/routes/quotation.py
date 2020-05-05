from app import app
from app.routes import *

#Rutas de Cotizacion
#Ruta Index cotizacion
@app.route('/quotation')
def quotation_index():
    if filtroS():
        oRequest = db.session.query(Request, Quotation).join(Quotation).filter(Request.state != 'Solicitado').all()
        return render_template('/quotation/index.html', listRequest = oRequest)
    else:
        return redirect('/login')

#Ruta detalles de cotizacion
@app.route('/quotation/detail/<string:id>')
def quotation_detail(id):
    if filtroS():
        q = db.session.query(Request.name, Request.address, Quotation.dateO, Request.origin, Quotation.para, Quotation.asunto, Quotation.value).filter(Request.id == Quotation.request_id).filter(Request.id == id).first()
        itemsA = db.session.query(Constraint.constraint).filter(id == Quotation.request_id).filter(Quotation.id == Constraint.quotation_id, Constraint.tipe == 0).all()
        itemsR = db.session.query(Constraint.constraint).filter(id == Quotation.request_id).filter(Quotation.id == Constraint.quotation_id, Constraint.tipe == 1).all()
        return render_template('/quotation/quotation.html', data = q, itemsA = itemsA, itemsR = itemsR)
    else:
        return redirect('/login')

#ruta de cambiar estado de cotizacion
# Aceptar o Rechazar
@app.route('/quotation/answer//<string:id>,<string:newState>')
def quotation_answer(id, newState):
    if filtroS():
        q = db.session.query(Request, Quotation).filter(Request.id == Quotation.request_id).filter(Request.id == id,).first()
        if q[0].state == 'Procesado':
            q[0].state = newState
            db.session.commit()
            print (q[0].state)
            q[1].valueT = q[1].value * 5
            db.session.commit()
        return redirect('/quotation')
    else:
        return redirect('/login')