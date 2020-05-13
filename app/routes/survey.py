from app import app, db
from flask import render_template, request, redirect
from sqlalchemy import exc
from app.routes import *
from datetime import datetime

@app.route('/survey/<string:id>')
def survey_send(id):
    obj_q = db.session.query(Request).filter(Quotation.request_id == Request.id).filter(Quotation.id == id).first()
    if obj_q is None:
        flash ('La Esta Cotizacion no Existe, Ya ha sido encuestada o Aun esta siendo Procesada', 'info')
        return redirect(url_for('quotation_index'))
    else:
        data = obj_q
        enviar_mensaje(data, 4)
        flash ('Se ha enviado la encuesta al cliente', 'success')
    return redirect(url_for('quotation_index'))

@app.route('/survey/quality/<string:id>',methods=["GET", "POST"])
def survey_quality(id):
    obj_q = db.session.query(Quotation, Request).filter(Quotation.request_id == Request.id).filter(Request.state == 'Aceptado').filter(Quotation.id == id).first()
    date = datetime.now().strftime("%d/%m/%Y")
    if request.method == 'POST':
        try:
            obj_survey = Survey(date = date, quotation_id = obj_q[0].id )
            db.session.add(obj_survey)
            db.session.commit()
            for i in range(1,16):
                p = request.form['pregunta'+str(i)]
                if p != '':
                    obj_quest = Question(quest = i, answer = p, survey_id = obj_survey.id)
                    db.session.add(obj_quest)
                    db.session.commit()
            obj_q[1].state = 'Completado'
            db.session.commit()
        except exc.SQLAlchemyError:
            flash('Esta Cotizacion ya fue Encuestada', 'info')
        return redirect('/')
    else:
        if obj_q is None:
            flash ('La Esta Cotizacion no Existe, Ya ha sido encuestada o Aun esta siendo Procesada', 'info')
            return redirect('/')
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
            flash('Verifique si la cotizacion ha sido encuestada o si esta Rechazada','info')
            return redirect('/')