import os
from flask import Flask, render_template, request, redirect
import random
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate





from werkzeug.utils import redirect

app = Flask(__name__)
#SQL Alchemy Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir,'data.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


#Model Creation
class UrlShortner(db.Model):
    __tablename__ ="URL_Table"
    id = db.Column(db.Integer, primary_key = True)
    original = db.Column(db.Text)
    Shortened = db.Column(db.Text)

    def __init__(self, original, Shortened):
        self.original = original
        self.Shortened = Shortened
    




dummylist_1= ['a','b',"c", "d", "e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","1","2","3","4","5","6","7","8","9","0","_",'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
############################
@app.route('/')
def home_get():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def home_post():
    original_url = request.form.get('in_1')
    
    if original_url != None:
        if original_url !="":
            short_url = random.choice(dummylist_1) + random.choice(dummylist_1) +random.choice(dummylist_1) + random.choice(dummylist_1)
            
            k = UrlShortner.query.filter_by(original =original_url)
            print("KKKKKKK---",k)
            for i in k:
                print("original_url : ",i)
                if i.original ==original_url:
                    short_url= i.Shortened
                    return render_template('home.html', data=short_url)
        
            new_row = UrlShortner(original_url, short_url)
            db.session.add(new_row)
            db.session.commit()
            return render_template('home.html', data=short_url)
    return render_template('home.html')



@app.route('/history')
def history_get():
    data = UrlShortner.query.all()
    # s = UrlShortner.query.all()
    # for i in s:
    #     db.session.delete(i)
    #     db.session.commit()
    return render_template('history.html', data=data)

@app.route('/sh/<short>')
def fun(short):
    url_list1 = UrlShortner.query.filter_by(Shortened = short)
    print("url_list1 :",url_list1)
    for i in url_list1:
        print("url_list1###",i)
        if (i.Shortened) == short:
            print(i.original)
            return redirect(i.original)
        else:
            return "incorrect URL"
            
@app.route("/youtube")
def you():
    return redirect('https://www.youtube.com/results?search_query=rnn+deep+learning')

##############################


if __name__ == "__main__":
    app.run(debug=True)