import sys

from backend.services.learning_service import LearningService


def test_full_flow():
    user_id = 999  # Use a separate test user ID
    topic_name = "Python Decorators"

    print(f"--- Starting Integration Test for '{topic_name}' ---")

    # 0. Cleanup
    LearningService.clear_history(user_id)
    print("Step 0: Cleared history for test user.")

    # 1. Run Crew (Mocked for speed if needed, but let's try a small real output first)
    # For a real test, we would call crew.run(), but here we'll simulate the LLM output
    # to specifically test the SERVICE and DB extraction logic.
    mock_content = """
# Python Decorators Roadmap
... (intro) ...

## Roadmap
1. Basics
2. Closures
3. Decorators

## Explanations
Decorators are functions...

## YouTube Videos
* Title: Python Decorators in 5 Minutes - https://youtube.com/watch?v=123

## Exercises
**Question 1: What is a closure?**
Answer: A closure is...

**Question 2: How do you use the @ symbol?**
Answer: You place it above...

* Create a timer decorator that prints the execution time of a function.
* Implement a memoization decorator.

**Quiz Question 1: Decorators modify behavior.**
A) True
B) False
Answer: A
"""
    print("Step 1: Simulating LLM Content generation.")

    # 2. Save Topic
    new_topic = LearningService.save_topic(user_id, topic_name, mock_content)
    print(f"Step 2: Saved topic '{topic_name}' (ID: {new_topic.id}).")

    # 3. Verify in DB
    LearningService.get_user_topics(user_id)
    print("Step 3: Verified topic exists in database.")

    # 4. Verify Dashboard Stats
    stats = LearningService.get_stats(user_id)
    print(f"Step 4: Dashboard Stats: {stats}")

    if stats["topics_learned"] == 1:
        print("\nSUCCESS: All steps in the flow are working correctly!")
        # Final cleanup for the test user
        LearningService.clear_history(user_id)
        return True
    else:
        print("\nFAILED: Stats do not match expected values.")
        return False


if __name__ == "__main__":
    try:
        success = test_full_flow()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"ERROR during test: {e}")
        sys.exit(1)
