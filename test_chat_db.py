import sys
import os
import sqlite3

# add backend to path
sys.path.insert(0, os.path.abspath('backend'))

from app import create_app

app = create_app()
app.testing = True

with app.test_client() as client:
    response = client.post('/chat', json={'query': 'What is RAG?', 'user_id': 99})
    print(response.get_json())

# Check the database
conn = sqlite3.connect('rag_chatbot.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM chats WHERE user_id = 99')
rows = cursor.fetchall()
print('DB Rows:', rows)
conn.close()
