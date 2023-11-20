from flask import Flask, request, render_template, jsonify
from forms import CalcForm
import requests


app = Flask(__name__)



@app.route('/')
def initialise():
    return render_template('index.html')


@app.route('/test', methods = ["GET", "POST"])
def get_data():
    data = {'key': 'value'}
    return jsonify(data)

@app.route('/calculator',  methods = ['GET', 'POST'])
def calculator():
    form = CalcForm(request.form)
    result = None
    if request.method == "POST":
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
        except KeyError as error:
            return "Missing Form Field"
    return render_template('calculator.html', form=form, result=result)



app.run(debug=True)

