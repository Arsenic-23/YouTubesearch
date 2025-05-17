from fastapi import APIRouter, Query
from ytmusicapi import YTMusic
from app.utils.audio_extractor import get_audio_url

@router.get("/audio")
def fetch_audio_url(video_id: str = Query(..., description="YouTube video ID")):
    try:
        audio_url = get_audio_url(video_id)
        return {"audio_url": audio_url}
    except Exception as e:
        return {"error": f"Failed to extract audio URL: {str(e)}"}
router = APIRouter()
ytmusic = YTMusic()  # Uses default headers; you can customize with headers.json if needed


@router.get("/hits")
def get_daily_hits():
    try:
        charts = ytmusic.get_charts(country="ZZ")  # "ZZ" = global charts
        songs = charts.get("tracks", [])
        return [
            {
                "title": song.get("title"),
                "videoId": song.get("videoId"),
                "artists": [a["name"] for a in song.get("artists", [])],
                "thumbnails": song.get("thumbnails"),
                "url": f"https://www.youtube.com/watch?v={song.get('videoId')}"
            }
            for song in songs[:200]
        ]
    except Exception as e:
        return {"error": f"Failed to fetch global hits: {str(e)}"}


@router.get("/explore")
def explore_genre(genre: str = Query(..., description="Search genre like pop, sufi, etc")):
    try:
        search_results = ytmusic.search(genre, filter="songs")
        return [
            {
                "title": song.get("title"),
                "videoId": song.get("videoId"),
                "artists": [a["name"] for a in song.get("artists", [])],
                "thumbnails": song.get("thumbnails"),
                "url": f"https://www.youtube.com/watch?v={song.get('videoId')}"
            }
            for song in search_results[:200]
        ]
    except Exception as e:
        return {"error": f"Failed to explore songs by genre '{genre}': {str(e)}"}