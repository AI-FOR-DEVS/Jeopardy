import sqlite3
from setup import create_connection

get_random_question_declaration = {
    "name": "get_random_question",
    "description": "Retrieves a random question from the questions table, filtered by category, including its ID, question text, answer, category, and points.",
    "parameters": {
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "description": "The category to filter questions by."
            }
        },
        "required": ['category']
    }
}


get_player_score_declaration = {
    "name": "get_player_score",
    "description": "Gets the total score for a specific player.",
    "parameters": {
            "type": "object",
            "properties": {
                "player_name": {
                    "type": "string",
                    "description": "The name of the player whose score is being queried."
                }
            },
        "required": ["player_name"]
    }
}

update_player_score_delaration = {
    "name": "update_player_score",
    "description": "Updates the score for a given player, adding a new score entry.",
    "parameters": {
            "type": "object",
            "properties": {
                "player_name": {
                    "type": "string",
                    "description": "The name of the player whose score is being updated."
                },
                "score": {
                    "type": "integer",
                    "description": "The score value to be added for the player."
                }
            },
        "required": ["player_name", "score"]
    }
}


def get_player_score(player_name):
    database = "jeopardy.db"
    conn = create_connection(database)
    """Get the total score for a specific player"""
    try:
        sql = '''SELECT SUM(score) FROM player_scores WHERE player_name = ?'''
        cur = conn.cursor()
        cur.execute(sql, (player_name,))
        score = cur.fetchone()[0]
        return score if score is not None else 0
    except sqlite3.Error as e:
        print(e)
        return None


def get_random_question(category):
    database = "jeopardy.db"
    conn = create_connection(database)
    print(f"----- CATEGORY : {category}")

    """
    Retrieve a random question from the questions table.
    Optionally filter by category.
    """
    try:
        cur = conn.cursor()
        if category:
            sql = '''SELECT id, question, answer, category, points FROM questions WHERE category = ? ORDER BY RANDOM() LIMIT 1'''
            cur.execute(sql, (category,))
        else:
            sql = '''SELECT id, question, answer, category, points FROM questions ORDER BY RANDOM() LIMIT 1'''
            cur.execute(sql)

        question = cur.fetchone()
        print(f"----- QUESTION : {question}")

        return question
    except sqlite3.Error as e:
        print(e)
        return None

def update_player_score(player_name, score):
    database = "jeopardy.db"
    conn = create_connection(database)
    """Add or update a player's score in the player_scores table"""
    try:
        sql = '''INSERT INTO player_scores(player_name, score) VALUES(?, ?)'''
        cur = conn.cursor()
        cur.execute(sql, (player_name, score))
        conn.commit()
    except sqlite3.Error as e:
        print(e)
        return None
