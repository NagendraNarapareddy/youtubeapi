from flask import Flask, render_template, request, jsonify
from youtubeapi import get_channel_id_by_handle, get_videos_from_channel, get_video_details, filter_shorts,youtube_api_client

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    channel_handle = request.form.get("channel_handle")

    # Get the channel ID
    channel_id = get_channel_id_by_handle(channel_handle)
    if not channel_id:
        return jsonify({"error": "Channel not found"}), 404

    # Get videos and filter Shorts
    videos = get_videos_from_channel(channel_id)
    shorts = filter_shorts(videos)

    return jsonify(shorts)

if __name__ == "__main__":
    app.run(debug=True)