#!/usr/bin/env python3

from db_credentials import get_db_credentials, get_db_connection

db_config = get_db_credentials("db_posts")


def get_posts(username):

    conn = get_db_connection(db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM posts WHERE username = %s ORDER BY date DESC", (username,))
    rows = cursor.fetchall()

    posts = [dict(row) for row in rows]

    return posts


def post(username, text):

    conn = get_db_connection(db_config)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO posts (username, text, date) VALUES (%s, %s, NOW())", (username, text))
    conn.commit()

    return True
