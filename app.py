from flask import Flask, redirect, request, session, url_for, render_template
import requests

# Your Spotify App Credentials
CLIENT_ID = "5945bee02e274a7daf17a1f7569063f3"
CLIENT_SECRET = "a828cbcf4df443fa854acb8aef8d164b"
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
