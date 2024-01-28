from wtforms import Form, IntegerField, StringField, SubmitField, SelectField




class CalcForm(Form):
    Number1 = IntegerField('Number 1')
    Calculation = StringField('Calculation')
    Number2 = IntegerField('Number 2')
    Submit = SubmitField('Submit')


class YoutubeForm(Form):
    topic = StringField('Topic')
    submit = SubmitField('Submit')


class TicTacToeForm(Form):

    move = SelectField('Move', choices=[('0,0', '0,0'), ('0,1', '0,1'), ('0,2', '0,2'), ('1,0', '1,0'), ('1,1', '1,1'), ('1,2', '1,2'), ('2,0', '2,0'), ('2,1', '2,1'), ('2,2', '2,2')]
)
    submit = SubmitField('Submit')
