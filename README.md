
                                          EmotiWAVE: Spotify Mood-Based Music Recommendation
Overview: 
EmotiWAVE is an intuitive music recommendation system powered by the Spotify API. Built with the core intention to enhance user experience by aligning song recommendations with the user's mood, EmotiWAVE stands out as an embodiment of how emotions and technology can converge to shape unique musical journeys.

Objective
At the heart of EmotiWAVE lies a simple yet profound goal: to fetch moods of users and provide them with Spotify music tracks that resonate with their emotions. By leveraging Spotify's robust API combined with advanced audio signal processing techniques, EmotiWAVE crafts a playlist that mirrors the user's feelings, be it joy, melancholy, excitement, or tranquility.

Key Features
User Mood Input: Fetches a mood score from users, allowing them to indicate their emotional state on a scale.
Audio Feature Extraction: Retrieves various audio features of tracks, such as danceability, energy, valence, and acousticness, from the Spotify API.
Dynamic Recommendation System: Dynamically adjusts the recommendation parameters based on the user's mood metric to curate a playlist that aligns with their emotional state.
OAuth 2.0 Authentication: Seamlessly integrates with Spotify's OAuth 2.0 system for secure access and fetching user-related data.
Intuitive User Interface: Guided interface that gently navigates users through the mood input process and swiftly presents them with a curated playlist.
Technical Stack
Languages & Libraries: Python, Flask, TensorFlow, NumPy.
API: Spotify API.
Middleware: Flask-CORS for handling CORS policies.
Environment Management: dotenv for environment variable management.
Getting Started
Pre-requisites:
Ensure you have Python3.x installed.
Spotify Developer account to fetch CLIENT_ID and CLIENT_SECRET.
Setup:
Clone this repository to your local machine.
Navigate to the project's root directory.
Load environment variables by placing them in a .env file and using:
bash
Copy code
load_dotenv("/path/to/.env/file")
Run:
Launch the Flask application using:
bash
Copy code
python main.py
Visit http://localhost:5001 to begin your musical journey!
API Endpoints:
/: Redirects the user to Spotify for authentication.
/callback: Handles the redirect from Spotify authentication and displays access and refresh tokens.
/recommendations: Fetches a list of recommended tracks from Spotify based on various seeds and target parameters.
Future Enhancements:
Emotion Detection from Speech: Integrate a deep learning model to detect user's emotion from their voice or speech, eliminating manual mood input.
More Granular Mood Mapping: Refine mood metrics to incorporate nuances of human emotions for even more personalized playlists.
Interactive UI: Implement a frontend framework to enhance user experience with visual mood indicators and animated playlist generation.
Built with ❤️ by [Your Name]. Feel free to raise issues or suggest enhancements.
