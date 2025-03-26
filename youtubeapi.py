import googleapiclient.discovery
import googleapiclient.errors

def youtube_api_client():
    api_service_name = "youtube"
    api_version = "v3"
    api_key = "AIzaSyCgAz3UR-wSB3c20Yw1ofM58r7sgk7l910"  # Replace with your YouTube Data API key
    
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)
    return youtube

def get_channel_id_by_handle(handle):
    youtube = youtube_api_client()
    request = youtube.search().list(
        part="snippet",
        q=handle,
        type="channel",
        maxResults=1
    )
    response = request.execute()
    if "items" in response and len(response["items"]) > 0:
        return response["items"][0]["id"]["channelId"]
    return None

def get_videos_from_channel(channel_id, max_results=10):
    youtube = youtube_api_client()
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=max_results,
        type="video"
    )
    response = request.execute()
    return response["items"]

def get_video_details(video_id):
    youtube = youtube_api_client()
    request = youtube.videos().list(
        part="contentDetails,snippet,player",
        id=video_id
    )
    response = request.execute()
    return response["items"][0] if "items" in response and response["items"] else None

def filter_shorts(videos):
    shorts_videos = []
    for video in videos:
        video_id = video["id"]["videoId"]
        details = get_video_details(video_id)
        if details:
            duration = details["contentDetails"]["duration"]
            title = details["snippet"]["title"].lower()
            description = details["snippet"].get("description", "").lower()
            embed_html = details["player"]["embedHtml"]

            is_shorts_embed = "shorts" in embed_html  # Shorts have a unique embed pattern

            if is_shorts_embed or (("PT" in duration and "M" not in duration) or "shorts" in title or "shorts" in description):
                shorts_videos.append({
                    "videoId": video_id,
                    "title": details["snippet"]["title"],
                    "url": f"https://www.youtube.com/shorts/{video_id}"
                })
    
    return shorts_videos

handle = "@zomato"
channel_id = get_channel_id_by_handle(handle)

if channel_id:
    videos = get_videos_from_channel(channel_id)
    shorts = filter_shorts(videos)
    for short in shorts:
        print(short)
else:
    print("Channel not found.")
