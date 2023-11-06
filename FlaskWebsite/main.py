from flask import Flask, request, render_template
from forms import CalcForm


app = Flask(__name__)

@app.route('/')
def initialise():
    return render_template('index.html')


@app.route('/calculator')
def calculator():
    form = CalcForm(request.form)
    return render_template('calculator.html', form=form)

@app.route('/calcresult', methods = ["POST"])
def calcResult():
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
        return render_template('calcresult.html', result=result)
    except KeyError as error:
        return "Missing Form Field"

app.run(debug=True)