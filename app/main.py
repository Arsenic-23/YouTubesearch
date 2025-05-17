from fastapi import FastAPI, Query
from ytmusicapi import YTMusic
from app.utils.search_and_metadata import search_youtube, fetch_metadata

app = FastAPI(title="YouTube Song Search API")

ytmusic = YTMusic()  # You can optionally use YTMusic("headers_auth.json") if needed


@app.get("/search")
def search_songs(query: str = Query(..., description="Search term like 'lofi chill'")):
    results = search_youtube(query, total_results=150)
    if not results:
        return {"error": "No results found."}

    first_video_url = results[0]["link"]
    first_metadata = fetch_metadata(first_video_url)

    preview_list = [
        {
            "title": v["title"],
            "duration": v["duration"],
            "id": v["id"],
            "url": v["link"],
            "thumbnail": v["thumbnails"][0]["url"],
            "views": v.get("viewCount", {}).get("short"),
            "published": v.get("publishedTime")
        }
        for v in results
    ]

    return {
        "top_result_metadata": first_metadata,
        "preview_results": preview_list
    }


@app.get("/hits")
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


@app.get("/explore")
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