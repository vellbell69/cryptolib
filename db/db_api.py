import sqlite3
import random

DB_PATH = "db\cryptolibs.db"

def add_user(id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO 'users' ('user_id') VALUES (?)", (id,))
    cur.execute("INSERT OR IGNORE INTO 'active_users' ('user_id') VALUES (?)", (id,))
    conn.commit()
    conn.close()

def del_active_user(id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"DELETE FROM 'active_users' WHERE user_id='{id}'")
    conn.commit()
    conn.close()

def count_user():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT() FROM users")
    count = cur.fetchall()[0][0]
    conn.commit()
    conn.close()
    return count

def get_all_active_user_id():
    user_id = []
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM active_users")
    data = cur.fetchall()
    for id in data:
        user_id.append(id[0])
    conn.commit()
    conn.close()
    return user_id


#_______________________________________________________________________________________________

def category(key):
    category = []
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM category")
        data = cur.fetchall()
        if key == "get":
            for item in data:
                category.append([f"get:{item[0]}", item[1]])
        if key == "add":
            for item in data:
                category.append([f"add:{item[0]}", item[1]])
        if key == "del":
            for item in data:
                category.append([f"del:{item[0]}", item[1]])
        if key == "article_del":
            for item in data:
                category.append([f"article_del:{item[0]}", item[1]])
#здесь callbacks                
        if key == "call_get":
            for item in data:
                category.append(f"get:{item[0]}")
        if key == "call_add":
            for item in data:
                category.append(f"add:{item[0]}")
        if key == "call_del":
            for item in data:
                category.append(f"del:{item[0]}")
    return category[::-1]

def article(key, choose):
    article = []
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM articles WHERE category_id='{key}'")
        data = cur.fetchall()
        for item in data:
            if choose == "get":
                article.append([f"article_get:{item[0]}", item[1], item[2], item[3], item[4], item[5]])
            if choose == "add":
                article.append([f"article_add:{item[0]}", item[1], item[2], item[3], item[4], item[5]])
            if choose == "del":
                article.append([f"article_del_call:{item[0]}", item[1], item[2], item[3], item[4], item[5]])
            
            if choose == "call_get":
                article.append(f"article_get:{item[0]}")
            if choose == "call_add":
                article.append(f"article_add:{item[0]}")
            if choose == "call_del":
                article.append(f"article_del:{item[0]}")
    return article

def article_data(key):
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM articles WHERE id='{key}'")
        data = cur.fetchall()
        return data

def category_add(name):
    id = random.randint(10000000, 99999999)
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute("INSERT INTO 'category' ('id', 'category_name') VALUES (?, ?)", (id, name,))
        con.commit()

def category_del(key):
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute(f"DELETE FROM category WHERE id='{key}'")
        cur.execute(f"DELETE FROM articles WHERE category_id='{key}'")
        con.commit()

def article_add(cid, name, author, discr, link):
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute("INSERT INTO 'articles' ('category_id', 'name', 'author', 'description', link) VALUES (?, ?, ?, ?, ?)", (cid, name, author, discr, link))
        con.commit()

def article_del(key):
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute(f"DELETE FROM articles WHERE id='{key}'")
        con.commit()