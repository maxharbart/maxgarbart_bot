import telebot
import requests
import creditentials
from flask import Flask
from threading import Timer


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


api_call = 'https://api.openweathermap.org/data/2.5/weather?lat=54.710162&lon=20.510134&appid=' + creditentials.api_key

weather = requests.get(api_call)
data = weather.json()

bot = telebot.TeleBot(creditentials.bot_token)

app = Flask(__name__)

@app.route('/')
def send_messages(message): 
    
    text = 'https://api.telegram.org/bot' + creditentials.bot_token + '/sendMessage?chat_id=' + creditentials.chat_id + '&parse_mode=Markdown&text=Температура сейчас в Калининграде: ' + message + ' C'
            
    response = requests.get(text)
            
    return response.json()

timer = RepeatTimer(7200, send_messages, args=(str(int(data['main']['temp']) - 273)))
timer.start()                 


if __name__ == "__main__":
    app.run()
