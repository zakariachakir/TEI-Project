from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

csrf = CSRFProtect()

class ContactForm(FlaskForm):
    style = {'class': 'ourClasses', 'style': 'height:250px;'}
    style1 = {'class': 'ourClasses', 'style': 'width:15%; height:30px'}
    message = TextAreaField('Coller le contenu du fichier JSON ici :', validators=[DataRequired('Veillez remplir ce champ')],
                            render_kw=style)
    nombre = StringField('Donner le nombre de chapitres contenu dans votre sommaire :', validators=[DataRequired('Veillez remplir ce champ')],
                       render_kw=style1)
    submit = SubmitField("Transformer en XML-TEI")