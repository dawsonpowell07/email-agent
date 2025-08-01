from graph import graph
import os
import json
import datetime
import shutil

def run_for_user(token_path: str, user_name: str):
    """Run the email agent for a specific user with their token."""
    print(f"Starting run for {user_name} with token: {token_path}")
    
    # Check if token file exists
    if not os.path.exists(token_path):
        print(f"Error: Token file {token_path} not found for {user_name}")
        return False
    
    # Copy the user's token to the expected location
    shutil.copy(token_path, "token.json")
    
    try:
        # Initialize the graph
        app = graph
        
        # Run the email processing workflow
        final_state = app.invoke({
            "messages": [{"role": "user", "content": f"Process emails for {user_name}"}]
        })
        
        # Save the results
        timestamp = datetime.datetime.now().isoformat().replace(":", "-")
        output_file = f"output_{user_name}_{timestamp}.json"
        
        with open(output_file, "w") as f:
            json.dump(final_state, f, indent=2, default=str)
        
        print(f"✅ Finished run for {user_name}. Results saved to {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error running for {user_name}: {e}")
        return False
    
    finally:
        # Clean up the token file
        if os.path.exists("token.json"):
            os.remove("token.json")

def main():
    """Main function to run the email agent for multiple users."""
    print("🚀 Starting email agent for multiple users...")
    
    # Define users and their token files
    users = [
        ("token1.json", "personal"),
        ("token2.json", "school")
    ]
    
    results = []
    
    for token_path, user_name in users:
        success = run_for_user(token_path, user_name)
        results.append((user_name, success))
    
    # Print summary
    print("\n📊 Summary:")
    for user_name, success in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"  {user_name}: {status}")
    
    # Exit with error code if any runs failed
    failed_runs = sum(1 for _, success in results if not success)
    if failed_runs > 0:
        print(f"\n⚠️  {failed_runs} run(s) failed")
        exit(1)
    else:
        print("\n🎉 All runs completed successfully!")

if __name__ == "__main__":
    main()
