import sqlite3
def authenticate(username,password):
    conn = sqlite3.connect("blag.db")
    c = conn.cursor()
    q = "SELECT password from posts WHERE username == %s"%username 
    c.execute(q)
    result = c.fetchall()
    return result == password
    
