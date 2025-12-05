import os
from anthropic import Anthropic
from tools.tickets import get_all_tickets
from tools.sentiment import get_sentiment
from tools.topics import extract_topics
from tools.report import save_report

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """
You are an AI system analyzing support tickets.

Your task:
1. Review all tickets provided
2. Count sentiments (positive, negative, neutral)
3. Identify top topics
4. Generate a brief summary report

Respond with a JSON summary containing:
- total_tickets
- sentiment_counts
- top_topics
- summary
"""

def run_old_way():
    print("🔴 OLD WAY: Loading all tickets into LLM context...")
    
    # Load all 50,000 tickets
    tickets = get_all_tickets(1)
    print(f"Loaded {len(tickets)} tickets")
    
    # Calculate what token usage WOULD be for all tickets
    sample_ticket = tickets[0]
    sentiment = get_sentiment(sample_ticket['text'])
    topics = extract_topics(sample_ticket['text'])
    sample_text = (
        f"Ticket {sample_ticket['id']}:\n"
        f"Message: {sample_ticket['text']}\n"
        f"Sentiment: {sentiment['sentiment']}\n"
        f"Topics: {', '.join(topics['topics'])}\n\n"
    )
    
    # Estimate: ~4 chars = 1 token, so len(text)/4 ≈ tokens
    tokens_per_ticket = len(sample_text) // 3  # Conservative estimate
    estimated_tokens_all = tokens_per_ticket * len(tickets)
    
    print(f"⚠️  Processing ALL {len(tickets)} tickets would use ~{estimated_tokens_all:,} tokens")
    print(f"   (Estimated {tokens_per_ticket} tokens per ticket)")
    print(f"\n   For demo purposes, processing only 50 tickets...")
    
    # Build content blocks with LIMITED ticket data for demo
    content_blocks = [
        {
            "type": "text",
            "text": f"Analyze these support tickets and provide summary statistics:\n\n"
        }
    ]
    
    # Process only 50 tickets for demo (to avoid API limits)
    demo_limit = 50
    for t in tickets[:demo_limit]:
        sentiment = get_sentiment(t['text'])
        topics = extract_topics(t['text'])
        
        content_blocks.append({
            "type": "text",
            "text": (
                f"Ticket {t['id']}:\n"
                f"Message: {t['text']}\n"
                f"Sentiment: {sentiment['sentiment']}\n"
                f"Topics: {', '.join(topics['topics'])}\n\n"
            )
        })
    
    print(f"Sending {demo_limit} tickets to Claude...")
    
    # Call Claude with sample data
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": content_blocks
        }]
    )
    
    # Token usage for sample
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens
    total_tokens = input_tokens + output_tokens
    
    # Extrapolate to full dataset
    extrapolated_tokens = (total_tokens * len(tickets)) // demo_limit
    
    print(f"\n📊 OLD WAY TOKEN USAGE (for {demo_limit} tickets):")
    print(f"   Input tokens:  {input_tokens:,}")
    print(f"   Output tokens: {output_tokens:,}")
    print(f"   Total tokens:  {total_tokens:,}")
    print(f"\n📈 EXTRAPOLATED for all {len(tickets)} tickets:")
    print(f"   Estimated total: ~{extrapolated_tokens:,} tokens")
    
    # Extract response text
    response_text = response.content[0].text if response.content else "No response"
    
    # Save report
    report = save_report({"summary": response_text, "method": "old_way", "tickets_processed": demo_limit})
    
    print(f"\n✅ Report saved: {report['report_id']}")
    print(f"\nResponse preview:\n{response_text[:300]}...")
    
    return extrapolated_tokens

if __name__ == "__main__":
    run_old_way()