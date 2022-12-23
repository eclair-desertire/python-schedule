from flask import Flask, render_template, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import secrets
from datetime import datetime
from flask_socketio import SocketIO, emit
import json
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:admin@postgres_db_container/scheduledb'
socketio=SocketIO(app)

db = SQLAlchemy(app)

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer(), primary_key=True)
    type = db.Column(db.String(255), nullable=False)

    subject_name = db.Column(db.String(255), nullable=False)
    cabinet = db.Column(db.String(255), nullable=False)
    teacher = db.Column(db.String(255), nullable=False)
    group = db.Column(db.String(255), nullable=False)
    time = db.Column(db.String(255), nullable=False)
    day = db.Column(db.String(255), nullable=False)

def init_data():
    s4=Subject(type='Практика',subject_name='Физика',cabinet='407',
    teacher='Кабанов Д.В.',group='A2204',time='10:00',day='Вторник')
    s5=Subject(type='Практика',subject_name='Физика',cabinet='407',
    teacher='Кабанов Д.В.',group='A2108',time='8:00',day='Среда')
    s6=Subject(type='Практика',subject_name='Физика',cabinet='409',
    teacher='Кабанов Д.В.',group='A2101',time='11:00',day='Среда')

    s7=Subject(type=' ',subject_name='Физкультура',cabinet=' ',
    teacher='Мамакина Д.А.',group='A2101',time='9:00',day='Понедельник')
    s8=Subject(type=' ',subject_name='Физкультура',cabinet=' ',
    teacher='Мамакина Д.А.',group='A2108',time='10:00',day='Вторник')
    s9=Subject(type=' ',subject_name='Физкультура',cabinet=' ',
    teacher='Мамакина Д.А.',group='A2204',time='8:00',day='Четверг')

    s10=Subject(type='Лекция',subject_name='Программирование',cabinet='333',
    teacher='Устинов А.И.',group='A2204',time='8:00',day='Понедельник')
    s11=Subject(type='Лекция',subject_name='Программирование',cabinet='333',
    teacher='Устинов А.И.',group='A2101',time='11:00',day='Понедельник')
    s12=Subject(type='Лекция',subject_name='Программирование',cabinet='333',
    teacher='Устинов А.И.',group='A2108',time='12:00',day='Понедельник')

    s13=Subject(type='Практика',subject_name='Программирование',cabinet='354',
    teacher='Устинов А.И.',group='A2101',time='9:00',day='Вторник')
    s14=Subject(type='Практика',subject_name='Программирование',cabinet='354',
    teacher='Устинов А.И.',group='A2204',time='10:00',day='Вторник')
    s15=Subject(type='Практика',subject_name='Программирование',cabinet='346',
    teacher='Устинов А.И.',group='A2108',time='9:00',day='Пятница')

    db.session.add_all([s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15])
    db.session.commit()
    print("Done")


@app.route('/teacher')
def teacher():
    return render_template('teacher.html')

@app.route('/student')
def student():
    return render_template('student.html')


@socketio.on('groupfilter')
def groupfilter(groupfil):
    results=Subject.query.filter_by(group=str(groupfil))
    data=[]
    # data={'data':{}}
    # for p in results:
    #     data['data'][p.id]=json.dumps({"id":p.id,"type":p.type,"subject_name":p.subject_name,"cabinet":p.cabinet,"teacher":p.teacher,"group":p.group,"time":p.time,"day":p.day},ensure_ascii=False)
    for p in results:
        data.append(json.dumps({"id":p.id,"type":p.type,"subject_name":p.subject_name,
    "cabinet":p.cabinet,"teacher":p.teacher,"group":p.group,"time":p.time,"day":p.day},ensure_ascii=False))
    # data=[{"id":p.id,"type":p.type,"subject_name":p.subject_name,
    # "cabinet":p.cabinet,"teacher":p.teacher,"group":p.group,"time":p.time,"day":p.day} for p in results]
    print(str(data))
    emit('groupfilterresult',{'results':str(data)}, broadcast=True)



if __name__ == "__main__":
    socketio.run(app,host='0.0.0.0',port=80)

    