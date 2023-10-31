from flask import Flask, request, render_template


app = Flask(__name__)

@app.route('/')
def initialise():
    return(render_template('index.html'))
@app.route('/calculator', methods = ["POST"])
def calculate():
    try:
        number1 = int(request.form["number1"])
        calc = request.form["calc"]
        number2 = int(request.form["number2"])
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