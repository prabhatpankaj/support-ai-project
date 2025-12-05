# Token Comparison: Traditional Agents vs Anthropic Programmatic Tool Calling

This repository contains a **real, reproducible experiment** comparing two approaches to AI agent development:

❌ **Old Way (Traditional LLM Agent)**  
LLM reads all data, performs reasoning in-context, and receives outputs from tools step-by-step.

✅ **New Way (Anthropic Programmatic Tool Calling)**  
LLM writes a Python program → Python executes loops, filtering, and processing → Only final summary returns to the model.

---

## 🚀 What This Project Demonstrates

This repo analyzes **50,000 real customer support tickets** stored in a SQLite database.

The agent performs:
- 📊 Sentiment classification (positive/negative/neutral)
- 🏷️ Topic extraction (order, refund, payment, delivery, etc.)
- 📈 Aggregation of statistics across all tickets
- 📄 Generation of a final daily report

---

## 💡 The Key Difference

| Approach    | LLM Sees                                   | Tokens           | Cost      | Efficiency |
| ----------- | ------------------------------------------ | ---------------- | --------- | ---------- |
| **Old Way** | Every ticket text (50k), every tool output | ~2,131,000 tokens | $19.18    | ❌ Slow, expensive |
| **New Way** | Only writes Python code once               | ~673 tokens      | $0.0061   | ✅ Fast, cheap |

### 📉 Results
- **Token Savings:** 99.97%
- **Cost Savings:** $19.17 per run
- **Efficiency Gain:** 3,166x fewer tokens

---

## 📁 Repository Structure

```
support-ai-project/
│
├── generate_db.py            # Generates 50k realistic support tickets
├── old_way.py                # Traditional token-heavy agent
├── new_way.py                # Programmatic Tool Calling agent
├── python_executor.py        # Safe Python sandbox for tool execution
├── compare.py                # Run both approaches and compare results
│
├── tools/
│   ├── __init__.py           # Python package marker
│   ├── tickets.py            # Fetch tickets from database
│   ├── sentiment.py          # Sentiment classifier tool
│   ├── topics.py             # Topic extraction tool
│   └── report.py             # Save/report results
│
├── db/
│   └── tickets.db            # Auto-created SQLite DB (50k messages)
│
├── requirements.txt          # Python dependencies
├── Dockerfile                # Container definition
├── docker-compose.yml        # Service orchestration
└── README.md                 # This file
```

---

## 🏃 Quick Start

