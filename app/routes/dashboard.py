from app import app, db
from app.routes import *
from flask import render_template
from sqlalchemy.sql import func
from sqlalchemy import exc, or_, and_, desc
from app.schemas.models import *
from datetime import datetime
from numpy import array

# Dashboard y otros graficos
@app.route('/dashboard')
def dashboard_index():
    if authentication():
        anio = datetime.now().strftime("%Y")
        return render_template('/dashboard/dashboard.html', anio = anio)
    else:
        return redirect(url_for('login_in'))

@app.route('/requestPie/<string:d>/<string:an>')
def request_pie(d, an):
    if authentication():
        tittle ='Tiempo de respuesta'
        anio = datetime.now().strftime("%Y")
        list_a = [int(anio), int(anio)-1, int(anio)-2, int(anio)-3, int(anio)-4]
        if an != anio:
            anio = an
        res = db.session.query(Quotation.delivery, Request.order).filter(Quotation.request_id == Request.id, Request.state != 'Solicitado').filter(and_(Quotation.delivery >= anio+str('-01-01')), Quotation.delivery <= anio+str('-12-31')).all()
        data = array([0,0,0,0,0,0,0,0,0])
        valor = ['30min ó -','30min-1h','1h-6hs','6hs-12hs','12hs-1Dia','1Dia-15Dias','15Dias-1Mes','1Mes-6Meses','6Meses ó +']
        for r in res:
            time_t = r[0] - r[1]
            if time_t.seconds < 1800:
                data[0] += 1
            elif time_t.seconds >= 1800 and time_t.seconds < 3600:
                data[1] +=1
            elif time_t.seconds >= 3600 and time_t.seconds < 21600:
                data[2] +=1
            elif time_t.seconds >= 21600 and time_t.seconds < 43200:
                data[3] +=1
            elif time_t.seconds >= 43200 and time_t.days < 1:
                data[4] +=1
            elif time_t.days >= 1 and time_t.days < 15:
                data[5] +=1
            elif time_t.days >= 15 and time_t.days < 30.4167:
                data[6] +=1
            elif time_t.days >= 30.4167 and time_t.days < 182.5:
                data[7] +=1
            else:
                data[8] +=1
        return render_template('/dashboard/piechart.html', mydata = data, valor = valor, tittle = tittle, dashboard = d, tipe = 'Tiempo', cant = 'Duración', list_a = list_a, graphic = 'requestPie')
    else:
        return redirect(url_for('login_in'))

@app.route('/requestBar/<string:d>/<string:an>')
def request_bar(d, an):
    if authentication():
        tittle ='Cantidad de Solicitudes por Tipo'
        anio = datetime.now().strftime("%Y")
        list_a = [int(anio), int(anio)-1, int(anio)-2, int(anio)-3, int(anio)-4]
        if an != anio:
            anio = an
        print(anio)
        data = []
        c = ['#0040FF','#088A4B','#FF0000','#FF8000','#a000a0']
        valor = ['Solicitado','Aceptado','Rechazado','Procesado','Completado']
        data.append(Request.query.filter_by(state = 'Solicitado').filter(and_(Request.order >= anio+str("-01-01"), Request.order <= anio+str("-12-31"))).count())
        data.append(Request.query.filter_by(state = 'Aceptado').filter(and_(Request.order >= anio+str("-01-01"), Request.order <= anio+str("-12-31"))).count())
        data.append(Request.query.filter_by(state = 'Rechazado').filter(and_(Request.order >= anio+str("-01-01"), Request.order <= anio+str("-12-31"))).count())
        data.append(Request.query.filter_by(state = 'Procesado').filter(and_(Request.order >= anio+str("-01-01"), Request.order <= anio+str("-12-31"))).count())
        data.append(Request.query.filter_by(state = 'Completado').filter(and_(Request.order >= anio+str("-01-01"), Request.order <= anio+str("-12-31"))).count())
        return render_template('/dashboard/barchart.html', mydata = data, valor = valor, valorA = valor, tittle = tittle, c = c, dashboard = d, tipe = 'Tipo Solicitud', cant = 'Cantidad', list_a = list_a, graphic = 'requestBar')
    else:
        return redirect(url_for('login_in'))

@app.route('/salesTime/<string:d>/<string:an>')
def sale_time(d,an):
    if authentication():
        try:
            tittle ='Ventas totales por dia'
            anio = datetime.now().strftime("%Y")
            list_a = [int(anio), int(anio)-1, int(anio)-2, int(anio)-3, int(anio)-4]
            if an != anio:
                anio = an
            c = ['#0040FF','#088A4B','#FF0000','#FF8000']
            data = []
            valor = []
            cur2 = db.session.query(Quotation.dateO).filter(and_(Quotation.delivery >= anio+str("-01-01"), Quotation.delivery <= anio+str("-12-31"))).group_by(Quotation.delivery).all()
            cur = db.session.query(func.sum(Quotation.valueT).label('mayor')).filter(Quotation.request_id == Request.id, or_(Request.state == 'Aceptado', Request.state == 'Completado')).filter(and_(Quotation.delivery >= anio+str("-01-01"), Quotation.delivery <= anio+str("-12-31"))).group_by(Quotation.dateO).all()
            for i in cur:
                data.append(i.mayor)
            for i in cur2:
                valor.append(i.dateO)
        except exc.SQLAlchemyError:
            pass
        return render_template('/dashboard/barchart.html', mydata = data, valor = valor, valorA = valor, tittle = tittle, c = c, dashboard = d, tipe = 'Solicitud', cant = 'Cantidad', list_a = list_a, graphic = 'salesTime')
    else:
        return redirect(url_for('login_in'))

