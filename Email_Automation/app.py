from flask import Flask, request, render_template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
#import socketserver
import csv
import pandas as pd
from email.utils import formataddr
#from http.server import HTTPServer, BaseHTTPRequestHandler

app = Flask(__name__)
# https://www.google.com/settings/security/lesssecureapps
@app.route('/')
def index():
    return render_template("home.html")

# name with common certificate
# Common content and different names along with common File
@app.route('/mail', methods=['GET', 'POST'])
def mailing():
    if request.method == 'POST':
        mails_list = []
        file = request.form['upload-file']
        #print("FIle",file)
        df = pd.read_csv(file)
        #print(df)
        dic = dict(zip(df.mails,df.names))
        count= 1
        for i in dic:
            i = str(i)
            print(count," : ",i)
            fromaddr = request.form.get('sender')
            toaddr = i
            msg = MIMEMultipart() 
            msg['From'] = formataddr(("Innomatics Research Labs", fromaddr))
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
            filename = "Innomatics_IBM_Certification_Registration_ Step by Step Instructions.pdf"
            attachment = open("D:/Automations/Email_Automation/App/Innomatics_IBM_Certification_Registration_ Step by Step Instructions.pdf", "rb")
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
            count += 1
        confirm = 'Mail Has been sent'
    
        return render_template("home.html",confirm = confirm)
    

@app.route('/import',methods = ['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        mails_list = []
        file = request.form['upload-file']
        #print("FIle",file)
        df = pd.read_csv(file,encoding= 'unicode_escape')
        #print(df)
        dic = dict(zip(df.mails,df.names))
        count= 1
        for i in dic:
            
            i = str(i)
            print(count," : ",i)
            fromaddr = request.form.get('sender')
            toaddr = i
            msg = MIMEMultipart() 
            msg['From'] = formataddr(("Innomatics Research Labs", fromaddr))
            msg['To'] = toaddr
            msg['Subject'] = request.form.get('subject')
            f = request.form['upload-body']
            f = open(f,'r', encoding="utf8")
            read = f.read()
            body = read.format(dic[i])
            log = open("logs.csv",'a')
            log.write(str(i))
            log.write("\n")
            #print("Body :",body)
            msg.attach(MIMEText(body, 'html'))
            filename = str(dic[i])+".html"
            attachment = open("D:/Automations/Attendance_monthly/marks/"+str(dic[i])+".html", "rb")
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
            count += 1
        confirm = 'Mail Has been sent'
        return render_template("home.html", confirm = confirm)
# Common Content
# Mail for only bulk mails with common content 
# this function is for both common name and different names      
@app.route('/textmail', methods=['GET', 'POST'])
def text_mail():
    if request.method == 'POST':
        mails_list = []
        file = request.form['upload-file']
        print("FIle",file)
        #with open(file) as f:
         #   csvfile = csv.reader(f)
          #  print(csvfile)
           # for row in csvfile:
            #    mails_list.append(row[0])
        df = pd.read_csv(file)
        dic = dict(zip(df.mails,df.names))
        count = 1
        for i in dic:
            i = str(i)
            fromaddr = request.form.get('sender')
            toaddr = i
            print(count," : ",i)
            msg = MIMEMultipart() 
            msg['From'] = formataddr(("Innomatics Research Labs", fromaddr))
            msg['To'] = toaddr
            msg['Subject'] = request.form.get('subject')
            body = request.form.get('mailbody')
            body = body.format(i, dic[i]) # pass name in place of dic[i] for common name
            #print(body)
            msg.attach(MIMEText(body, 'html'))
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            pwd = request.form.get('password')
            s.login(fromaddr, pwd)
            text = msg.as_string()
            s.sendmail(fromaddr, toaddr, text)
            s.quit()
            count += 1
        confirm = 'Mail Has been sent'
    
        return render_template("home.html",confirm = confirm)

# Name & Certificate
# Mail with name and certificate
# Need to upload text file and .csv file
@app.route('/mail_with_names', methods=['GET', 'POST']) 
def mail_with_names():
    if request.method == 'POST':
        mails_list = []
        file = request.form['upload-file']
        #print("FIle",file)
        df = pd.read_csv(file,encoding= 'unicode_escape')
        #print(df)
        dic = dict(zip(df.mails,df.names))
        count= 1
        for i in dic:
            
            i = str(i)
            print(count," : ",i)
            fromaddr = request.form.get('sender')
            toaddr = i
            msg = MIMEMultipart() 
            msg['From'] = formataddr(("Innomatics Research Labs", fromaddr))
            msg['To'] = toaddr
            msg['Subject'] = request.form.get('subject')
            f = request.form['upload-body']
            f = open(f,'r', encoding="utf8")
            read = f.read()
            body = read.format(dic[i])
            log = open("logs.csv",'a')
            log.write(str(i))
            log.write("\n")
            #print("Body :",body)
            msg.attach(MIMEText(body, 'html'))
            filename = dic[i]+".pdf"
            attachment = open("D:/Automations/Certificate_name_edit/Internship/Data Science/AgenticAI_Internship_Feb_2026/OfferLetters/pdf/"+dic[i]+".pdf", "rb")
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
            count += 1
        confirm = 'Mail Has been sent'
    
        return render_template("home.html",confirm = confirm)

if __name__ == "__main__":
    app.run(debug=True)
    
    
 #ram.eetakota@innomatics.in ----------> gbiw cjba kuak dflg
 
 # operations@innomatics.in ---------> zbuu xvym pyju vxvm---------ncsy kgup yvoy ujhu
 # info@innomatics.in   --------------->   hbtg bzbd qsua uhaf
 
 # For creating app password click on below link
 # https://myaccount.google.com/signinoptions/twosv?rapt=AEjHL4MOGMjgwgrKNXfB5sANgSNk3Sslh2KZt60_tQkjj9r614E1M_b8V5hNMgnSShN2-AHkUvC4ArziZv7OiBQxMsVj0RKqSF1UDPt7EzPmSPM_7hFhyjE&pli=1