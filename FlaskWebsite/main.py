from flask import Flask, request, render_template
from werkzeug.exceptions import BadRequestKeyError

app = Flask(__name__)

@app.route('/')
def initialise():
    return(render_template('index.html'))
@app.route('/calculator', methods = ["GET", "POST"])
def calculate():
    try:
        number1 = int(request.form["number1"])
        calc = request.form["calc"]
        number2 = int(request.form["number2"])
    except BadRequestKeyError as error:
        return "Missing Form Field"

    if calc == "+":
        result = (number1 + number2)
    elif calc == "-":
        result = (number1 - number2)
    elif calc == "*":
        result = (number1*number2)
    elif calc == "/":
        result = (number1/number2)
    else:
        print ("Not a valid sum")
    print (result)
    return render_template('index.html', result=result)



app.run(debug=True)