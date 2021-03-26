import os
import random
import string
from xml.dom import minidom
import json as JS
from flask import Flask, render_template, request, send_file
import xml.etree.ElementTree as ET


from form import ContactForm, csrf

def randStr(chars = string.ascii_uppercase + string.digits, N=10):
	return ''.join(random.choice(chars) for _ in range(N))

app = Flask(__name__)
name = randStr(N=4)+'.xml'
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
csrf.init_app(app)


@app.route('/', methods=['POST', 'GET'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():        
        print('-------------------------')
        print(request.form['message'])
        print('-------------------------')
        data = JS.loads(request.form['message'])
        root = ET.Element("TEI")
        root.set("xmlns", "http://www.tei-c.org/ns/1.0")
        teiheader = ET.SubElement(root, "teiHeader")
        filedesc = ET.SubElement(teiheader, "fileDesc")
        titlestmt = ET.SubElement(filedesc, "titleStmt")
        ET.SubElement(titlestmt, "title").text = data['TEI']['teiHeader']['fileDesc']['titleStmt']['title']
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
        row = ET.SubElement(table, "row")
        for i in range(0, int(request.form['nombre'])):
            j = 0
            ET.SubElement(row, "cell").text = data["TEI"]["text"]["front"]["div"]["table"]["row"][i]["cell"][j]
            ET.SubElement(row, "cell").text = data["TEI"]["text"]["front"]["div"]["table"]["row"][i]["cell"][j+1]
        body = ET.SubElement(text, "body")
        ET.SubElement(body, "p").text = data["TEI"]["text"]["body"]["p"]

        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
        with open("C:/Users/aypax/PycharmProjects/Projet_Tei/Generated_xml_files/"+name, "w") as f:
             f.write(xmlstr)
        return render_template('views/success/success.html', name=name)

    return render_template('views/accueil/accueil.html', form=form)

@app.route('/download')
def downloadFile ():
    path ="C:/Users/aypax/PycharmProjects/Projet_Tei/Generated_xml_files/"+name
    return send_file(path, attachment_filename='xml_tei.xml', as_attachment=True)


@app.route('/success')
def success():
    return render_template('views/success/success.html')

def randStr(chars = string.ascii_uppercase + string.digits, N=10):
	return ''.join(random.choice(chars) for _ in range(N))

if __name__ == "__main__":
    app.run(debug=True)