@app.route('/salesTimeline/<string:d>/<string:an>')
def sale_timeline(d, an):
    if authentication():
        try:
            tittle ='Ventas (Total, Promedio, Mayor, Menor)'
            anio = datetime.now().strftime("%Y")
            list_a = [int(anio), int(anio)-1, int(anio)-2, int(anio)-3, int(anio)-4]
            if an != anio:
                anio = an
            data = []
            data2 = []
            data3 = []
            data4 = []
            valor = []
            ejex = db.session.query(Quotation.dateO).filter(Quotation.request_id == Request.id, or_(Request.state == 'Aceptado', Request.state == 'Completado')).filter(and_(Quotation.delivery >= anio+str("-01-01"), Quotation.delivery <= anio+str("-12-31"))).group_by(Quotation.dateO).order_by(Quotation.delivery).all()
            total = db.session.query(func.sum(Quotation.valueT).label("valorT")).filter(Quotation.request_id == Request.id, or_(Request.state == 'Aceptado', Request.state == 'Completado')).filter(and_(Quotation.delivery >= anio+str("-01-01"), Quotation.delivery <= anio+str("-12-31"))).group_by(Quotation.dateO).order_by(Quotation.delivery).all()
            prom = db.session.query(func.avg(Quotation.valueT).label("valorP")).filter(Quotation.request_id == Request.id, or_(Request.state == 'Aceptado', Request.state == 'Completado')).filter(and_(Quotation.delivery >= anio+str("-01-01"), Quotation.delivery <= anio+str("-12-31"))).group_by(Quotation.dateO).order_by(Quotation.delivery).all()
            maxi = db.session.query(func.max(Quotation.valueT).label("valorM")).filter(Quotation.request_id == Request.id, or_(Request.state == 'Aceptado', Request.state == 'Completado')).filter(and_(Quotation.delivery >= anio+str("-01-01"), Quotation.delivery <= anio+str("-12-31"))).group_by(Quotation.dateO).order_by(Quotation.delivery).all()
            mini = db.session.query(func.min(Quotation.valueT).label("valorMi")).filter(Quotation.request_id == Request.id, or_(Request.state == 'Aceptado', Request.state == 'Completado')).filter(and_(Quotation.delivery >= anio+str("-01-01"), Quotation.delivery <= anio+str("-12-31"))).group_by(Quotation.dateO).order_by(Quotation.delivery).all()
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
        return render_template('/dashboard/linechart.html', total = data, prom = data2, maxi = data3, mini = data4, valor = valor, tittle = tittle, dashboard = d, tipe = 'Fecha de venta', cant = 'Valor', list_a = list_a, graphic = 'salesTimeline')
    else:
        return redirect(url_for('login_in'))

@app.route('/surveyPie/<string:d>/<string:an>')
def survey_pie(d, an):
    if authentication():
        tittle = 'Valoracion de Encuestas'
        anio = datetime.now().strftime("%Y")
        list_a = [int(anio), int(anio)-1, int(anio)-2, int(anio)-3, int(anio)-4]
        if an != anio:
            anio = an
        res = db.session.query(Question.answer, func.count(Question.answer).label('num')).filter(Question.survey_id == Survey.id).filter(Survey.quotation_id == Quotation.id).filter(Quotation.request_id == Request.id).filter(Request.state == 'Completado').filter(and_(Quotation.delivery >= anio+str("-01-01"), Quotation.delivery <= anio+str("-12-31"))).group_by(Question.answer).all()
        data = []
        valor = []
        suma = 0
        for r in res:   
            if(r.answer == 'Excelente' or r.answer == 'Bueno' or r.answer == 'Malo' or r.answer == 'N/A' or r.answer == 'Si' or r.answer == 'No'):
                data.append(r.num)
                valor.append(r.answer)
            else:
                suma = suma + r.num
        data.append(suma)
        valor.append('Otros')
        return render_template('/dashboard/piechart.html', mydata = data, valor = valor, tittle = tittle, dashboard = d, tipe = 'Tipo de Valoracion', cant = 'Cantidad de valoracion', list_a = list_a, graphic = 'surveyPie')
    else:
        return redirect(url_for('login_in'))

