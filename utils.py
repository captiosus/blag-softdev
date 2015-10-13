import sqlite3
def authenticate(username,password):
    conn = sqlite3.connect("blag.db")
    c = conn.cursor()
    q = "SELECT password from users WHERE username == %s"%username 
    c.execute(q)
    result = c.fetchall()
    return result == password
    
