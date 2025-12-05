import sqlite3
import random
from faker import Faker
import os

fake = Faker()

# Create db directory if it doesn't exist
os.makedirs("db", exist_ok=True)

# Templates for realistic support messages
TEMPLATES = [
    "My order #{order_id} hasn't arrived yet. Can you help?",
    "I need a refund for order #{order_id}. The product was damaged.",
    "When will my delivery arrive? Order #{order_id}",
    "The payment failed for my order #{order_id}. Please assist.",
    "My package is delayed. Order #{order_id}",
    "I want to return my order #{order_id}. It's not what I expected.",
    "Can I get a refund? Order #{order_id} arrived broken.",
    "The app keeps crashing when I try to place an order.",
    "I haven't received my delivery confirmation for order #{order_id}",
    "Payment issue with order #{order_id}. Card was charged twice.",
    "Product quality is poor. Order #{order_id}. Want refund.",
    "Delivery was delayed by 3 days. Order #{order_id}",
    "Can you track my order #{order_id}?",
    "I need help with my payment method for order #{order_id}",
    "Order #{order_id} is missing items. Please help.",
]

def generate_tickets(num_tickets=50000):
    conn = sqlite3.connect("db/tickets.db")
    c = conn.cursor()
    
    # Create table
    c.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Clear existing data
    c.execute("DELETE FROM tickets")
    
    print(f"Generating {num_tickets} support tickets...")
    
    tickets = []
    for i in range(num_tickets):
        template = random.choice(TEMPLATES)
        order_id = random.randint(100000, 999999)
        message = template.replace("{order_id}", str(order_id))
        tickets.append((message,))
        
        if (i + 1) % 10000 == 0:
            print(f"Generated {i + 1} tickets...")
    
    # Bulk insert
    c.executemany("INSERT INTO tickets (message) VALUES (?)", tickets)
    conn.commit()
    
    # Verify count
    c.execute("SELECT COUNT(*) FROM tickets")
    count = c.fetchone()[0]
    print(f"\n✅ Successfully created {count} tickets in db/tickets.db")
    
    conn.close()

if __name__ == "__main__":
    generate_tickets(50000)