import subprocess
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "API de Extração de Vídeos do YouTube está rodando!"})

@app.route("/channel/<channel_url>")
def get_channel_videos(channel_url):
    """Obtém todos os IDs de vídeos de um canal"""
    try:
        result = subprocess.run(
            ["yt-dlp", "--flat-playlist", "-J", f"https://www.youtube.com/c/{channel_url}"],
            capture_output=True,
            text=True
        )
        data = json.loads(result.stdout)
        video_ids = [entry["id"] for entry in data.get("entries", [])]

        return jsonify({"channel": channel_url, "video_ids": video_ids})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/playlist/<playlist_id>")
def get_playlist_videos(playlist_id):
    """Obtém todos os IDs de vídeos de uma playlist"""
    try:
        result = subprocess.run(
            ["yt-dlp", "--flat-playlist", "-J", f"https://www.youtube.com/playlist?list={playlist_id}"],
            capture_output=True,
            text=True
        )
        data = json.loads(result.stdout)
        video_ids = [entry["id"] for entry in data.get("entries", [])]

        return jsonify({"playlist": playlist_id, "video_ids": video_ids})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
