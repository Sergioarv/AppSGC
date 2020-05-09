from app import app, db
from flask import render_template
from sqlalchemy.sql import func
from sqlalchemy import exc, or_
from app.schemas.models import Request, Quotation
import datetime

# Dashboard y otros graficos
@app.route('/dashboard')
def dashboard_index():
    return render_template('/dashboard/dashboard.html')

@app.route('/solicitudes/<string:d>')
def solicitudes(d):
    tittle ='Cantidad de Solicitudes por Tipo'
    data = []
    valor = ['Solicitado','Rechazado','Procesado','Aceptado','Completado']
    data.append(Request.query.filter_by(state = 'Solicitado').count())
    data.append(Request.query.filter_by(state = 'Rechazado').count())
    data.append(Request.query.filter_by(state = 'Procesado').count())
    data.append(Request.query.filter_by(state = 'Aceptado').count())
    data.append(Request.query.filter_by(state = 'Completado').count())
    return render_template('/dashboard/piechart.html', mydata = data, valor = valor, tittle = tittle, dashboard = d)

@app.route('/solicitudesBar/<string:d>')
def solicitudesBar(d):
    tittle ='Cantidad de Solicitudes por Tipo'
    data = []
    c = ['#0040FF','#088A4B','#FF0000','#FF8000','#a000a0']
    valor = ['Solicitado','Aceptado','Rechazado','Procesado','Completado']
    data.append(Request.query.filter_by(state = 'Solicitado').count())
    data.append(Request.query.filter_by(state = 'Aceptado').count())
    data.append(Request.query.filter_by(state = 'Rechazado').count())
    data.append(Request.query.filter_by(state = 'Procesado').count())
    data.append(Request.query.filter_by(state = 'Completado').count())
    return render_template('/dashboard/barchart.html', mydata = data, valor = valor, tittle = tittle, c = c, dashboard = d)

@app.route('/tiempo/<string:d>')
def tiempo(d):
    try:
        tittle ='Ventas totales por dia'
        c = ['#0040FF','#088A4B','#FF0000','#FF8000']
        data = []
        valor = []
        cur2 = db.session.query(Quotation.dateO).group_by(Quotation.dateO).all()
        cur = db.session.query(func.sum(Quotation.valueT).label('mayor')).filter(Quotation.request_id == Request.id, or_(Request.state == 'Aceptado', Request.state == 'Completado')).group_by(Quotation.dateO).all()
        for i in cur:
            data.append(i.mayor)
        for i in cur2:
            valor.append(i.dateO)
    except exc.SQLAlchemyError:
        pass
    return render_template('/dashboard/barchart.html', mydata = data, valor = valor, tittle = tittle, c = c, dashboard = d)

@app.route('/lineTiempo/<string:d>')
def line_tiempo(d):
    try:
        tittle ='Ventas (Total, Promedio, Mayor, Menor)'
        data = []
        data2 = []
        data3 = []
        data4 = []
        valor = []
        ejex = db.session.query(Quotation.dateO).filter(Quotation.request_id == Request.id, or_(Request.state == 'Aceptado', Request.state == 'Completado')).group_by(Quotation.dateO).all()
        total = db.session.query(func.sum(Quotation.valueT).label("valorT")).filter(Quotation.request_id == Request.id, or_(Request.state == 'Aceptado', Request.state == 'Completado')).group_by(Quotation.dateO).all()
        prom = db.session.query(func.avg(Quotation.valueT).label("valorP")).filter(Quotation.request_id == Request.id, or_(Request.state == 'Aceptado', Request.state == 'Completado')).group_by(Quotation.dateO).all()
        maxi = db.session.query(func.max(Quotation.valueT).label("valorM")).filter(Quotation.request_id == Request.id, or_(Request.state == 'Aceptado', Request.state == 'Completado')).group_by(Quotation.dateO).all()
        mini = db.session.query(func.min(Quotation.valueT).label("valorMi")).filter(Quotation.request_id == Request.id, or_(Request.state == 'Aceptado', Request.state == 'Completado')).group_by(Quotation.dateO).all()
        for i in ejex:
            valor.append(i.dateO)
        for i in total:
            data.append(i.valorT)
        for i in prom:
            data2.append(i.valorP)
        for i in maxi:
            data3.append(i.valorM)
        for i in mini:
            data4.append(i.valorMi)
    except exc.SQLAlchemyError:
        pass
    return render_template('/dashboard/linechart.html', total = data, prom = data2, maxi = data3, mini = data4, valor = valor, tittle = tittle, dashboard = d)