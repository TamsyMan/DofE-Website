from flask import Flask, request, render_template, jsonify
from forms import CalcForm
import requests


app = Flask(__name__)


def find_time():
    api_url = 'http://worldtimeapi.org/api/ip'
    response = requests.get(api_url)
    data = response.json()

    datetime = data.get("datetime")
    date_and_time = datetime.split("T")
    date = date_and_time[0]
    time = date_and_time[1]
    time = time.split(".")
    time = time[0]
    parts_of_date = date.split("-")
    parts_of_time = time.split(":")
    hour = parts_of_time[0]
    minute = parts_of_time[1]
    second = parts_of_time[2]
    year = parts_of_date[0]
    month = parts_of_date[1]
    day = parts_of_date[2]

    days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    weekday = days_of_week[data.get("day_of_week")]

    all_info = {"date": date, "time": time, "hour": hour, "min": minute, "second": second,"year": year, "month": month, "day": day, "weekday": weekday}

    return all_info

@app.route('/')
def initialise():
    return render_template('index.html')

def date_suffix_calculator():
    day = find_time()["day"]
    if day[-1] == "1" and day != "11":
        suffix = "st"
    elif day[-1] == "2" and day != "12":
        suffix = "nd"
    elif day[-1] == "3" and day != "13":
        suffix = "rd"
    else:
        suffix = "th"

    return suffix

def month_calculator():
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December']
    month = find_time()["month"]
    month = months[int(month)-1]
    return month
@app.route('/clock', methods = ["GET", "POST"])
def clock():
    time = find_time()["time"]
    day = find_time()["day"]
    month = month_calculator()
    year = find_time()["year"]
    suffix = date_suffix_calculator()
    weekday = find_time()["weekday"]
    final_string = f"It is {time} on the {day}{suffix} of {month}, {year}. It is a {weekday}."

    return render_template('clock.html', final_string = final_string)

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

