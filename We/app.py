from myproject import app, db, mail
from flask import render_template, redirect, request, url_for, flash, abort, session
from flask_login import login_user,login_required,logout_user,current_user
from myproject.models import User, Quiz, UserHistory, ForgotPassword
from myproject.forms import LoginForm, RegistrationForm, InsertQuestion, EnterEmail, EnterPassword
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from datetime import datetime
from sqlalchemy import func
import smtplib
from random import randint
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from flask_mail import Mail, Message
from random import randint
from PIL import Image, ImageDraw, ImageFont
#import Image, ImageDraw, ImageFont
import os
import json
import ast

df = pd.DataFrame({'Tag' : [], 'Question' : [], 'Option_A' : [], 'Option_B' : [], 'Option_C' : [], 'Option_D' : [], 'Answer' : []})
# num = 0
# count = 0
otp = []
key = ''
res1 = ''

@app.route('/')
def home():
    return render_template('index_temp.html')


@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('modules_temp.html')

###########-------START----------#################################################################################################################
# OTP Verification for attending test
@app.route('/verify',methods=['GET', 'POST'])
@login_required
def verify():
    global otp
    global key
    global res1
    #print('Im in verify function')
    email= current_user.email
    #print("$$$$$$$$$$", email)
    temp_otp = randint(99999,999999)
    otp.append(temp_otp)
    print('OTPPPPPPP :',otp)
    with open('otp.json','r') as f1:
        res = f1.read()
        res1 = ast.literal_eval(res)
        key = email
        val = temp_otp
        for i in range(len(res1.keys())):
            if key in res1.keys():
                res1[key] = val
            else:
                res1[key] = val
        with open('otp.json','w') as f2:
            f2.write(str(res1))
            f2.close()
    msg=Message(subject='OTP',sender='eramkumar94@gmail.com',recipients=[email])
    msg.body=str(temp_otp)
    mail.send(msg)
    return render_template('otp.html')

# OTP Validation
@app.route('/validate',methods=['GET', 'POST'])
def validate():
    global otp
    global key
    key = current_user.email

    user_otp=request.form['otp']
    #if int(otp)==int(user_otp):
    print('USERRR OTP',user_otp,':',otp)
    with open('otp.json','r') as f3:
        red = f3.read()
        result = ast.literal_eval(red)

        #original_otp = result[key]
        print("mail :",key,"****",user_otp)
        if (key in result.keys()) and (int(user_otp) == int(result[key])):
            return redirect(url_for('quiz'))
    return "<h3>Invalid OTP, Please Try Again</h3>"
##############--------END------------------##################################################################################################################

@app.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            #Log in the user
            login_user(user)
            flash('Logged in successfully.')
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('welcome_user')

            return redirect(next)
    return render_template('login_temp.html', form=form)


