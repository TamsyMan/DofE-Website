from flask import Flask, request, render_template
from forms import CalcForm


app = Flask(__name__)

@app.route('/')
def initialise():
    form = CalcForm(request.form)
    return(render_template('index.html', form=form))
@app.route('/calculator', methods = ["POST"])
def calculate():
    try:
        number1 = int(request.form["Number1"])
        calc = request.form["Calculation"]
        number2 = int(request.form["Number2"])
        if calc == "+":
            result = (number1 + number2)
        elif calc == "-":
            result = (number1 - number2)
        elif calc == "*":
            result = (number1 * number2)
        elif calc == "/":
            result = (number1 / number2)
        else:
            result = "Not a valid sum"
        return render_template('calculator.html', result=result)
    except KeyError as error:
        return "Missing Form Field"

app.run(debug=True)