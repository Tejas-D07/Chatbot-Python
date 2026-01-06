from flask import Flask, render_template, request, jsonify
import random
from datetime import datetime
import requests
import os

app = Flask(__name__)

UNSPLASH_ACCESS_KEY = "jZrruxHP6feUcXxb4S-nChaYx0ooFx-7ogpB0PXhTR0"
NEBIUS_API_KEY = "v1.CmQKHHN0YXRpY2tleS1lMDBreDR6MnNqZ3pmZTRzY2cSIXNlcnZpY2VhY2NvdW50LWUwMGsyaGVyemJnZGU2YTNreDIMCIXKtcoGEIHf4fEBOgwIg83NlQcQgPz0iANAAloDZTAw.AAAAAAAAAAEAnIK23oOADKBzyJeBejV2ZjvxrZkgQMvI5MOuCYdzLjlPmlc94SwTfJw-AsTV4Tcrr0wzlvBvtfoHuV_dTpsH"

def play_game(user_choice):
    options = ["rock", "paper", "scissors"]
    bot_choice = random.choice(options)
    result = f"You chose {user_choice}, I chose {bot_choice}. "
    if user_choice == bot_choice:
        result += "It's a tie! 😐"
    elif (user_choice == "rock" and bot_choice == "scissors") or \
         (user_choice == "paper" and bot_choice == "rock") or \
         (user_choice == "scissors" and bot_choice == "paper"):
        result += "You win! 🎉"
    else:
        result += "I win! 😎"
    return result

