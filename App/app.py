from flask import Flask, request, render_template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
#import socketserver
import csv
import pandas as pd
#from http.server import HTTPServer, BaseHTTPRequestHandler

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/mail', methods=['GET', 'POST'])
def mailing():
    fromaddr = request.form.get('sender')
    toaddr = request.form.get('receiver')
    msg = MIMEMultipart() 
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Tesing Mail"
    body = "Congratulations! You Got Shortlisted"
    msg.attach(MIMEText(body, 'plain'))
    filename = "file.pdf"
    attachment = open("D:/Ramkumar/Certificate_name_edit/DM/file.pdf", "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
       
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    pwd = request.form.get('password')
    s.login(fromaddr, pwd)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
    confirm = 'Mail Has been sent'
    
    return render_template("index.html",confirm = confirm)
    

@app.route('/import',methods = ['GET', 'POST'])
def importCsv():
    if request.method == 'POST':
        mails_list = []
        file = request.form['upload-file']
        print("FIle",file)
        with open(file) as f:
            csvfile = csv.reader(f)
            print(csvfile)
            for row in csvfile:
                mails_list.append(row[0])
        for i in mails_list:
            fromaddr = request.form.get('sender')
            toaddr = i
            msg = MIMEMultipart() 
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = request.form.get('subject')
            body = request.form.get('mailbody')
            msg.attach(MIMEText(body, 'plain'))
            filename = "file.pdf"
            attachment = open("D:/Ramkumar/Certificate_name_edit/DM/file.pdf", "rb")
            p = MIMEBase('application', 'octet-stream')
            p.set_payload((attachment).read())
            encoders.encode_base64(p)
               
            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            msg.attach(p)
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            pwd = request.form.get('password')
            s.login(fromaddr, pwd)
            text = msg.as_string()
            s.sendmail(fromaddr, toaddr, text)
            s.quit()
        confirm = 'Mail Has been sent'
        return render_template("index.html", confirm = confirm)

# Mail for only bulk mails with common content       
@app.route('/textmail', methods=['GET', 'POST'])
def text_mail():
    if request.method == 'POST':
        mails_list = []
        file = request.form['upload-file']
        print("FIle",file)
        with open(file) as f:
            csvfile = csv.reader(f)
            print(csvfile)
            for row in csvfile:
                mails_list.append(row[0])
        for i in mails_list:
            fromaddr = request.form.get('sender')
            toaddr = i
            msg = MIMEMultipart() 
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = request.form.get('subject')
            body = request.form.get('mailbody')
            msg.attach(MIMEText(body, 'plain'))
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            pwd = request.form.get('password')
            s.login(fromaddr, pwd)
            text = msg.as_string()
            s.sendmail(fromaddr, toaddr, text)
            s.quit()
        confirm = 'Mail Has been sent'
    
        return render_template("index.html",confirm = confirm)

# Mail with name and certificate
# Need to upload text file and .csv file
@app.route('/mail_with_names', methods=['GET', 'POST']) 
def mail_with_names():
    if request.method == 'POST':
        mails_list = []
        file = request.form['upload-file']
        #print("FIle",file)
        df = pd.read_csv(file)
        #print(df)
        dic = dict(zip(df.mails,df.names))
        for i in dic:
            fromaddr = request.form.get('sender')
            toaddr = i
            msg = MIMEMultipart() 
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = request.form.get('subject')
            f = request.form['upload-body']
            f = open(f,'r')
            read = f.read()
            body = read.format(dic[i])
            log = open("logs.csv",'a')
            log.write(i)
            log.write("\n")
            #print("Body :",body)
            msg.attach(MIMEText(body, 'plain'))
            filename = dic[i]+".pdf"
            attachment = open("D:/Ramkumar/Certificate_name_edit/workshop/jpg/pdf/"+dic[i]+".pdf", "rb")
            p = MIMEBase('application', 'octet-stream')
            p.set_payload((attachment).read())
            encoders.encode_base64(p)
               
            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            msg.attach(p)
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            pwd = request.form.get('password')
            s.login(fromaddr, pwd)
            text = msg.as_string()
            s.sendmail(fromaddr, toaddr, text)
            s.quit()
        confirm = 'Mail Has been sent'
    
        return render_template("index.html",confirm = confirm)

if __name__ == "__main__":
    app.run(debug=True)
    
    
   
    