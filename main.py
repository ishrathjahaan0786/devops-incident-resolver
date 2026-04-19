from agents.manager import run_incident_resolver
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    print("🤖 DevOps Incident Resolver Agent Starting...\n")
    
    # Read the log file
    log_path = "sample_logs/error.log"
    
    if not os.path.exists(log_path):
        print(f"❌ Log file not found at {log_path}")
        return
    
    with open(log_path, "r") as f:
        log_content = f.read()
    
    print(f"📂 Log file loaded successfully")
    print(f"📋 Log content:\n{log_content}\n")
    print("=" * 60)
    
    # Run the incident resolver
    results = run_incident_resolver(log_content)
    
    print("\n" + "=" * 60)
    print("✅ INCIDENT RESOLUTION COMPLETE")
    print("=" * 60)
    
    if results.get("self_correction"):
        print("⚠️  Self-correction was triggered during this run")
    
    print(f"\n📊 Final Status: {results.get('status', 'unknown')}")
    print(f"🔗 GitHub Issue: {results.get('github_issue', 'Not created')}")

if __name__ == "__main__":
    main()