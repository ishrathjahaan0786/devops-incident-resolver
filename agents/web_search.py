from crewai import Agent, Task, Crew
from dotenv import load_dotenv
from tools.search_tool import search_fix
import os

load_dotenv()

def find_fix(error_message: str) -> dict:
    """Search for fixes for the given error."""
    
    # First get raw search results
    search_results = search_fix(error_message)
    
    agent = Agent(
        role="Fix Research Specialist",
        goal="Find the best solution for DevOps errors from search results",
        backstory="""You are a senior software engineer who specializes in 
        debugging and fixing production issues. You analyze search results 
        and extract the most practical, actionable fix for any error.""",
        verbose=True,
        llm="groq/llama-3.3-70b-versatile"
    )
    
    task = Task(
        description=f"""
        Based on these search results for the error: "{error_message}"
        
        Search Results:
        {search_results}
        
        Extract the best fix and return EXACTLY this format and nothing else:
        FIX1: <first solution in one clear sentence>
        FIX2: <backup solution in one clear sentence>
        STEPS: <numbered steps to apply Fix 1, max 4 steps>
        CONFIDENCE: <High / Medium / Low>
        """,
        expected_output="Structured fix with FIX1, FIX2, STEPS and CONFIDENCE fields",
        agent=agent
    )
    
    crew = Crew(agents=[agent], tasks=[task], verbose=True)
    result = crew.kickoff()
    
    # Parse the result
    output = str(result)
    lines = output.strip().split("\n")
    
    parsed = {}
    current_key = None
    steps_lines = []
    
    for line in lines:
        if line.startswith("FIX1:"):
            parsed["fix1"] = line.replace("FIX1:", "").strip()
        elif line.startswith("FIX2:"):
            parsed["fix2"] = line.replace("FIX2:", "").strip()
        elif line.startswith("CONFIDENCE:"):
            parsed["confidence"] = line.replace("CONFIDENCE:", "").strip()
        elif line.startswith("STEPS:"):
            current_key = "steps"
            steps_lines.append(line.replace("STEPS:", "").strip())
        elif current_key == "steps" and line.strip():
            steps_lines.append(line.strip())
    
    parsed["steps"] = "\n".join(steps_lines)
    
    return parsed