def get_unsplash_image(query):
    url = "https://api.unsplash.com/photos/random"
    headers = {
        "Accept-Version": "v1",
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
    }
    params = {
        "query": query,
        "orientation": "landscape"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data["urls"]["regular"]
    except Exception as e:
        print(f"Unsplash API error: {e}")
        return "https://placekitten.com/200/200"

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        return f"🌤️ The current weather in {city.title()} is {temp}°C with {desc}."
    except requests.RequestException as e:
        return "⚠️ Failed to fetch weather. Please try again later."

def generate_logo(prompt_text):
    try:
        url = "https://api.studio.nebius.com/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {NEBIUS_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "black-forest-labs/flux-schnell",
            "prompt": prompt_text
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        image_url = response.json()['data'][0]['url']
        return image_url
    except Exception as e:
        print("🔴 Logo generation failed:", e)
        return None

small_talk = [
     "Sorry i didn't understand that.",
    "Let's do something fun! Try /joke or /game 🎲"
]

def get_bot_response(message):
    msg = message.lower().strip()

    if any(greet in msg for greet in ["hi", "hey","hello"]):
        return random.choice([
            "Hey there! 👋 Type /help to explore. 🌟",
            "Hello, friend! 😊 I'm excited to chat! 💬"
        ])

    if "help" in msg:
        return (
            "👉 joke - Funny joke<br>"
            "👉 fact - Random fact<br>"
            "👉 game - Play rock-paper-scissors<br>"
            "👉 snake - Play Snake Game 🐍<br>"
            "👉 rock/paper/scissors ✊📄✂- Play move<br>"
            "👉 quote - Motivational quote 🚀<br>"
            "👉 riddle - Fun riddle 🧠<br>"
            "👉 image [bird|animal|place] - Show image<br>"
            "👉 hug - Virtual hug 🤗<br>"
            "👉 play song - Stream from Spotify 🎵"
        )

    if "joke" in msg:
        jokes = [
            "Why don’t scientists trust atoms? They make up everything! 😂",
            "Why did the computer visit the doctor? It had a virus! 🦠",
            "What do you call fake spaghetti? An impasta! 🍝"
        ]
        return random.choice(jokes)

    if "generate" in msg and "logo" in msg and "named" in msg:
        try:
            name = msg.split("named")[-1].strip()
            prompt = f"A high quality logo design for a brand named '{name}'"
            logo_url = generate_logo(prompt)
            if logo_url:
                return f"Here is your logo:<br><img src='{logo_url}' alt='logo' style='max-width:100%; border-radius:10px;' />"
            else:
                return "⚠️ Logo generation failed. Please try again later."
        except Exception as e:
            return f"Error: {e}"

    if "fact" in msg:
        facts = [
            "Octopuses have three hearts. 🐙",
            "Honey never spoils. 🍯",
            "Bananas are berries, but strawberries aren't. 🍌🍓",
            "Wombat poop is cube-shaped. 💩",
            "Sloths can hold their breath longer than dolphins! 🦥"
        ]
        return random.choice(facts)

    if "quote" in msg:
        quotes = [
            "Believe you can and you're halfway there. 💪",
            "Keep going, you’re doing great! 🌟",
            "Dream big and dare to fail. 🚀",
            "You are stronger than you think. 💖",
            "Every day is a fresh start. 🌅"
        ]
        return random.choice(quotes)

    if "play game" in msg:
     return "Play Rock-Paper-Scissors here: <a href='/game' target='_blank'>🎮 Start Game</a>"

    if msg in ["rock", "paper", "scissors"]:
        return play_game(msg)

    if "riddle" in msg:
        riddles = [
            "What has keys but can't open locks? — A piano 🎹",
            "What can you catch but not throw? — A cold 🤧",
            "What has a face and two hands but no arms or legs? — A clock 🕰️"
        ]
        return random.choice(riddles)

    if "funny" in msg:
        funny = [
            "I'm reading a book on anti-gravity. It's impossible to put down! 😂",
            "Why don't skeletons fight each other? They don't have the guts.",
            "I told my computer I needed a break, and it said no problem—it needed one too!",
            "Parallel lines have so much in common. It’s a shame they’ll never meet."
        ]
        return random.choice(funny)

    if "hug" in msg:
        return "Here's a big warm hug just for you! 🤗💖"

    if "how are you" in msg:
        return random.choice([
            "I'm great, thanks! 😊",
            "Doing awesome! 🌟"
        ])

    if "date" in msg:
        return f"Today's date is {datetime.now().strftime('%A, %B %d, %Y')}."

    if "time" in msg:
        return f"The current time is {datetime.now().strftime('%I:%M %p')}."

    if "song" in msg:
        return "Click here to open Spotify: <a href='https://open.spotify.com/' target='_blank'>Spotify 🎵</a>"



    if "image" in msg:
        words = msg.split()
        try:
            idx = words.index("image")
            if idx + 1 < len(words):
                query = words[idx + 1]
            else:
                query = "random"
        except ValueError:
            query = "random"
        image_url = get_unsplash_image(query)
        return f"<img src='{image_url}' alt='{query}' style='max-width:100%; border-radius:12px; margin-top:10px;' />"

    if "weather" in msg:
        city = msg.replace("weather in", "").replace("weather", "").strip()
        if city:
            return get_weather(city)
        else:
            return "🌦️ Please specify a city, like 'weather in Mumbai'."

    if "snake game" in msg:
        return "Click here to play the Snake Game: <a href='/snake' target='_blank'>🐍 Play Snake</a>"

    if any(bye in msg for bye in ["bye", "goodbye", "see you"]):
        return "Bye! Have a great day! 👋😊"

    return random.choice([
        "Try something else",
        "Sorry, I can't understand",
        random.choice(small_talk)
    ])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    response = get_bot_response(user_input)
    return jsonify({"reply": response})

@app.route("/snake")
def snake_game():
    return render_template("snake.html")

@app.route("/test-logo")
def test_logo():
    test_prompt = "A futuristic esports logo with the name 'ShadowBlade' in neon sci-fi style"
    url = generate_logo(test_prompt)
    return jsonify({"logo_url": url or "Failed to generate"})

@app.route("/game")
def rps_game():
    return render_template("rps_game.html")

@app.route("/rps", methods=["POST"])
def rps_result():
    data = request.get_json()
    user_choice = data.get("choice", "")
    result = play_game(user_choice)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)