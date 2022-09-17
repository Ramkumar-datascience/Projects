from myproject import app, db
from flask import render_template, redirect, request, url_for, session,Flask,flash
from flask_login import login_user
from myproject.models import Admin, NewLead
from myproject.forms import LoginForm, RegistrationForm, NewLeadForm
from werkzeug.security import check_password_hash
import csv
import pandas as pd
from flask_paginate import Pagination

#
# @app.route('/')
# def index():
#     return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print("Im Here")
        query = Admin.query.filter_by(email = form.email.data).first()
        if(query):
            msg = '***User already exists, kindly use another email'
            print(msg)
            return render_template('register.html', form=form, msg=msg)
        else:
            admin = Admin(email = form.email.data,
                        username = form.username.data,
                        password = form.password.data)
            db.session.add(admin)
            db.session.commit()

            print("#########",admin)
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=request.form.get('username')).first()
        if admin is not None and admin.check_password(request.form.get('password')):
            #Log in the user
            login_user(admin)
            #lead = NewLead.query.all()
            return redirect(url_for('page'))
            #return render_template('leads.html')
        else:
            msg = "Ivalid Username and Password"
            return render_template('login.html', form = form, msg = msg)
    else:
        return render_template('login.html', form=form)

@app.route('/pagination')
def page():
    page = request.args.get('page', 1, type=int)
    ROWS_PER_PAGE = 5
    lead = NewLead.query.order_by(NewLead.id.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)
    return render_template('leads.html',lead = lead)

@app.route('/newLead',methods = ['GET', 'POST'])
def newLead():
    form = NewLeadForm()
    if request.method == 'POST':
        newlead = NewLead(email = request.form.get('email'),
                    fullname = request.form.get('fullname'),
                    mobile = request.form.get('mobile'),
                    leadfrom = request.form.get('leadfrom'),
                    handleby = request.form.get('handleby'),
                    status = request.form.get('status'),
                    comment = request.form.get('comment'))
        db.session.add(newlead)
        db.session.commit()

        #lead = NewLead.query.all()
        print("New Lead added successfully")
        return redirect(url_for('page'))
    return redirect(url_for('page'))
    #return render_template('new_lead.html',form = form)

@app.route('/deleteLead',methods = ['GET', 'POST'])
def delete_lead():

    form = NewLeadForm()
    if request.method == 'POST':
        for getid in request.form.getlist('leadcheckbox'):
            print("Lead ID",getid)
            del_lead = NewLead.query.get(getid)
            print("lead query :",del_lead)
            db.session.delete(del_lead)
            db.session.commit()
            print("Deleted successfully")
        #lead = NewLead.query.all()
        return redirect(url_for('page'))
    return render_template('leads.html',lead=lead)

@app.route('/updateLead',methods = ['GET', 'POST'])
def update_lead():
    print("Im in Update function")
    form = NewLeadForm()
    if request.method == 'POST':
        updated_data = NewLead.query.get(request.form.get('id'))
        updated_data.email = request.form.get('email')
        updated_data.fullname = request.form.get('fullname')
        updated_data.mobile = request.form.get('mobile')
        updated_data.leadfrom = request.form.get('leadfrom')
        updated_data.handleby = request.form.get('handleby')
        updated_data.status = request.form.get('status')
        updated_data.comment = request.form.get('comment')

        db.session.commit()
    #lead = NewLead.query.all()
    return redirect(url_for('page'))

@app.route('/import',methods = ['GET', 'POST'])
def importCsv():
    print("Im in Import section")
    form = NewLeadForm()
    if request.method == 'POST':
        file = request.form['upload-file']
        print("FIle",file)
        with open(file) as f:
            csvfile = csv.reader(f)
            for row in csvfile:
                print("rrrrrrrow",row)
                updated_data = NewLead(
                email = row[1],
                fullname = row[2],
                mobile = row[3],
                leadfrom = row[4],
                handleby = row[5],
                status = row[6],
                comment = row[7]
                )
                db.session.add(updated_data)
                db.session.commit()
    #lead = NewLead.query.all()
    return redirect(url_for('page'))

@app.route('/LeadDetails',methods = ['GET', 'POST'])
def LeadDetails():
    form = NewLeadForm()
    print("im in lead details")
    if request.method == 'POST':
        form =  NewLead.query.filter(NewLead.fullname == request.form.get('fullname')).first()
        print("FORM", form)
        db.session.commit()
    return redirect(url_for('LeadDetails'))

if __name__ == '__main__':
    app.run(debug = True)
