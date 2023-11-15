from flask import Flask, request, render_template, jsonify
from forms import CalcForm
import requests


app = Flask(__name__)



@app.route('/')
def initialise():
    return render_template('index.html')


@app.route('/calculator', methods = ["GET", "POST"])
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

# @app.route('/api/clock', methods = ["GET", "POST"])
# def clock():
#     test = [
#         { "Name": "Test",
#           "Number": 1},
#         { "Name": "Test2",
#           "Number": 2}
#     ]
#     return jsonify(test)
@app.route('/clockapi', methods=['GET'])
def clockapi():
    response = requests.get('http://127.0.0.1:5000/clockapi')
    api_data = response.json()

    return render_template('clockapi.html', api_data=api_data)