@app.route('/saleTri/<string:d>/<string:an>')
def sale_tri(d, an):
    if authentication():
        data = []
        aux = []
        c = ['#0040FF','#088A4B','#FF0000','#FF8000','#0040FF','#088A4B','#FF0000','#FF8000','#0040FF','#088A4B','#FF0000','#FF8000','#0040FF','#088A4B','#FF0000','#FF8000']
        valor = ['Enero','Febrero','Marzo','1er Trimestre', 'Abril', 'Mayo', 'Junio', '2do Trimestre', 'Julio','Agosto','Septiembre','3er Trimestre','Octubre','Noviembre', 'Diciembre', '4to Trimestre']
        valorA = ['Ene','Feb','Mar','1er Trim', 'Abr', 'May', 'Jun', '2do Trim', 'Jul','Ago','Sept','3er Trim','Oct','Nov', 'Dic', '4to Trim']
        tittle = 'Ventas por trimestres'
        anio = datetime.now().strftime("%Y")
        list_a = [int(anio), int(anio)-1, int(anio)-2, int(anio)-3, int(anio)-4]
        if an != anio:
            anio = an
        aux.append(db.session.query(func.sum(Quotation.valueT)).filter(Quotation.request_id == Request.id).filter(Request.state != 'Solicitado').filter(and_(Quotation.delivery >= anio+str('-01-01'), Quotation.delivery <= anio+str('-01-31'))).first())
        aux.append(db.session.query(func.sum(Quotation.valueT)).filter(Quotation.request_id == Request.id).filter(Request.state != 'Solicitado').filter(and_(Quotation.delivery >= anio+str('-02-01'), Quotation.delivery <= anio+str('-02-28'))).first())
        aux.append(db.session.query(func.sum(Quotation.valueT)).filter(Quotation.request_id == Request.id).filter(Request.state != 'Solicitado').filter(and_(Quotation.delivery >= anio+str('-03-01'), Quotation.delivery <= anio+str('-03-31'))).first())
        aux.append(db.session.query(func.sum(Quotation.valueT)).filter(Quotation.request_id == Request.id).filter(Request.state != 'Solicitado').filter(and_(Quotation.delivery >= anio+str('-04-01'), Quotation.delivery <= anio+str('-04-30'))).first())
        aux.append(db.session.query(func.sum(Quotation.valueT)).filter(Quotation.request_id == Request.id).filter(Request.state != 'Solicitado').filter(and_(Quotation.delivery >= anio+str('-05-01'), Quotation.delivery <= anio+str('-05-31'))).first())
        aux.append(db.session.query(func.sum(Quotation.valueT)).filter(Quotation.request_id == Request.id).filter(Request.state != 'Solicitado').filter(and_(Quotation.delivery >= anio+str('-06-01'), Quotation.delivery <= anio+str('-06-30'))).first())
        aux.append(db.session.query(func.sum(Quotation.valueT)).filter(Quotation.request_id == Request.id).filter(Request.state != 'Solicitado').filter(and_(Quotation.delivery >= anio+str('-07-01'), Quotation.delivery <= anio+str('-07-31'))).first())
        aux.append(db.session.query(func.sum(Quotation.valueT)).filter(Quotation.request_id == Request.id).filter(Request.state != 'Solicitado').filter(and_(Quotation.delivery >= anio+str('-08-01'), Quotation.delivery <= anio+str('-08-31'))).first())
        aux.append(db.session.query(func.sum(Quotation.valueT)).filter(Quotation.request_id == Request.id).filter(Request.state != 'Solicitado').filter(and_(Quotation.delivery >= anio+str('-09-01'), Quotation.delivery <= anio+str('-09-30'))).first())
        aux.append(db.session.query(func.sum(Quotation.valueT)).filter(Quotation.request_id == Request.id).filter(Request.state != 'Solicitado').filter(and_(Quotation.delivery >= anio+str('-10-01'), Quotation.delivery <= anio+str('-10-31'))).first())
        aux.append(db.session.query(func.sum(Quotation.valueT)).filter(Quotation.request_id == Request.id).filter(Request.state != 'Solicitado').filter(and_(Quotation.delivery >= anio+str('-11-01'), Quotation.delivery <= anio+str('-11-30'))).first())
        aux.append(db.session.query(func.sum(Quotation.valueT)).filter(Quotation.request_id == Request.id).filter(Request.state != 'Solicitado').filter(and_(Quotation.delivery >= anio+str('-12-01'), Quotation.delivery <= anio+str('-12-31'))).first())
        suma = 0
        cont = 0
        for a in aux:
            if a[0] is None:
                data.append(0)
            else:
                data.append(a[0])
                suma = suma + a[0]
            cont += 1
            if cont == 3:
                data.append(suma)
                suma = 0
                cont = 0
        return render_template('/dashboard/columnchart.html', mydata = data, valor = valor, valorA = valorA, tittle = tittle, c = c, dashboard = d, tipe = 'Mes o Trimestre del año %s'%anio, cant = 'Total Ventas', list_a = list_a, graphic = 'saleTri')
    else:
        return redirect(url_for('login_in'))