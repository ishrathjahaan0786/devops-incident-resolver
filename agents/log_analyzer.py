from crewai import Agent, Task, Crew
import crewai.llms.cache as crew_cache
from dotenv import load_dotenv
import os

# Disable CrewAI cache markers for Groq
crew_cache.mark_cache_breakpoint = lambda msg: msg

load_dotenv()

def analyze_log(log_content: str) -> dict:
    """Analyze log file and extract error details."""
    
    agent = Agent(
        role="Log Analyzer",
        goal="Extract and analyze errors from log files accurately",
        backstory="""You are an expert DevOps engineer with 10 years of experience 
        reading and analyzing server logs. You can instantly identify the most 
        critical errors and understand their root causes.""",
        verbose=True,
        llm="groq/qwen/qwen3.8-27b"
    )
    
    task = Task(
        description=f"""
        Analyze this log file and extract the most critical error:
        
        {log_content}
        
        You must return EXACTLY this format and nothing else:
        ERROR: <the main error message>
        FILE: <the file where error occurred>
        SEVERITY: <Critical / High / Low>
        ROLE: <Backend / DevOps / Database>
        SUMMARY: <one sentence explanation of what went wrong>
        """,
        expected_output="Structured error analysis with ERROR, FILE, SEVERITY, ROLE and SUMMARY fields",
        agent=agent
    )
    
    crew = Crew(agents=[agent], tasks=[task], verbose=True)
    result = crew.kickoff()
    
    # Parse the result
    output = str(result)
    lines = output.strip().split("\n")
    
    parsed = {}
    for line in lines:
        if line.startswith("ERROR:"):
            parsed["error"] = line.replace("ERROR:", "").strip()
        elif line.startswith("FILE:"):
            parsed["file"] = line.replace("FILE:", "").strip()
        elif line.startswith("SEVERITY:"):
            parsed["severity"] = line.replace("SEVERITY:", "").strip()
        elif line.startswith("ROLE:"):
            parsed["role"] = line.replace("ROLE:", "").strip()
        elif line.startswith("SUMMARY:"):
            parsed["summary"] = line.replace("SUMMARY:", "").strip()
    
    return parsed
