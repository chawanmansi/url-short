from flask import Flask, request, redirect
import sqlite3
import string
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            conn = sqlite3.connect('urls.db')
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY AUTOINCREMENT, original_url TEXT, short_url TEXT)')
            cursor.execute('SELECT short_url FROM urls WHERE original_url = ?', (url,))
            row = cursor.fetchone()
            if row:
                short_url = row[0]
            else:
                while True:
                    short_url = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
                    cursor.execute('SELECT id FROM urls WHERE short_url = ?', (short_url,))
                    row = cursor.fetchone()
                    if not row:
                        break
                cursor.execute('INSERT INTO urls (original_url, short_url) VALUES (?, ?)', (url, short_url))
                conn.commit()
            conn.close()
            return f'<body style="background-color: #87CEEB;"><div style="display: flex; justify-content: center; align-items: center; height: 100vh;"><p style="text-align: center;">Shortened URL you entered: <a href="{request.host_url}{short_url}">{request.host_url}{short_url}</a></p></div></body>'
    return '''
        <body style="background-color: #87CEEB;">
            <div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
                <form method="post">
                    <label for="url">Please enter the URL:</label>
                    <input type="text" name="url" id="url">
                    <input type="submit" value="Short it !!">
                    <label for="op">Made by Mansi</label>
                </form>
            </div>
        </body>
    '''

@app.route('/<short_url>')
def redirect_to_url(short_url):
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('SELECT original_url FROM urls WHERE short_url = ?', (short_url,))
    row = cursor.fetchone()
    if row:
        original_url = row[0]
        conn.close()
        return redirect(original_url)
    else:
        conn.close()
        return '<body style="background-color: #87CEEB;"><div style="display: flex; justify-content: center; align-items: center; height: 100vh;"><p style="text-align: center;">URL NOT FOUND ;( <a href=</a></p></div></body>'

if __name__ == '__main__':
    app.run(debug=True)
