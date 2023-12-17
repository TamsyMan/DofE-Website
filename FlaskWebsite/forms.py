from wtforms import Form, IntegerField, StringField, SubmitField

class CalcForm(Form):
    Number1=IntegerField('Number 1')
    Calculation=StringField('Calculation')
    Number2=IntegerField('Number 2')
    Submit=SubmitField('Submit')

class YoutubeForm(Form):
    topic = StringField('Topic')
    submit=SubmitField('Submit')