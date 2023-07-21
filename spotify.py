import spotipy
from spotipy.oauth2 import SpotifyOAuth
import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import TkinterDnD
import ctypes

SPOTIPY_CLIENT_ID = '82b7de3b38484b179a73520cbca9863c'
SPOTIPY_CLIENT_SECRET = 'e36ac0943bd8442fb93e62249575129f'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080/callback'  # e.g., http://localhost:8080/callback

# Create a spotipy client with OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope="playlist-modify-private"
))


# Map mood strings to corresponding energy levels (float values between 0 and 1)
MOODS = {
    'happy': 0.8,
    'sad': 0.2,
    'energetic': 1.0,
    'chill': 0.5,
    'aggressive': 0.9,
    'peaceful': 0.4,
    'excited': 0.95,
    'reflective': 0.6,
    'dark': 0.1,
    'dreamy': 0.45,
    # Add more mood-energy mappings as needed
}

# List of suggested genres
SUGGESTED_GENRES = [
    'pop',
    'rock',
    'hip-hop',
    'jazz',
    'classical',
    'country',
    'electronic',
    'reggae',
    'indie',
    # Add more genres as needed
]


def get_energy_level(mood):
    # Get the level for entered mood
    return MOODS.get(mood.lower(), None)  # Return None if the mood is not found


def get_valid_genre_input():
    print("\nPossible genres: " + ", ".join(SUGGESTED_GENRES))
    print("-----------------------------------")
    while True:
        genre = input("Enter your preferred genre: ").lower().strip()

        if genre in SUGGESTED_GENRES:
            return genre
        else:
            print("Invalid genre. Please choose from the suggested genres.\n")
            print(", ".join(SUGGESTED_GENRES))
            print("-----------------------------------")

def get_valid_mood_input():
    while True:
        mood = input("Enter your mood (select from the list above): ").lower()
        if mood in MOODS:
            return mood
        else:
            print("Invalid mood. Please choose from the list of possible moods:\n")
            print(", ".join(MOODS.keys()))
            print("-----------------------------------")


def create_playlist(mood, genre, num_tracks):
    energy_level = get_energy_level(mood)

    if energy_level is None:
        print("Invalid mood. Please choose one of the following moods:")
        print(", ".join(MOODS.keys()))
        print("-----------------------------------")
        return None

    # Limit the number of tracks between 10 and 100 (inclusive)
    num_tracks = max(10, min(num_tracks, 100))

    # Get a list of track IDs based on mood and genre
    tracks = sp.recommendations(seed_genres=[genre], target_energy=energy_level, limit=num_tracks)
    track_ids = [track['id'] for track in tracks['tracks']]

    # Get user's Spotify username
    user_info = sp.current_user()
    user_id = user_info['id']

    # Create a new playlist
    playlist = sp.user_playlist_create(user_id, name=f"{mood.capitalize()} {genre.capitalize()} Playlist", public=False)

    # Add tracks to the playlist
    sp.playlist_add_items(playlist['id'], track_ids)

    return playlist['external_urls']['spotify']

def show_playlist_url(mood, genre, url):
    # Force the dialog box to be shown on top
    ctypes.windll.user32.SetForegroundWindow(ctypes.windll.kernel32.GetConsoleWindow())

    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Playlist Created", f"Your playlist has been created!\n\n\"{mood.capitalize()} {genre.capitalize()}\" is now in your playlists!", parent=root)



def main():
    print("Possible moods: happy, sad, energetic, chill, aggressive, peaceful, excited, reflective, dark, dreamy")
    print("-----------------------------------")

    while True:
        mood = get_valid_mood_input().lower().strip()
        genre = get_valid_genre_input().lower().strip()

        while True:
            try:
                num_tracks = int(input("Enter the number of songs for the playlist (10-50): "))
                if num_tracks < 10 or num_tracks > 50:
                    print("Invalid number of songs. Please enter a value between 10 and 50.")
                    print("-----------------------------------")
                else:
                    playlist_url = create_playlist(mood, genre, num_tracks)  # Move the function call here
                    if playlist_url:
                        show_playlist_url(mood, genre, playlist_url)  # Pass mood, genre, and playlist_url as arguments
                    return  # Exit the loop after creating the playlist
            except ValueError:
                print("Invalid input. Please enter a number.")
                print("-----------------------------------")

if __name__ == "__main__":
    main()






