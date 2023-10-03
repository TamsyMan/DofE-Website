from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def siteOpened():
    return render_template('index.html')


@app.route('/', methods = ["GET", "POST"])
def calculate():
    if request.method == "POST":
        number1 = request.form('number1')
        calc = request.form('calc')
        number2 = request.form('number2')
        print (number1)
        if calc == "+":
            print (number1 + number2)
        elif calc == "-":
            print (number1 - number2)
        elif calc == "*":
            print (number1*number2)
        elif calc == "/":
            print (number1/number2)
        else:
            print ("Not a valid sum")
        return render_template('index.html')


app.run()