from myproject import app, db, mail
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user,login_required,logout_user
from myproject.models import User, Quiz
from myproject.forms import LoginForm, RegistrationForm, InsertQuestion
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import smtplib
from flask_mail import Mail, Message
from random import randint
import os
from PIL import Image

df = pd.DataFrame({'Tag' : [], 'Question' : [], 'Option_A' : [], 'Option_B' : [], 'Option_C' : [], 'Option_D' : [], 'Answer' : []})
num=0
count=0
otp = ''


@app.route('/')
def home():
    return render_template('index_temp.html')


@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('modules_temp.html')

@app.route('/verify',methods=['GET', 'POST'])
def verify():
    global otp
    #print('Im in verify function')
    email="eetakota.ramkumar@gmail.com"
    otp=randint(000000,999999)
    msg=Message(subject='OTP',sender='eramkumar94@gmail.com',recipients=[email])
    msg.body=str(otp)
    mail.send(msg)
    return render_template('verify.html')

@app.route('/validate',methods=['GET', 'POST'])
def validate():
    global otp
    user_otp=request.form['otp']
    if int(otp)==int(user_otp):
        return redirect(url_for('questions'))
    return "<h3>Please Try Again</h3>"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user is not None and user.check_password(form.password.data):
            #Log in the user
            login_user(user)
            flash('Logged in successfully.')
            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('welcome_user')

            return redirect(next)
    return render_template('login_temp.html', form=form)


@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
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
    global df
    for row in db.session.query(Quiz).all():
        var = {'Tag' : row.tag, 'Question' : row.question, 'Option_A' : row.option_a, 'Option_B' : row.option_b, 'Option_C' : row.option_c, 'Option_D' : row.option_d, 'Answer' : row.answer}
        df = df.append(var, ignore_index = True)
    return render_template('test_temp.html')



@app.route('/quiz', methods = ['GET', 'POST'])
@login_required
def quiz():
    global df
    global num
    global count
    num += 1
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'certificate.jpg')
    content = "Hello Ramkumar..... Your gmail is going Hack soon....."
    message = content+'\n'+pic1
    print(df)
    q = df['Question'].tolist()
    op_1 = df['Option_A'].tolist()
    op_2 = df['Option_B'].tolist()
    op_3 = df['Option_C'].tolist()
    op_4 = df['Option_D'].tolist()
    ans = df['Answer'].tolist()
    #if(num == 1):
        #return render_template('quest_temp.html', ques=q, op1=op_1, op2=op_2, op3=op_3, op4=op_4, n=num)
    if(num <= 6):
        for i in range(len(ans)):
            if(str(i) in request.form.keys() and request.form[str(i)] == str(ans[i])):
                print("R"*30)
                print(request.form[str(i)], ans[i])
                count += 1
        print('Count is',count)
        return render_template('quest_temp.html', ques=q, op1=op_1, op2=op_2, op3=op_3, op4=op_4, n=num)
    else:
        num = 0
        c = count
        count = 0
        if c > 3:
            remark = "Excellent"
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login("eramkumar94@gmail.com","9550361900")
            server.sendmail("eramkumar94@gmail.com","eetakota.ramkumar@gmail.com",message)
			# msg = Message(sender="eramkumar94@gmail.com", recipients = MAIL)
			# msg.body = "Hi This is Ram. Cooooolllll!!!!!!!!"
			# email.send(msg)

        else:
            remark = "Better Luck Next Time"
        return render_template('score_temp.html', remark = remark, name = 'Ramkumar', count = c)



@app.route('/view', methods = ['GET', 'POST'])
def question_bank():
    if request.method == "GET":
        return render_template('view.html', query=Quiz.query.all())
    return render_template("view.html", query=Quiz.query.all())


if __name__ == '__main__':
    app.run(debug=True)
