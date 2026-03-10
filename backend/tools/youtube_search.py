from typing import Any, Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class YoutubeSearchInput(BaseModel):
    """Input for YouTube search."""

    topic: str = Field(..., description="The topic to search for on YouTube.")


class YoutubeSearchTool(BaseTool):
    name: str = "youtube_search"
    description: str = (
        "Search for educational videos on YouTube about a specific topic. "
        "Returns a list of video titles and links."
    )
    args_schema: Type[BaseModel] = YoutubeSearchInput

    def _run(self, **kwargs: Any) -> str:
        # Fuzzy extraction to handle LLM schema confusion
        topic = self._extract_topic(kwargs)

        if not topic:
            return "Error: No search topic provided."

        import yt_dlp

        query = topic + " tutorial"
        ydl_opts = {
            "quiet": True,
            "extract_flat": True,
            "force_generic_extractor": True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Use ytsearch5 prefix as recommended by user
                search_query = f"ytsearch5:{query}"
                result = ydl.extract_info(search_query, download=False)

                if "entries" not in result or not result["entries"]:
                    return f"No YouTube videos found for '{topic}'."

                videos = []
                for entry in result["entries"]:
                    title = entry.get("title", "Unknown Title")
                    url = entry.get("webpage_url") or entry.get("url")
                    if not url and entry.get("id"):
                        url = f"https://www.youtube.com/watch?v={entry['id']}"

                    if url:
                        videos.append(f"- {title}: {url}")

                    if len(videos) >= 5:
                        break

                if not videos:
                    return f"No valid YouTube links found for '{topic}'."

                return f"YouTube Search Results for '{topic}':\n" + "\n".join(videos)

        except Exception as e:
            return f"Error searching YouTube with yt-dlp: {str(e)}"

    def _extract_topic(self, kwargs: Any) -> str:
        """Deeply search for a topic string in the arguments."""
        # 1. Direct hit
        if "topic" in kwargs and isinstance(kwargs["topic"], str):
            return kwargs["topic"]

        # 2. String fallback
        if isinstance(kwargs, str):
            return kwargs

        # 3. Recursive search for 'topic' or any string value that looks like a topic
        def find_string(obj: Any) -> str:
            if isinstance(obj, str):
                return obj
            if isinstance(obj, dict):
                # Priority 1: 'topic' key
                if "topic" in obj:
                    res = find_string(obj["topic"])
                    if res:
                        return res
                # Priority 2: 'title' or 'query' if topic is missing
                for k in ["title", "query", "properties"]:
                    if k in obj:
                        res = find_string(obj[k])
                        if res:
                            return res
                # Priority 3: any string value
                for val in obj.values():
                    res = find_string(val)
                    if res:
                        return res
            return ""

        return str(find_string(kwargs))
