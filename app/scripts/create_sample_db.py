"""Script to create a sample SQLite database for a classic literature bookstore."""

import os
import sqlite3
from datetime import datetime, timedelta
import random

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "scratchpad", "bookstore.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Sample data
SAMPLE_USERS = [
    ("John", "Doe", "john@example.com", True),
    ("Jane", "Smith", "jane@example.com", True),
    ("Robert", "Wilson", "bob@example.com", False),
    ("Alice", "Brown", "alice@example.com", True),
    ("Charles", "Davis", "charlie@example.com", True),
    ("Emma", "Jones", "emma@example.com", False),
    ("David", "Miller", "david@example.com", True),
    ("Sophia", "Wilson", "sophia@example.com", True),
    ("James", "Taylor", "james@example.com", True),
    ("Olivia", "Moore", "olivia@example.com", False),
    ("Michael", "Anderson", "michael@example.com", True),
    ("Elena", "Garcia", "elena@example.com", True),
    ("William", "Martinez", "william@example.com", True),
    ("Isabella", "Lopez", "isabella@example.com", True),
    ("Alexander", "Lee", "alex@example.com", True),
]

SAMPLE_BOOKS = [
    ("I, Robot", "Isaac Asimov", 15.99, "Science Fiction", 1950),
    ("Foundation", "Isaac Asimov", 14.99, "Science Fiction", 1951),
    ("The Metamorphosis", "Franz Kafka", 12.99, "Fiction", 1915),
    ("The Trial", "Franz Kafka", 13.99, "Fiction", 1925),
    ("Crime and Punishment", "Fyodor Dostoevsky", 16.99, "Literary Fiction", 1866),
    ("The Brothers Karamazov", "Fyodor Dostoevsky", 17.99, "Literary Fiction", 1880),
    ("Siddhartha", "Hermann Hesse", 11.99, "Philosophical Fiction", 1922),
    ("Steppenwolf", "Hermann Hesse", 13.99, "Philosophical Fiction", 1927),
    ("The Glass Bead Game", "Hermann Hesse", 14.99, "Philosophical Fiction", 1943),
    ("1984", "George Orwell", 13.99, "Dystopian Fiction", 1949),
    ("Animal Farm", "George Orwell", 12.99, "Political Satire", 1945),
    ("Brave New World", "Aldous Huxley", 14.99, "Dystopian Fiction", 1932),
    ("The Old Man and the Sea", "Ernest Hemingway", 11.99, "Literary Fiction", 1952),
    ("To Kill a Mockingbird", "Harper Lee", 13.99, "Literary Fiction", 1960),
    ("One Hundred Years of Solitude", "Gabriel García Márquez", 15.99, "Magical Realism", 1967),
]


def create_sample_database():
    """Creates a sample bookstore database with users, books, and orders tables."""

    # Set the store opening date (3 months ago from Dec 25, 2024)
    STORE_OPENING_DATE = datetime(2024, 9, 25)
    CURRENT_DATE = datetime(2024, 12, 25)

    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Create users table
        cursor.execute(
            """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN NOT NULL
        )
        """
        )

        # Create books table
        cursor.execute(
            """
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            genre TEXT NOT NULL,
            publication_year INTEGER NOT NULL,
            stock INTEGER DEFAULT 100
        )
        """
        )

        # Create orders table
        cursor.execute(
            """
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            total_amount DECIMAL(10,2) NOT NULL,
            status TEXT CHECK(status IN ('pending', 'completed', 'cancelled')) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (book_id) REFERENCES books (id)
        )
        """
        )

        # Insert sample users
        current_time = CURRENT_DATE
        for first_name, last_name, email, is_active in SAMPLE_USERS:
            cursor.execute(
                "INSERT INTO users (first_name, last_name, email, created_at, is_active) VALUES (?, ?, ?, ?, ?)",
                (first_name, last_name, email, current_time, is_active),
            )
            current_time -= timedelta(days=random.randint(1, 90))

        # Insert sample books
        for title, author, price, genre, year in SAMPLE_BOOKS:
            cursor.execute(
                "INSERT INTO books (title, author, price, genre, publication_year) VALUES (?, ?, ?, ?, ?)",
                (title, author, price, genre, year),
            )

        # Insert sample orders
        statuses = ["completed"] * 8 + ["pending"] * 1 + ["cancelled"] * 1  # 80% completed, 10% pending, 10% cancelled
        current_time = CURRENT_DATE

        # Create multiple orders for each user
        for user_id in range(1, len(SAMPLE_USERS) + 1):
            # Generate 5-15 orders per user
            num_orders = random.randint(5, 15)
            for _ in range(num_orders):
                book_id = random.randint(1, len(SAMPLE_BOOKS))
                quantity = random.randint(1, 3)
                # Get the book price directly from SAMPLE_BOOKS using book_id - 1 as index
                book_price = SAMPLE_BOOKS[book_id - 1][2]  # Index 2 is the price in the book tuple
                total_amount = round(quantity * book_price, 2)
                status = random.choice(statuses)

                # Orders within the last 3 months
                order_date = STORE_OPENING_DATE + timedelta(
                    days=random.randint(0, 90), hours=random.randint(0, 23), minutes=random.randint(0, 59)
                )

                cursor.execute(
                    "INSERT INTO orders (user_id, book_id, quantity, total_amount, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (user_id, book_id, quantity, total_amount, status, order_date),
                )

        # Commit the changes
        conn.commit()
        print(f"✅ Sample bookstore database created successfully at {DB_PATH}")

        # Print some sample data
        print("\n📊 Sample Queries:")

        print("\nActive Users:")
        cursor.execute(
            """
            SELECT first_name, last_name, email 
            FROM users 
            WHERE is_active = 1 
            LIMIT 3
        """
        )
        print(cursor.fetchall())

        print("\nAvailable Books:")
        cursor.execute(
            """
            SELECT title, author, price 
            FROM books 
            LIMIT 3
        """
        )
        print(cursor.fetchall())

        print("\nRecent Orders:")
        cursor.execute(
            """
            SELECT u.first_name, u.last_name, b.title, o.quantity, o.total_amount, o.created_at 
            FROM orders o 
            JOIN users u ON o.user_id = u.id 
            JOIN books b ON o.book_id = b.id 
            ORDER BY o.created_at DESC 
            LIMIT 3
        """
        )
        print(cursor.fetchall())

    except Exception as e:
        print(f"❌ Error creating database: {str(e)}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    create_sample_database()
