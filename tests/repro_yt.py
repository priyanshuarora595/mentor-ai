import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from backend.tools.youtube_search import YoutubeSearchTool

try:
    topic = "Python Decorators"
    print(f"Searching for: {topic} using yt-dlp tool...")
    tool = YoutubeSearchTool()
    result = tool._run(topic=topic)
    print("\n--- Tool Result ---")
    print(result)
    print("-------------------\n")

    if "YouTube Search Results" in result and "https://" in result:
        print("Success!")
    else:
        print("Failure: Results do not contain expected content.")
except Exception as e:
    print(f"Caught error: {type(e).__name__}: {str(e)}")
    import traceback

    traceback.print_exc()
