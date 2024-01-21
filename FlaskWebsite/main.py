import random

from flask import Flask, request, render_template
from forms import CalcForm, YoutubeForm
import requests
import googleapiclient.discovery

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

    all_info = {"date": date, "time": time, "hour": hour, "min": minute, "second": second, "year": year, "month": month,
                "day": day, "weekday": weekday}

    return all_info


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
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    month = find_time()["month"]
    month = months[int(month) - 1]
    return month


@app.route('/')
def initialise():
    return render_template('index.html')


@app.route("/video", methods=["GET", "POST"])
def video():
    form = YoutubeForm(request.form)
    video_play = None
    video_ids = []

    if request.method == "POST":
        search_term = request.form["topic"]
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey="AIzaSyDlxNmbWJTuecjrOXVoAr-Ah9euV-qK4tE")

        search_response = youtube.search().list(q=search_term, type="video", part="id", maxResults=25).execute()

        for item in search_response.get("items", []):
            video_ids.append(item["id"]["videoId"])

        if video_ids:
            random_num = random.randint(0, 24)
            random_video_id = video_ids[random_num]
            video_play = f"https://www.youtube.com/embed/{random_video_id}"

    if video_play:
        return render_template('video.html', video_play=video_play, form=form)
    else:
        return render_template('video.html',form=form)


@app.route('/clock', methods=["GET", "POST"])
def clock():
    time = find_time()["time"]
    day = find_time()["day"]
    month = month_calculator()
    year = find_time()["year"]
    suffix = date_suffix_calculator()
    weekday = find_time()["weekday"]
    final_string = f"It is {time} on the {day}{suffix} of {month}, {year}. It is a {weekday}."

    return render_template('clock.html', final_string=final_string)


@app.route('/calculator', methods=['GET', 'POST'])
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

@app.route('/TicTacToe', methods = ["GET", "POST"])

def TicTacToe():

    parts_of_board = {
        "0,0": {"location": "0,0", "x": "0", "y": "0", "Status": " "},
        "0,1": {"location": "0,1", "x": "0", "y": "1", "Status": " "},
        "0,2": {"location": "0,2", "x": "0", "y": "2", "Status": " "},
        "1,0": {"location": "1,0", "x": "1", "y": "0", "Status": " "},
        "1,1": {"location": "1,1", "x": "1", "y": "1", "Status": " "},
        "1,2": {"location": "1,2", "x": "1", "y": "2", "Status": " "},
        "2,0": {"location": "2,0", "x": "2", "y": "0", "Status": " "},
        "2,1": {"location": "2,1", "x": "2", "y": "1", "Status": " "},
        "2,2": {"location": "2,2", "x": "2", "y": "2", "Status": " "}}
    col_0 = []
    col_1 = []
    col_2 = []
    row_0 = []
    row_1 = []
    row_2 = []
    num_of_moves = 0
    game_over = False
    players = ["X", "O"]
    while True:
        if not game_over:
            x_or_o = num_of_moves % 2
            turn_to_move = players[x_or_o]
            row_play = input("Pick a row")
            column_play = input("Pick a column")
            move = row_play + "," + column_play
            if parts_of_board[move]["Status"] == " ":
                parts_of_board[move]["Status"] = turn_to_move
                num_of_moves = num_of_moves + 1
            else:
                print ("A tile is already there. Try again.")
            for i in range (0,3):
                for j in range (0,3):
                    square_to_print = f"{i},{j}"
                    print (parts_of_board[square_to_print]["Status"] + "|", end=" ")
                print ("\n -----")
            if ((parts_of_board["0,0"]["Status"] == parts_of_board["1,1"]["Status"] == parts_of_board["2,2"]["Status"]) and parts_of_board["1,1"]["Status"] != " ") or ((parts_of_board["0,2"]["Status"] == parts_of_board["1,1"]["Status"] == parts_of_board["2,0"]["Status"]) and parts_of_board["1,1"]["Status"] != " "):
                print(f"{parts_of_board['1,1']['Status']} Is the winner")
            # for i in range(0,3):
            #     column_check = i
            # for key, value in parts_of_board.items(c):
            #     if value["x"] = column_check:
            for i in range(0,3):
                column_values = []
                for col in range (0,3):
                    column_values.append(parts_of_board[f"{i}, {col}"]["Status"]"])




#                 Need to do win detection and add web framework







app.run(debug=True)
