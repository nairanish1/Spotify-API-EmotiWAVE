import json
import random
from dotenv import load_dotenv  # To load environment variables from a .env file
import os
from requests import post, get  # For making HTTP requests
import webbrowser  # To control the browser
import numpy as np  # For numerical operations
import tensorflow as tf  # Machine learning library
from tensorflow import keras  # High-level neural networks API
from flask import Flask, request, redirect  # Flask web framework
from flask_cors import CORS  # Handling cross-origin resource sharing for Flask
import base64
import requests
# Load environment variables from a specific .env file
load_dotenv("/Users/anishnair/Spotify API - Emotiwave/.env")
# Get client ID and secret for Spotify API from environment variables
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Constants for Spotify authorization and API endpoints
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
REDIRECT_URI = "http://localhost:5001/callback"
SCOPE = "user-read-private user-read-email"
SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) 

@app.route("/")
def index():
    """Redirect user to Spotify for authentication."""
    auth_url = f"{SPOTIFY_AUTH_URL}?client_id={client_id}&response_type=code&redirect_uri={REDIRECT_URI}&scope=user-read-private%20user-read-email"
    return redirect(auth_url)

@app.route("/callback")
def callback():
    """Handle the redirect from Spotify authentication."""
    code = request.args.get('code')  # Get the authorization code from the query string
    if not code:
        # If there's no code, return an error message
        return "Error occurred: No authorization code returned"
    # Set up Flask app
    # 
 # Set up CORS for all origins
    
    access_token, refresh_token = get_tokens_from_code(code)  # Extract access and refresh tokens
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": client_id,
        "client_secret": client_secret
    } 
    response = post("https://accounts.spotify.com/api/token", data=token_data)
    token_json = response.json()
    access_token = token_json.get("access_token")
    refresh_token = token_json.get("refresh_token")
    return f"Access Token: {access_token} <br> Refresh Token: {refresh_token}"
    return "Successfully authenticated with Spotify."

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)

def direct_user_to_auth():
    auth_query_parameters = { 
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "client_id": client_id
    }
    url_args = "&".join(["{}={}".format(key, val) for key, val in auth_query_parameters.items()])
    auth_url = f"{SPOTIFY_AUTH_URL}/?{url_args}"
    webbrowser.open(auth_url)

def get_tokens_from_code(code):
    token_url = "https://accounts.spotify.com/api/token"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode('utf-8')
    }
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    response = requests.post(token_url, headers=headers, data=payload)
    
    # Handle the response
    if response.status_code == 200:
        data = response.json()
        return data['access_token'], data['refresh_token']
    else:
        # Error handling logic
        raise Exception("Failed to obtain tokens.")
    if not access_token or not refresh_token:
        print("Error fetching tokens:", json_result.get("error_description", "Unknown error"))
        exit()
    return access_token, refresh_token

def get_auth_header(token):
    """Returns the authorization header dictionary required for Spotify's API."""
    return {"Authorization": f"Bearer {token}"}

def get_audio_features(track_id, token):
    headers = get_auth_header(token)
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    result = get(url, headers=headers)
    audio_features = result.json()
    return audio_features

def get_track_info(track_id, token):
    headers = get_auth_header(token)
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    result = get(url, headers=headers)
    track_info = result.json()
    return track_info

def map_user_rating_to_metric(rating):
    threshold_increment = 0.76  
    return min(14, int(rating / threshold_increment) + 1)

def classify_track_mood_by_key(track_key):
    major_keys = {1, 2, 4, 5, 7, 9, 11, 13, 15, 17, 19}
    return "uplifting" if track_key in major_keys else "moody"

def adjust_spotify_parameters_based_on_metric(metric_score, tempo):
    base_value = 0.5
    adjustment = metric_score * 0.05
    
    if tempo == 'slow':
        adjustment = -adjustment
    
    return {
        'target_danceability': max(0, min(1, base_value + adjustment)),
        'target_energy': max(0, min(1, base_value + adjustment)),
        'target_valence': max(0, min(1, base_value + adjustment)),
        'target_acousticness': max(0, min(1, base_value - adjustment))
    } if tempo != 'mid-paced' else {key: base_value for key in ['target_danceability', 'target_energy', 'target_valence', 'target_acousticness']}

