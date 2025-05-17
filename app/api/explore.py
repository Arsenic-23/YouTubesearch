# app/api/explore.py

from fastapi import APIRouter, Query
from ytmusicapi import YTMusic

router = APIRouter()
ytmusic = YTMusic()  # You can optionally initialize with headers.json if needed

@router.get("/hits")
def get_daily_hits(country: str = Query("US", description="Country code like US, IN, UK")):
    charts = ytmusic.get_charts(country=country)
    songs = charts.get("tracks", [])
    return [
        {
            "title": song["title"],
            "videoId": song["videoId"],
            "artists": [a["name"] for a in song["artists"]],
            "thumbnails": song["thumbnails"],
            "url": f"https://www.youtube.com/watch?v={song['videoId']}"
        }
        for song in songs[:200]
    ]

@router.get("/explore")
def explore_genre(genre: str = Query(..., description="Search genre like pop, sufi, etc")):
    search_results = ytmusic.search(genre, filter="songs")
    return [
        {
            "title": song["title"],
            "videoId": song.get("videoId"),
            "artists": [a["name"] for a in song.get("artists", [])],
            "thumbnails": song.get("thumbnails"),
            "url": f"https://www.youtube.com/watch?v={song['videoId']}"
        }
        for song in search_results[:200]
    ]