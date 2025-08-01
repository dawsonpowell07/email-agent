from graph import graph
import os
import json
import datetime
from dotenv import load_dotenv
from utils.auth import set_current_user

load_dotenv()


def run_for_user(user_email: str) -> bool:
    """Run the email agent for a specific user."""
    print(f"Starting run for {user_email}")
    set_current_user(user_email)

    try:
        app = graph
        final_state = app.invoke(
            {
                "messages": [
                    {"role": "user", "content": f"Process emails for {user_email}"}
                ],
                "user_email": user_email,
            }
        )

        timestamp = datetime.datetime.now().isoformat().replace(":", "-")
        output_file = f"output_{user_email}_{timestamp}.json"
        with open(output_file, "w") as f:
            json.dump(final_state, f, indent=2, default=str)
        print(f"✅ Finished run for {user_email}. Results saved to {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error running for {user_email}: {e}")
        return False


def main() -> None:
    """Main function to run the email agent for multiple users."""
    print("🚀 Starting email agent for multiple users...")

    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Make sure to set the OPENAI_API_KEY environment variable or add it to your .env file")
        return

    users = ["personal@example.com", "school@example.com"]
    results = []
    for email in users:
        success = run_for_user(email)
        results.append((email, success))

    print("\n📊 Summary:")
    for email, success in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"  {email}: {status}")

    failed_runs = sum(1 for _, success in results if not success)
    if failed_runs > 0:
        print(f"\n⚠️  {failed_runs} run(s) failed")
        exit(1)
    else:
        print("\n🎉 All runs completed successfully!")


if __name__ == "__main__":
    main()
