from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

csrf = CSRFProtect()

class ContactForm(FlaskForm):
    message = TextAreaField('Coller le contenu du fichier JSON ici :', validators=[DataRequired('Veillez remplir ce champ')])
    submit = SubmitField("Transformer en XML-TEI")