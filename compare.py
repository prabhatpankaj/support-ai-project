import os
from old_way import run_old_way
from new_way import run_new_way

def main():
    print("=" * 80)
    print("TOKEN COMPARISON: Old Way vs New Way")
    print("=" * 80)
    
    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("\nSet it with:")
        print("  export ANTHROPIC_API_KEY='your-api-key'")
        return
    
    print("\n" + "=" * 80)
    old_tokens = run_old_way()
    
    print("\n" + "=" * 80)
    new_tokens = run_new_way()
    
    print("\n" + "=" * 80)
    print("📊 FINAL COMPARISON")
    print("=" * 80)
    print(f"Old Way (extrapolated): ~{old_tokens:,} tokens")
    print(f"New Way (actual):        {new_tokens:,} tokens")
    
    if old_tokens > new_tokens:
        savings_pct = ((old_tokens - new_tokens) / old_tokens * 100)
        reduction = old_tokens / new_tokens
        print(f"\n💰 Savings: {savings_pct:.2f}%")
        print(f"📉 Reduction: {reduction:.1f}x fewer tokens")
        
        # Cost comparison (assuming $3 per 1M input tokens, $15 per 1M output tokens)
        # Simplified: using average of $9 per 1M tokens
        old_cost = (old_tokens / 1_000_000) * 9
        new_cost = (new_tokens / 1_000_000) * 9
        print(f"\n💵 Estimated Cost Comparison (at $9/1M tokens avg):")
        print(f"   Old Way: ${old_cost:.2f}")
        print(f"   New Way: ${new_cost:.4f}")
        print(f"   You save: ${old_cost - new_cost:.2f} per run")
    
    print("=" * 80)

if __name__ == "__main__":
    main()