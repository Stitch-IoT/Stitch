import sqlite3

# Connect to the database (or create a new one if it doesn't exist)
connection = sqlite3.connect('words_storage.db')
cursor = connection.cursor()

# Create a table for storing words
cursor.execute('''
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL
    )
''')

# Save changes
connection.commit()

# Close the connection
connection.close()


def add_word(word):
    connection = sqlite3.connect('words_storage.db')
    cursor = connection.cursor()

    # Insert the word into the table
    cursor.execute('INSERT INTO words (word) VALUES (?)', (word,))

    # Save changes
    connection.commit()

    # Close the connection
    connection.close()


# # Example calls to the function (one call per word)
# add_word('python')
# add_word('be careful')
# add_word('attention')

def get_all_words():
    get_connection = sqlite3.connect('words_storage.db')
    get_cursor = get_connection.cursor()

    # Select all words from the table
    get_cursor.execute('SELECT word FROM words')
    words = get_cursor.fetchall()

    # Close the connection
    get_connection.close()

    return words

# Example call to the function
all_words = get_all_words()
print(all_words)

def delete_word(word):
    connection = sqlite3.connect('words_storage.db')
    cursor = connection.cursor()

    # Delete the word from the table
    cursor.execute('DELETE FROM words WHERE word = ?', (word,))

    # Save changes
    connection.commit()

    # Close the connection
    connection.close()

# Example call to delete a word
delete_word('python')
delete_word('be careful')
delete_word('be careful')