### Prerequisites
- Docker and Docker Compose **OR**
- Python 3.11+ with pip
- Anthropic API key ([get one here](https://console.anthropic.com/))

### Option 1: Using Docker (Recommended)

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd support-ai-project

# 2. Set your API key
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env

# 3. Generate the database (50,000 tickets)
docker-compose run db_generator

# 4. Run the full comparison
docker-compose run compare

# Or run individually:
docker-compose run old_way
docker-compose run new_way
```

### Option 2: Using Python Directly

```bash
# 1. Clone and navigate
git clone <your-repo-url>
cd support-ai-project

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your API key
export ANTHROPIC_API_KEY='your-api-key-here'

# 5. Generate the database
python generate_db.py

# 6. Run comparison
python compare.py

# Or run individually:
python old_way.py
python new_way.py
```

---

## 📊 Expected Output

### Old Way (Traditional Agent)
```
🔴 OLD WAY: Loading all tickets into LLM context...
Loaded 50000 tickets
⚠️  Processing ALL 50000 tickets would use ~2,250,000 tokens
   (Estimated 45 tokens per ticket)

   For demo purposes, processing only 50 tickets...
Sending 50 tickets to Claude...

📊 OLD WAY TOKEN USAGE (for 50 tickets):
   Input tokens:  1,900
   Output tokens: 231
   Total tokens:  2,131

📈 EXTRAPOLATED for all 50000 tickets:
   Estimated total: ~2,131,000 tokens
```

### New Way (Programmatic Tool Calling)
```
🟢 NEW WAY: LLM writes Python code to process data...

📊 NEW WAY TOKEN USAGE:
   Input tokens:  219
   Output tokens: 454
   Total tokens:  673

🐍 Generated Python code:
[Shows the Python code Claude wrote]

⚙️  Executing Python code to process all 50,000 tickets...
[REPORT SAVED] {statistics for all 50,000 tickets}

✅ Processing complete!
```

### Final Comparison
```
================================================================================
📊 FINAL COMPARISON
================================================================================
Old Way (extrapolated): ~2,131,000 tokens
New Way (actual):        673 tokens

💰 Savings: 99.97%
📉 Reduction: 3166.4x fewer tokens

💵 Estimated Cost Comparison (at $9/1M tokens avg):
   Old Way: $19.18
   New Way: $0.0061
   You save: $19.17 per run
================================================================================
```

---

## 🔍 How It Works

### Old Way (Traditional Agent)
1. **Load all 50,000 tickets** from the database
2. **Pass each ticket** to the LLM along with sentiment and topic data
3. **LLM processes** every single ticket in its context window
4. **Generate report** based on all the data in context

**Problem:** Massive token usage scales linearly with data size.

### New Way (Programmatic Tool Calling)
1. **Ask LLM to write Python code** for the analysis task
2. **Execute the Python code** in a safe sandbox environment
3. **Python processes all 50,000 tickets** using efficient loops
4. **Only the final summary** returns to the LLM

**Benefit:** Token usage stays constant regardless of data size!

---

## 🎯 Key Insights

### Why This Matters
- **Cost Efficiency:** Save 99.97% on token costs for data-heavy tasks
- **Speed:** Process millions of records without hitting context limits
- **Scalability:** Token usage doesn't scale with dataset size
- **Accuracy:** Deterministic processing eliminates LLM hallucinations on data aggregation

### When to Use Programmatic Tool Calling
- ✅ Large dataset analysis (thousands to millions of records)
- ✅ Repetitive operations (filtering, aggregating, counting)
- ✅ Data transformations and ETL tasks
- ✅ Statistical calculations
- ✅ Multi-step workflows with intermediate processing

### When to Use Traditional Approach
- ❌ Small datasets (< 100 items)
- ❌ Tasks requiring complex reasoning on each item
- ❌ When you need LLM judgment for every decision

---

## 🛠️ Customization

### Modify the Analysis
Edit the tools in the `tools/` directory to change how data is processed:
- `sentiment.py` - Customize sentiment logic
- `topics.py` - Add new topic categories
- `tickets.py` - Change data source or query logic

### Scale the Dataset
Change the number of tickets in `generate_db.py`:
```python
generate_tickets(100000)  # Generate 100k tickets instead
```

### Try Different Models
Update the model in `old_way.py` and `new_way.py`:
```python
model="claude-opus-4-20250514"  # Use Opus for better code generation
```

---

## 📚 Learn More

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Programmatic Tool Use Guide](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [Token Pricing](https://www.anthropic.com/pricing)

---

## 🐛 Troubleshooting

### "Model not found" error
Make sure you're using a valid model name. Current models:
- `claude-sonnet-4-20250514` (recommended)
- `claude-opus-4-20250514`

### "API key not set" error
```bash
# Set your API key
export ANTHROPIC_API_KEY='sk-ant-...'

# Or create .env file
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

### Docker orphan containers warning
```bash
docker-compose down --remove-orphans
```

---

## 📝 License

MIT License - feel free to use this for your own experiments!

---

## 🤝 Contributing

Found a bug or want to improve the comparison? PRs welcome!

---

## ⭐ Key Takeaway

**Programmatic Tool Calling isn't just an optimization—it's a paradigm shift.**

Instead of feeding data TO the LLM, have the LLM write code that PROCESSES the data. This transforms LLMs from expensive reasoning engines into efficient orchestrators of computation.

**Result:** 3,166x token reduction, 99.97% cost savings, unlimited scalability. 🚀



### here is the result of the comparison . 

```

docker-compose run compare
WARN[0000] Found orphan containers ([support-ai-project-new_way-run-fecf232f8d75 support-ai-project-old_way-run-61051e4eba97 support-ai-project-old_way-run-589ef65d8232]) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up.
================================================================================
TOKEN COMPARISON: Old Way vs New Way
================================================================================

================================================================================
🔴 OLD WAY: Loading all tickets into LLM context...
Loaded 50000 tickets
⚠️  Processing ALL 50000 tickets would use ~2,250,000 tokens
   (Estimated 45 tokens per ticket)

   For demo purposes, processing only 50 tickets...
Sending 50 tickets to Claude...

📊 OLD WAY TOKEN USAGE (for 50 tickets):
   Input tokens:  1,900
   Output tokens: 231
   Total tokens:  2,131

📈 EXTRAPOLATED for all 50000 tickets:
   Estimated total: ~2,131,000 tokens
[REPORT SAVED] {'summary': '```json\n{\n  "total_tickets": 50,\n  "sentiment_counts": {\n    "positive": 17,\n    "negative": 19,\n    "neutral": 14\n  },\n  "top_topics": [\n    {\n      "topic": "order",\n      "count": 25,\n      "percentage": 50\n    },\n    {\n      "topic": "general",\n      "count": 25,\n      "percentage": 50\n    }\n  ],\n  "summary": "Analysis of 50 support tickets shows an even split between order-related issues (50%) and general issues (50%). Sentiment distribution is relatively balanced with 38% negative, 34% positive, and 28% neutral tickets. Common issues include payment gateway problems, damaged orders, delivery delays, billing discrepancies, app crashes, incorrect items, and refund processing delays. The high volume of order-related complaints suggests potential fulfillment and logistics challenges that may need operational attention."\n}\n```', 'method': 'old_way', 'tickets_processed': 50}

✅ Report saved: REPORT-2025-001

Response preview:
```json
{
  "total_tickets": 50,
  "sentiment_counts": {
    "positive": 17,
    "negative": 19,
    "neutral": 14
  },
  "top_topics": [
    {
      "topic": "order",
      "count": 25,
      "percentage": 50
    },
    {
      "topic": "general",
      "count": 25,
      "percentage": 50
    }
  ]...

================================================================================
🟢 NEW WAY: LLM writes Python code to process data...

📊 NEW WAY TOKEN USAGE:
   Input tokens:  219
   Output tokens: 454
   Total tokens:  673

🐍 Generated Python code:
# Get all tickets from the last 30 days
tickets = get_all_tickets(30)

# Initialize counters
sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
topic_counts = {}
total_tickets = len(tickets)

# Process each ticket
for ticket in tickets:
    # Get sentiment for the ticket content
    sentiment_result = get_sentiment(ticket.get('content', ''))
    sentiment = sentiment_result.get('sentiment', 'neutral')
    sentiment_counts[sentiment] += 1

    # Extract topics from the ticket content
    topics_result = extract_topics(ticket.get('content', ''))
    topics = topics_result.get('topics', [])

    # Count each topic
    for topic in topics:
        topic_counts[topic] = topic_counts.get(topic, 0) + 1

# Calculate sentiment percentages
sentiment_percentages = {}
for sentiment, count in sentiment_counts.items():
    sentiment_percentages[sentiment] = round((count / total_tickets) * 100, 1) if total_tickets > 0 else 0

# Get top 10 topics
top_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:10]

# Create the report
report = {
    "total_tickets": total_tickets,
    "sentiment_analysis": {
        "counts": sentiment_counts,
        "percentages": sentiment_percentages
    },
    "top_topics": dict(top_topics),
    "summary": f"Processed {total_tickets} tickets. Most common sentiment: {max(sentiment_counts, key=sentiment_counts.get)}. Top issue: {top_topics[0][0] if top_topics else 'None'}"
}

# Save the report
result = save_report(report)

⚙️  Executing Python code to process all 50,000 tickets...
[REPORT SAVED] {'total_tickets': 50000, 'sentiment_analysis': {'counts': {'positive': 16720, 'negative': 16637, 'neutral': 16643}, 'percentages': {'positive': 33.4, 'negative': 33.3, 'neutral': 33.3}}, 'top_topics': {'general': 50000}, 'summary': 'Processed 50000 tickets. Most common sentiment: positive. Top issue: general'}

✅ Processing complete!
Result: {'report_id': 'REPORT-2025-001'}

================================================================================
📊 FINAL COMPARISON
================================================================================
Old Way (extrapolated): ~2,131,000 tokens
New Way (actual):        673 tokens

💰 Savings: 99.97%
📉 Reduction: 3166.4x fewer tokens

💵 Estimated Cost Comparison (at $9/1M tokens avg):
   Old Way: $19.18
   New Way: $0.0061
   You save: $19.17 per run
================================================================================

```