from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import os

# Environment check
is_production = os.getenv("VERCEL") == "1"

# FastAPI app
app = FastAPI(
    title="PsyFinder API",
    version="1.0.0",
    root_path="/api" if is_production else ""
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "PsyFinder API", "version": "1.0.0", "timestamp": datetime.utcnow().isoformat()}

@app.get("/events")
async def get_events(source: str = "major", force_refresh: bool = False):
    """
    Retrieve events from different sources
    """
    try:
        # Mock data for now - later will integrate with major_fests_scraper.py
        if source == "major":
            events_data = {
                "success": True,
                "source": "major",
                "events": [
                    {
                        "title": "Tomorrowland 2025",
                        "date": "2025-07-18",
                        "place": "Boom, Belgium",
                        "genre": "Electronic/Trance",
                        "image": "https://images.unsplash.com/photo-1518005020951-eccb49447d0a?w=600",
                        "description": "The world's biggest electronic music festival",
                        "url": "https://tomorrowland.com"
                    },
                    {
                        "title": "Ultra Music Festival",
                        "date": "2025-03-28",
                        "place": "Miami, USA",
                        "genre": "Electronic/EDM",
                        "image": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600",
                        "description": "Premier electronic music festival",
                        "url": "https://ultramusicfestival.com"
                    },
                    {
                        "title": "Ozora Festival",
                        "date": "2025-08-05",
                        "place": "Hungary",
                        "genre": "Psytrance",
                        "image": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=600",
                        "description": "The ultimate psytrance experience",
                        "url": "https://ozorafestival.eu"
                    }
                ],
                "cache_info": {
                    "last_update": datetime.utcnow().isoformat(),
                    "source": "major_festivals_api"
                },
                "total": 3
            }
        elif source == "clubberia":
            events_data = {
                "success": True,
                "source": "clubberia",
                "events": [
                    {
                        "title": "Tokyo Psychedelic Night",
                        "date": "2025-07-15",
                        "place": "Shibuya, Tokyo",
                        "genre": "Psytrance",
                        "image": "https://images.unsplash.com/photo-1571974599782-87624638275c?w=600",
                        "description": "Underground psytrance event in Tokyo",
                        "url": "#"
                    },
                    {
                        "title": "Cosmic Dance",
                        "date": "2025-07-20",
                        "place": "Harajuku, Tokyo",
                        "genre": "Progressive Trance",
                        "image": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600",
                        "description": "Progressive trance night",
                        "url": "#"
                    }
                ],
                "cache_info": {
                    "last_update": datetime.utcnow().isoformat(),
                    "source": "clubberia_scraper"
                },
                "total": 2
            }
        else:
            events_data = {
                "success": False,
                "error": f"Unknown source: {source}",
                "events": []
            }
        
        return JSONResponse(content=events_data)
    
    except Exception as e:
        return JSONResponse(
            content={
                "success": False,
                "error": str(e),
                "events": []
            },
            status_code=500
        )

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)