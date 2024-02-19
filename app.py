from flask import Flask, redirect, request, session, url_for, render_template, jsonify
import requests
from queue_agent import CustomAgent
from queue_agent import SpotifyAgentRunner
from spotify_interface import SpotifyInterface
import json

# Your Spotify App Credentials
spotify_helper = SpotifyInterface()
CLIENT_ID, CLIENT_SECRET = spotify_helper.get_client_info()

REDIRECT_URI = "http://localhost:3000/callback"

# Spotify URLs
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

app = Flask(__name__)
app.secret_key = 'your_random_secret_key'  # Replace with your secret key

@app.route('/')
def index():
    if 'access_token' in session:
        # Pass the access token to the logged_in template
        print("Access Token:", session.get('access_token'))
        return render_template('logged_in.html', access_token=session['access_token'])
    else:
        # Define the login URL here for clarity and pass it to the template
        login_url = url_for('login', _external=True)
        return render_template('welcome.html', login_url=login_url)

@app.route('/login')
def login():
    scope = "playlist-modify-public streaming"
    return redirect(f"{SPOTIFY_AUTH_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={scope}")

@app.route('/callback')
def callback():
    code = request.args.get('code')
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=payload)
    token_info = post_request.json()
    if 'access_token' in token_info:
        session['access_token'] = token_info['access_token']
        return redirect(url_for('index'))
    else:
        return "Error retrieving access token from Spotify", 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/get_next_track')
def get_next_track():
    spotify = spotify_helper.get

@app.route('/update_queue')
def update_queue():
    queue_json = request.args.get('queue')
    messages_json = request.args.get('messages')
    
    # Convert JSON strings to Python objects
    queue = json.loads(queue_json)
    messages = json.loads(messages_json)
    print(queue)
    print(messages)
    
    agent = SpotifyAgentRunner()
    updated_queue,messsages = agent.main(queue, messages)
    
    # Assuming updated_queue is a list of track URIs
    print("UPDATE")
    print(updated_queue)
    return jsonify({"updated_queue": updated_queue, "messages": messages})
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
