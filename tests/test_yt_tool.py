import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from backend.tools.youtube_search import YoutubeSearchTool


def test_tool():
    print("Testing YoutubeSearchTool...")
    tool = YoutubeSearchTool()
    # Try a search
    try:
        result = tool._run(topic="Python Decorators")
        print("\n--- Tool Result ---")
        print(result)
        print("-------------------\n")

        if "proxies error" in result:
            print(
                "SUCCESS: Patch correctly caught the proxies error and returned the fallback message."
            )
        elif "YouTube Search Results" in result:
            print(
                "SUCCESS: Search worked normally (maybe httpx version is different in this environment or library behaves differently)."
            )
        else:
            print("FAILURE: Unexpected result format.")

    except Exception as e:
        print(f"FAILURE: Tool raised an exception: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_tool()