seed_artists = "SOME_ARTIST_ID"  # or some list or other value
seed_genres = "SOME_GENRE"       # or some list or other value
seed_tracks = "SOME_TRACK_ID"   # or some list or other value
target_size = 20                # or some other integer
market = "US"  
def fetch_spotify_recommendations(seed_artists=None, seed_genres=None, seed_tracks=None, 
                                  target_size=20, market=None, target_valence=None, 
                                  target_danceability=None, target_key=None, 
                                  min_tempo=None, max_tempo=None, target_energy=None, target_acousticness=None):
    token_url = "https://accounts.spotify.com/api/token"
    token_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    token_result = post(token_url, data=token_data).json()
    access_token = token_result.get("access_token")
    1
    headers = get_auth_header(access_token)
    recommendations_url = f"{SPOTIFY_API_BASE_URL}/recommendations"
    
    payload = {
        "seed_artists": seed_artists,
        "seed_genres": seed_genres,
        "seed_tracks": seed_tracks,
        "limit": target_size,
        "market": market,
        "target_valence": target_valence,
        "target_danceability": target_danceability,  # Added this line
        "target_key": target_key,
        "min_tempo": min_tempo,
        "max_tempo": max_tempo
    }
    return get(recommendations_url, headers=headers, params=payload).json().get('tracks', [])

keys_mapping = {
    'uplifting/happy': [1, 2, 4, 5, 7, 9, 11, 13, 15, 17, 19],
    'reflective/moody': [0, 3, 6, 8, 10, 12, 14, 16, 18]
} 
valid_tonal_choices = ['uplifting/happy', 'reflective/moody']
valid_tempo_choices = ['fast', 'mid-paced', 'slow']

# User rating input with validation
while True:
    try:
        user_rating = float(input("How are you feeling today from 0-10: "))
        if not 0 <= user_rating <= 10:
            raise ValueError("Rating should be between 0 and 10.")
        metric_score = map_user_rating_to_metric(user_rating)
        break  
    except ValueError as e:
        print(f"Invalid input: {e}")


def get_user_input(prompt, valid_choices):
    while True:
        response = input(prompt).lower()
        if response in valid_choices:
            return response
        print(f"Invalid choice. Please choose one of the following: {', '.join(valid_choices)}.")

tonal_preference = get_user_input("Do you prefer 'uplifting/happy' or 'reflective/moody'? ", valid_tonal_choices)
tempo_preference = get_user_input("Do you prefer something 'fast', 'mid-paced', or 'slow'? ", valid_tempo_choices)
target_key = random.choice(keys_mapping[tonal_preference])

params = adjust_spotify_parameters_based_on_metric(metric_score, tempo_preference)
params['target_key'] = target_key
spotify_recommendations = fetch_spotify_recommendations(seed_artists, seed_genres, seed_tracks, target_size, market, **params)

if spotify_recommendations:
    print("Spotify Recommendations:")
    for i, track in enumerate(spotify_recommendations):
        print(f"{i+1}. {track['name']} - {', '.join([artist['name'] for artist in track['artists']])}")

direct_user_to_auth()

# Replace with your authorization code
authorization_code = "BQAN4FYKUOAIU1SvlxcktoadYXENh93hrjECniGvgV0kb-ATq5XJq4XfLUrUWP_iHlvA-mbo9NGiqY-XyEUnXdlMgYptvIVfZTo1NH40kdT4Se5CBAqu8FjIbRCjhQlVZilgXbga9C2t6_IwZo-PFAEvmHNz5c5yc7bFeTFQCHoC-GRBQ0u5uUw731uRZH9nEA"

# Get access_token using the provided authorization_code
access_token, _ = get_tokens_from_code(authorization_code)

# Specify a track ID
track_id = "2MVQbDuhVs2muWFURtIdNb"

audio_features = get_audio_features(track_id, access_token)
track_info = get_track_info(track_id, access_token)

# Fetch Spotify recommendations based on seed artists and genres
seed_artists = ""  # Replace with your seed artists
seed_genres = ""  # Replace with your seed genres
seed_tracks = track_id  # Use the same track as seed track
target_size = 10
market = 'US'  # Replace with desired market
#this seems too complex for the user to understand. 

spotify_recommendations = fetch_spotify_recommendations(seed_artists, seed_genres, seed_tracks, target_size, market)


print("Spotify Recommendations:")
for index, track in enumerate(spotify_recommendations, 1):
    print(f"{index}. {track['name']} - {', '.join([artist['name'] for artist in track['artists']])}")

def adjust_spotify_parameters_based_on_metric(metric_score):
    base_value = min(0.0715 * metric_score, 1.0)

    return {
        "target_valence": base_value,
        "target_energy": base_value,
        "target_danceability": base_value,
        "target_acousticness": base_value
    }

params = adjust_spotify_parameters_based_on_metric(metric_score)
spotify_recommendations = fetch_spotify_recommendations(seed_artists, seed_genres, seed_tracks, target_size, market, **params)

print("Spotify Recommendations Based on Your Emotion:")
for index, track in enumerate(spotify_recommendations, 1):
    print(f"{index}. {track['name']} - {', '.join([artist['name'] for artist in track['artists']])}")
