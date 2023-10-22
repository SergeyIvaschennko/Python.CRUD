from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect("phonebook.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route('/add', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        conn = sqlite3.connect("phonebook.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/')
def index():
    conn = sqlite3.connect("phonebook.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()
    conn.close()
    return render_template('index.html', contacts=contacts)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_contact(id):
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        conn = sqlite3.connect("phonebook.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE contacts SET name=?, phone=? WHERE id=?", (name, phone, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        conn = sqlite3.connect("phonebook.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts WHERE id=?", (id,))
        contact = cursor.fetchone()
        conn.close()
        return render_template('update.html', contact=contact)

@app.route('/delete/<int:id>')
def delete_contact(id):
    conn = sqlite3.connect("phonebook.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    create_table()
    app.run(debug=False)
