import sqlite3
import random


# Function to connect to the SQLite database
def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

# Function to create tables


def create_tables(conn):
    """Create tables in the specified database connection"""
    try:
        c = conn.cursor()

        # Create Questions Table
        c.execute('''CREATE TABLE IF NOT EXISTS questions (
                        id INTEGER PRIMARY KEY,
                        question TEXT NOT NULL,
                        answer TEXT NOT NULL,
                        category TEXT,
                        points INTEGER)''')

        # Create Player Scores Table
        c.execute('''CREATE TABLE IF NOT EXISTS player_scores (
                        id INTEGER PRIMARY KEY,
                        player_name TEXT NOT NULL,
                        score INTEGER NOT NULL)''')

        conn.commit()
    except sqlite3.Error as e:
        print(e)


# Function to add a new question with its answer, category, and points
def add_question(conn, question, answer, category, points):
    """Add a new question with its answer, category, and points to the questions table"""
    try:
        sql = '''INSERT INTO questions(question, answer, category, points) VALUES(?, ?, ?, ?)'''
        cur = conn.cursor()
        cur.execute(sql, (question, answer, category, points))
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        print(e)
        return None


def add_jeopardy_questions_with_categories_points(conn):
    """Add Jeopardy-style questions with categories and points to the questions table"""
    jeopardy_questions = [
        ("The 'Sunshine State' in the U.S.",
         "What is Florida?", "U.S. States", 100),
        ("This author wrote '1984' and 'Animal Farm'",
         "Who is George Orwell?", "Authors", 100),
        ("The profession of the character who narrated 'The Miller's Tale' in 'The Canterbury Tales'",
         "What is a miller?", "Literature", 800),
        ("This 1925 novel features a character named 'Dr. T.J. Eckleburg', known for his symbolic depiction",
         "What is 'The Great Gatsby'?", "Literature", 800),
        ("The model developed by Crick and Watson, crucial to understanding this biological structure",
         "What is DNA?", "Science", 800),
        ("The limit named after an Indian-American astrophysicist, crucial in understanding the fate of massive stars",
         "What is the Chandrasekhar Limit?", "Science", 800),
        ("The agreement signed between Germany and the Soviet Union in 1939, marking a significant prelude to World War II",
         "What is the Molotov-Ribbentrop Pact?", "History", 800),
        ("The Emperor of France who reigned immediately before Napoleon III",
         "Who is Louis-Philippe I?", "History", 800),
        ("The second-largest island in the Mediterranean Sea, divided between two primary political entities",
         "What is Sardinia?", "Geography", 800),
        ("A South American river flowing through multiple countries, other than the Amazon",
         "What is the Paraná River?", "Geography", 800),
        ("This term refers to a word that is spelled the same forwards and backwards",
         "What is a palindrome?", "Linguistics", 1000),
        ("This fictional character, a symbol of Americana, was created by cartoonist Harold Gray in 1924",
         "Who is Little Orphan Annie?", "Pop Culture", 1000),
        ("This philosophical paradox involves a cat that may be simultaneously both alive and dead, according to quantum theory",
         "What is Schrödinger's Cat?", "Philosophy", 1000),
        ("This ancient technique, used in Egyptian and Byzantine art, involves setting small pieces of stone or glass into a surface to create a picture", "What is mosaic?", "Art", 1000)

    ]
    # Clear existing questions and add new Jeopardy-style questions with categories and points
    clear_questions(conn)
    for question, answer, category, points in jeopardy_questions:
        add_question(conn, question, answer, category, points)

# Function to clear the existing questions in the database


def clear_questions(conn):
    """Clear all questions from the questions table"""
    try:
        sql = '''DELETE FROM questions'''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

# Main function to create database and tables


def main():
    database = "jeopardy.db"
    conn = create_connection(database)
    if conn is not None:
        # Create tables
        create_tables(conn)

        # Add Jeopardy-style questions with categories and points
        add_jeopardy_questions_with_categories_points(conn)
        print(
            "Jeopardy-style sample questions with categories and points added successfully.")
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