@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        query = User.query.filter_by(email = form.email.data).first()
        if(query):
            msg = '***User already exists, kindly use another email'
            return render_template('register_temp.html', form=form, msg=msg)
        else:
            user = User(email = form.email.data,
                        username = form.username.data,
                        password = form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Thanks for registering! Now you can login!')
            return redirect(url_for('login'))
    return render_template('register_temp.html', form=form)


@app.route('/add', methods = ['GET', 'POST'])
def insert_question():
    form = InsertQuestion()
    if form.validate_on_submit():
        quest = Quiz(tag = form.tag.data, question = form.question.data, option_a = form.option_a.data, option_b = form.option_b.data, option_c = form.option_c.data, option_d = form.option_d.data, answer = form.answer.data)
        db.session.add(quest)
        db.session.commit()
        return redirect(url_for('insert_question'))
    return render_template('insert_question.html', form=form)


@app.route('/instructions', methods = ['GET', 'POST'])
@login_required
def questions():
    # ADD LOGIC TO GET DATA FROM DB
    query = UserHistory.query.filter_by(user = current_user).order_by(UserHistory.attempted_on.desc()).first()
    days = 365

    if(query):
        gap = datetime.now().date() - query.attempted_on.date()
        days = gap.days

    if(days < 0):
        return render_template('denied_temp.html', gap = days)
    else:
        # save df in session
        # session['data'] = df
        # else dict of list {[row1], [row2], [row3], ....}

        session['num'] = 0
        session['count'] = 0

        global df
        df = pd.DataFrame({'Tag' : [], 'Question' : [], 'Option_A' : [], 'Option_B' : [], 'Option_C' : [], 'Option_D' : [], 'Answer' : []})
        query = Quiz.query.order_by(func.random()).limit(20)
        for row in query:
            var = {'Tag' : row.tag, 'Question' : row.question, 'Option_A' : row.option_a, 'Option_B' : row.option_b, 'Option_C' : row.option_c, 'Option_D' : row.option_d, 'Answer' : row.answer}
            df = df.append(var, ignore_index = True)
        print(df)
        return render_template('test_temp.html')


cert_name = ''
@app.route('/quiz', methods = ['GET', 'POST'])
@login_required
def quiz():
    if session.get("num") is None:
        return "Bad Request"
    global df
    # global num
    # global count
    ########----------START--------############################################################################################################################
    global cert_name
    session['num'] += 1
    # reading certificate form folder
    pic1 = os.path.abspath(app.config['UPLOAD_FOLDER'])
    pic1 = os.path.join(pic1, 'certificate.jpg')

    email_user = 'eetakota.ramkumar@gmail.com'
    email_sender = 'eramkumar94@gmail.com'
    subject = 'Python Certificate From Innomatics'

    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_user
    msg['Subject'] = subject

    body = "Hi Dear...., Congratulations......!"
#########------END---------#################################################################################################################
    q = df['Question'].tolist()
    op_1 = df['Option_A'].tolist()
    op_2 = df['Option_B'].tolist()
    op_3 = df['Option_C'].tolist()
    op_4 = df['Option_D'].tolist()
    ans = df['Answer'].tolist()

    if(session['num'] <= 21):
        for i in range(len(ans)):
            if(str(i) in request.form.keys() and request.form[str(i)] == str(ans[i])):
                session['count'] += 1
        return render_template('quest_temp.html', ques=q, op1=op_1, op2=op_2, op3=op_3, op4=op_4, n=session['num'])
    else:
        c = session['count']
        session.clear()
        if c > 13:
            remark = 'Excellent'
####---------START---------##########################################################################################################################
            font = ImageFont.truetype('arial.ttf',60)
            img = Image.open('./myproject/static/pics/certificate.jpg')
            draw = ImageDraw.Draw(img)
            draw.text(xy=(725,535),text='{}'.format(current_user.username),fill=(0,0,0),font=font)
            cert_name = 'certificate_'+current_user.username+'.jpg'
            img.save(cert_name)

            msg.attach(MIMEText(body,'plain'))
            filename = cert_name
            attachment = open(filename, 'rb')
            print('ATTTachaaa',attachment)
            part = MIMEBase('application','octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',"attachment; filename= "+filename)

            msg.attach(part)
            text = msg.as_string()
            #print('MAILLLLLLLLL',text)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('eramkumar94@gmail.com','9550361900')
            server.sendmail("eramkumar94@gmail.com",current_user.email,text)
			#msg = Message(sender="eramkumar94@gmail.com", recipients = MAIL)
            server.send(text)
################---------END------------##########################################################################################################################################
        else:
            remark = "Better luck next time"
        user_history = UserHistory(tag='Python', score=c, user_id=current_user.id)
        db.session.add(user_history)
        db.session.commit()
    return render_template('score_temp.html', remark = remark, count = c)

# if os.path.isfile(cert_name):
#     os.remove(cert_name)

@app.route('/history')
@login_required
def history():
    query = UserHistory.query.filter_by(user = current_user).order_by(UserHistory.attempted_on.desc())
    return render_template('History.html', results = query)


@app.route('/view', methods = ['GET', 'POST'])
def question_bank():
    if request.method == "GET":
        return render_template('view.html', query=Quiz.query.all())
    return render_template("view.html", query=Quiz.query.all())

@app.route('/email')
def enter_email():
    return render_template("forget_mail.html")

@app.route('/forgot_password', methods = ['GET', 'POST'])
def forgot_password():
    form = EnterEmail()
    if form.validate_on_submit():
        session['email'] = ''
        query = User.query.filter_by(email = form.email.data).first()
        if(query):
            session['email'] = form.email.data
            # reset_otp = randint(9999999, 100000000)
            # reset_user = ForgotPassword(email = session['email'], otp = reset_otp)
            # db.session.add(reset_user)
            # db.session.commit()
            # # Send OTP to the user on email
            # print("*"*20, reset_otp)
            # END
        # return redirect(url_for('reset_user_otp'))
        return redirect(url_for('reset_password'))
    return render_template("forget_mail.html", form=form)


@app.route('/reset_user_otp', methods = ['GET', 'POST'])
def reset_user_otp():
    if('email' in session.keys() and User.query.filter_by(email = session['email']).first()):
        form = OTP()
        if form.validate_on_submit():
            query = ForgotPassword.query.filter_by(email = session['email']).first()
            print("*"*20, query.otp, form.otp.data)
            print("*"*20, type(query.otp), type(form.otp.data))
            if(query.otp == form.otp.data):
                return redirect(url_for('reset_password'))
        return render_template('reset_password_otp.html', form = form)
    return '<h1>Invalid Request</h1>'


@app.route('/reset_password', methods = ['GET', 'POST'])
def reset_password():
    if('email' in session.keys() and User.query.filter_by(email = session['email']).first()):
        form = EnterPassword()
        if form.validate_on_submit():
            cookie = session['email']
            u = User.query.filter_by(email = cookie).first()
            u.password_hash = generate_password_hash(form.password.data)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('reseting_password.html', form=form)
    return '<h1>Invalid Request</h1>'


# @app.route('/upload', methods = ['GET', 'POST'])
# def upload_questions():
#     py_quiz = pd.read_csv('myproject/python_quiz_temp.csv', encoding = 'unicode_escape')
#     for x in range(py_quiz.shape[0]):
#         quest = Quiz(tag = py_quiz.iloc[x].tag, question = py_quiz.iloc[x].question, option_a = py_quiz.iloc[x].option_a, option_b = py_quiz.iloc[x].option_b, option_c = py_quiz.iloc[x].option_c, option_d = py_quiz.iloc[x].option_d, answer = py_quiz.iloc[x].answer)
#         db.session.add(quest)
#         db.session.commit()
#     return '<h1>Upload Page</h1>'


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
