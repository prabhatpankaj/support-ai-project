import os
from anthropic import Anthropic
from python_executor import run_python

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """
You are an AI assistant with access to a Python execution environment.

Available functions:
- get_all_tickets(days: int) -> list[dict] - Get all support tickets
- get_sentiment(text: str) -> dict - Get sentiment {"sentiment": "positive"|"negative"|"neutral"}
- extract_topics(text: str) -> dict - Get topics {"topics": ["order", "refund", etc]}
- save_report(report: dict) -> dict - Save final report

Your task: Write Python code that:
1. Fetches all tickets
2. Processes them efficiently using loops
3. Counts sentiments and topics
4. Creates a summary report
5. Saves it using save_report()

Store your final result in a variable called 'result'.

Write concise, efficient Python code. DO NOT return any results to me - just process everything in Python.
"""

def run_new_way():
    print("🟢 NEW WAY: LLM writes Python code to process data...")
    
    # Ask Claude to write the processing code
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": "Write Python code to analyze all support tickets and generate a report."
        }]
    )
    
    # Token usage (just for the planning phase)
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens
    total_tokens = input_tokens + output_tokens
    
    print(f"\n📊 NEW WAY TOKEN USAGE:")
    print(f"   Input tokens:  {input_tokens:,}")
    print(f"   Output tokens: {output_tokens:,}")
    print(f"   Total tokens:  {total_tokens:,}")
    
    # Extract the Python code
    response_text = response.content[0].text if response.content else ""
    
    # Find code block
    if "```python" in response_text:
        code = response_text.split("```python")[1].split("```")[0].strip()
    elif "```" in response_text:
        code = response_text.split("```")[1].split("```")[0].strip()
    else:
        code = response_text
    
    print(f"\n🐍 Generated Python code:\n{code}\n")
    print("⚙️  Executing Python code to process all 50,000 tickets...")
    
    # Execute the code (this processes all data without sending back to LLM)
    result = run_python(code)
    
    print(f"\n✅ Processing complete!")
    print(f"Result: {result}")
    
    return total_tokens

if __name__ == "__main__":
    run_new_way()