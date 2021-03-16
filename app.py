#!/usr/bin/python3
import os
from xml.dom import minidom
import json as JS
from flask import Flask, render_template, request, redirect, send_file
from flask_mail import Mail
import xml.etree.ElementTree as ET


from form_contact import ContactForm, csrf

mail = Mail()

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
csrf.init_app(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'zikochakir@gmail.com'
app.config['MAIL_PASSWORD'] = 'Chakirzakaria19980511'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail.init_app(app)

@app.route('/')
def index():
    return render_template('views/home/index.html')

@app.route('/contact', methods=['POST', 'GET'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():        
        print('-------------------------')
        print(request.form['message'])
        print('-------------------------')
        #send_message(request.form)

        data = request.form['message']
        root = ET.Element("TEI")
        root.set("xmlns", "http://www.tei-c.org/ns/1.0")
        teiheader = ET.SubElement(root, "teiHeader")
        filedesc = ET.SubElement(teiheader, "fileDesc")
        titlestmt = ET.SubElement(filedesc, "titleStmt")
        ET.SubElement(titlestmt, "title").text = data["TEI"]["teiHeader"]["fileDesc"]["titleStmt"]["title"]
        pubstmt = ET.SubElement(filedesc, "publicationStmt")
        ET.SubElement(pubstmt, "p").text = data["TEI"]["teiHeader"]["fileDesc"]["publicationStmt"]["p"]
        source = ET.SubElement(filedesc, "sourceDesc")
        ET.SubElement(source, "p").text = data["TEI"]["teiHeader"]["fileDesc"]["sourceDesc"]["p"]

        text = ET.SubElement(root, "text")
        front = ET.SubElement(text, "front")
        div = ET.SubElement(front, "div")
        div.set("type", "sommaire")
        ET.SubElement(div, "head").text = data["TEI"]["text"]["front"]["div"]["head"]
        table = ET.SubElement(div, "table")
        ET.SubElement(table, "head").text = data["TEI"]["text"]["front"]["div"]["table"]["head"]
        row1 = ET.SubElement(table, "row")
        row1.set("cols", "2")
        ET.SubElement(row1, "cell").text = data["TEI"]["text"]["front"]["div"]["table"]["row"][0]["cell"][0]
        ET.SubElement(row1, "cell").text = data["TEI"]["text"]["front"]["div"]["table"]["row"][0]["cell"][1]
        row2 = ET.SubElement(table, "row")
        ET.SubElement(row2, "cell").text = data["TEI"]["text"]["front"]["div"]["table"]["row"][1]["cell"]
        row3 = ET.SubElement(table, "row")
        ET.SubElement(row3, "cell").text = data["TEI"]["text"]["front"]["div"]["table"]["row"][2]["cell"][0]
        ET.SubElement(row3, "cell").text = data["TEI"]["text"]["front"]["div"]["table"]["row"][2]["cell"][1]
        body = ET.SubElement(text, "body")
        ET.SubElement(body, "p").text = data["TEI"]["text"]["body"]["p"]

        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
        with open("result1.xml", "w") as f:
             f.write(xmlstr)
        return redirect('/success')

    return render_template('views/contacts/contact.html', form=form)

@app.route('/download')
def downloadFile ():
    path ="C:/Users/aypax/PycharmProjects/contact-form-python-flask/voleur.xml"
    #For windows you need to use drive name [ex: F:/Example.pdf]
    return send_file(path, as_attachment=True)

@app.route('/success')
def success():
    return render_template('views/home/index.html')

# def send_message(message):
#     print(message.get('name'))
#
#     msg = Message(message.get('subject'), sender = message.get('email'),
#             recipients = ['id1@gmail.com'],
#             body= message.get('message')
#     )
#     mail.send(msg)

if __name__ == "__main__":
    app.run(debug = True)