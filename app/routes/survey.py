from app import app, db
from flask import render_template, request, redirect
from sqlalchemy import exc
from app.routes import *
from datetime import datetime

@app.route('/survey/<string:id>')
def survey_send(id):
    oQ = db.session.query(Request).filter(Quotation.request_id == Request.id).filter(Quotation.id == id).first()
    if oQ is None:
        flash ('La Esta Cotizacion no Existe, Ya ha sido encuestada o Aun esta siendo Procesada', 'info')
        return redirect('/quotation')
    else:
        data = oQ
        enviarMensaje(data, 4)
        flash ('Se ha enviado la encuesta al cliente', 'success')
    return redirect('/quotation')

@app.route('/survey/quality/<string:id>',methods=["GET", "POST"])
def survey_quality(id):
    oQ = db.session.query(Quotation, Request).filter(Quotation.request_id == Request.id).filter(Request.state == 'Aceptado').filter(Quotation.id == id).first()
    date = datetime.now().strftime("%d/%m/%Y")
    if request.method == 'POST':
        try:
            oSurvey = Survey(date = date, quotation_id = oQ[0].id )
            db.session.add(oSurvey)
            db.session.commit()
            for i in range(1,16):
                try:
                    p = request.form['pregunta'+str(i)]
                except:
                    pass
                if p != '':
                    oQuest = Question(quest = i, answer = p, survey_id = oSurvey.id)
                    db.session.add(oQuest)
                    db.session.commit()
            oQ[1].state = 'Completado'
            db.session.commit()
        except exc.SQLAlchemyError:
            flash('Esta Cotizacion ya fue Encuestada', 'info')
        return redirect('/')
    else:
        if oQ is None:
            flash ('La Esta Cotizacion no Existe, Ya ha sido encuestada o Aun esta siendo Procesada', 'info')
            return redirect('/')
        else:
            data = oQ[1]
            enviarMensaje(data, 4)
        return render_template('/survey/survey_quality.html', date = date)

@app.route('/survey/detail/<string:id>', methods = ['GET','POST'])
def survey_detail(id):
    if request.method == 'POST':
        return redirect ('/quotation')
    else:
        try:
            date = db.session.query(Survey.date).filter(Survey.quotation_id == id).first()
            data = db.session.query(Question).filter(Question.survey_id == Survey.id).filter(Survey.quotation_id == id).all()
            return render_template('/survey/survey_detail.html', data = data, date = date.date, id = id)
        except:
            flash('Verifique La cotizacion','info')
            return redirect('/')