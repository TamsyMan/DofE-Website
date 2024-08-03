import random

from flask import Flask, request, render_template
from forms import CalcForm, YoutubeForm, TicTacToeForm
import requests
import googleapiclient.discovery
import os
from dotenv import load_dotenv

load_dotenv()
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
        youtube = googleapiclient.discovery.build("youtube", "v3",
                                                  developerKey=(os.getenv("YOUTUBE_API_KEY")))

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
        return render_template('video.html', form=form)


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
        except KeyError:
            return "Missing Form Field"
    return render_template('calculator.html', form=form, result=result)


game_assets = {
    "0,0": {"location": "0,0", "x": "0", "y": "0", "Status": " "},
    "0,1": {"location": "0,1", "x": "0", "y": "1", "Status": " "},
    "0,2": {"location": "0,2", "x": "0", "y": "2", "Status": " "},
    "1,0": {"location": "1,0", "x": "1", "y": "0", "Status": " "},
    "1,1": {"location": "1,1", "x": "1", "y": "1", "Status": " "},
    "1,2": {"location": "1,2", "x": "1", "y": "2", "Status": " "},
    "2,0": {"location": "2,0", "x": "2", "y": "0", "Status": " "},
    "2,1": {"location": "2,1", "x": "2", "y": "1", "Status": " "},
    "2,2": {"location": "2,2", "x": "2", "y": "2", "Status": " "},
    "player": "X",
    "game_over": False,
    "winner": None
}


@app.route('/TicTacToe', methods=["GET", "POST"])
def TicTacToe():
    global game_assets
    form = TicTacToeForm(request.form)
    game_over = game_assets["game_over"]
    winner = game_assets["winner"]
    message = None
    while True:
        if not game_over:
            if game_assets["0,0"]["Status"] != " " and game_assets["0,1"]["Status"] != " " and game_assets["0,2"]["Status"] != " " and game_assets["1,0"]["Status"] != " " and game_assets["1,1"]["Status"] != " " and game_assets["1,2"]["Status"] != " " and game_assets["2,0"]["Status"] != " " and game_assets["2,1"]["Status"] != " " and game_assets["2,2"]["Status"] != " " and winner is None:
                message = "This is a draw. Neither player wins."
            if request.method == "POST":
                move = request.form["move"]
                if game_assets[move]["Status"] == " ":
                    turn_to_move = game_assets["player"]
                    game_assets[move]["Status"] = turn_to_move
                    if turn_to_move == "O":
                        turn_to_move = "X"
                    else:
                        turn_to_move = "O"
                    game_assets["player"] = turn_to_move
                elif message != "This is a draw. Neither player wins.":
                    message = "A tile is already there. Try again."
                if ((game_assets["0,0"]["Status"] == game_assets["1,1"]["Status"] == game_assets["2,2"]["Status"]) and game_assets["1,1"]["Status"] != " ") or ((game_assets["0,2"]["Status"] == game_assets["1,1"]["Status"] == game_assets["2,0"]["Status"]) and game_assets["1,1"]["Status"] != " "):
                    winner = game_assets['1,1']['Status']
                    game_assets["winner"] = winner
                    game_assets["game_over"] = True
                for col in range(0, 3):
                    column_statuses = [
                        game_assets[f"{row},{col}"]["Status"]
                        for row in range(3)]
                    if all(status == column_statuses[0] and status != " " for status in column_statuses):
                        winner = column_statuses[0]
                        game_assets["winner"] = winner
                        game_assets["game_over"] = True
                for row in range(0, 3):
                    row_statuses = [
                        game_assets[f"{row},{col}"]["Status"]
                        for col in range(3)]
                    if all(status == row_statuses[0] and status != " " for status in row_statuses):
                        winner = row_statuses[0]
                        game_assets["winner"] = winner
                        game_assets["game_over"] = True
        else:
            message = f"Game Over. {winner} is the winner"

        return render_template('TicTacToe.html', game_assets=game_assets, form=form, message=message)


app.run(debug=True)
