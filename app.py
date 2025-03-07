import subprocess
import json
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "API de Extração de Vídeos do YouTube está rodando!"})

@app.route("/channel/<channel_handle>")
def get_all_videos(channel_handle):
    """Obtém todos os vídeos de um canal, incluindo Shorts e vídeos normais"""
    try:
        # URL da aba "Vídeos" do canal (contém TODOS os vídeos)
        uploads_url = f"https://www.youtube.com/@{channel_handle}/videos"

        result = subprocess.run(
            ["yt-dlp", "--flat-playlist", "-J", uploads_url],
            capture_output=True,
            text=True
        )

        data = json.loads(result.stdout)
        video_list = [{"videoId": entry["id"], "title": entry["title"]} for entry in data.get("entries", [])]

        return jsonify({"channel": channel_handle, "videos": video_list})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/playlist/<playlist_id>")
def get_playlist_videos(playlist_id):
    """Obtém todos os vídeos de uma playlist"""
    try:
        playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"

        result = subprocess.run(
            ["yt-dlp", "--flat-playlist", "-J", playlist_url],
            capture_output=True,
            text=True
        )

        data = json.loads(result.stdout)
        video_list = [{"videoId": entry["id"], "title": entry["title"]} for entry in data.get("entries", [])]

        return jsonify({"playlist": playlist_id, "videos": video_list})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
