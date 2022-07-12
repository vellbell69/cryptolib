import sqlite3

def add_user(id):
    conn = sqlite3.connect("cryptolibs.db")
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO 'users' ('user_id') VALUES (?)", (id,))
    cur.execute("INSERT OR IGNORE INTO 'active_users' ('user_id') VALUES (?)", (id,))
    conn.commit()
    conn.close()

def del_active_user(id):
    conn = sqlite3.connect("cryptolibs.db")
    cur = conn.cursor()
    cur.execute(f"DELETE FROM 'active_users' WHERE user_id='{id}'")
    conn.commit()
    conn.close()

def count_user():
    conn = sqlite3.connect("cryptolibs.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT() FROM users")
    count = cur.fetchall()[0][0]
    conn.commit()
    conn.close()
    return count

def add_item(ccode, cname, name, avtor, link, disc):
    conn = sqlite3.connect("cryptolibs.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO 'articles' ('category_code', 'category_name', 'name', 'avtor', 'link', 'subscribe') VALUES (?, ?, ?, ?, ?, ?)", (ccode, cname, name, avtor, link, disc,))
    conn.commit()
    conn.close()



def get_categories():
    conn = sqlite3.connect("cryptolibs.db")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT category_code, category_name FROM articles")
    categories = cur.fetchall()
    conn.close()
    return categories

def get_callback():
    conn = sqlite3.connect("cryptolibs.db")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT category_code FROM articles")
    categories = cur.fetchall()
    conn.close()
    callback = []
    for item in categories:
        callback.append(item[0])
    return callback

def get_callback_articles():
    conn = sqlite3.connect("cryptolibs.db")
    cur = conn.cursor()
    cur.execute("SELECT id FROM articles")
    articles_callback = cur.fetchall()
    conn.close()
    callback = []
    for item in articles_callback:
        callback.append(item[0])
    return callback 

def get_items(category_code):
    conn = sqlite3.connect("cryptolibs.db")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM articles WHERE category_code='{category_code}'")
    articles = cur.fetchall()
    conn.close()
    return articles

def get_articles(id_article):
    conn = sqlite3.connect("cryptolibs.db")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM articles WHERE id='{id_article}'")
    articles = cur.fetchall()
    conn.close()
    return articles


#._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._

def get_add_callback():
    conn = sqlite3.connect("cryptolibs.db")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT category_code FROM articles")
    categories = cur.fetchall()
    conn.close()
    callback = []
    for item in categories:
        callback.append(f"add:{item[0]}")
    callback.append("create_category")
    return callback

def get_add_callback():
    conn = sqlite3.connect("cryptolibs.db")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT category_code FROM articles")
    categories = cur.fetchall()
    conn.close()
    callback = []
    for item in categories:
        callback.append(f"add:{item[0]}")
    callback.append("create_category")
    return callback

def get_add_category_info(key):
    new_key = key[key.find(":") + 1 : ]
    conn = sqlite3.connect("cryptolibs.db")
    cur = conn.cursor()
    cur.execute(f"SELECT DISTINCT category_name FROM articles WHERE category_code='{new_key}'")
    data = []
    data.append(cur.fetchall()[0][0])
    data.append(new_key)
    conn.close()
    return data

#.......................................

def get_del_callback():
    conn = sqlite3.connect("cryptolibs.db")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT category_code FROM articles")
    categories = cur.fetchall()
    conn.close()
    callback = []
    for item in categories:
        callback.append(f"del:{item[0]}")
    return callback

def get_del_callback_articles():
    conn = sqlite3.connect("cryptolibs.db")
    cur = conn.cursor()
    cur.execute("SELECT id FROM articles")
    articles_callback = cur.fetchall()
    conn.close()
    callback = []
    for item in articles_callback:
        callback.append(f"del:{item[0]}")
    return callback 

def del_item(id):
    conn = sqlite3.connect("cryptolibs.db")
    cur = conn.cursor()
    cur.execute(f"DELETE FROM 'articles' WHERE id='{id}'")
    conn.commit()
    conn.close()

#__________________________________________

def get_all_user_id():
    user_id = []
    conn = sqlite3.connect("cryptolibs.db")
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users")
    data = cur.fetchall()
    for id in data:
        user_id.append(id[0])
    conn.commit()
    conn.close()
    return user_id


def get_notify_article():
    conn = sqlite3.connect("cryptolibs.db")
    cur = conn.cursor()
    notify_message = []
    cur.execute("SELECT notify_text FROM notify_articles")
    data = cur.fetchall()
    conn.commit()
    conn.close()
    for item in data:
        notify_message.append(item[0])
    return notify_message

def add_notify_article(text):
    conn = sqlite3.connect("cryptolibs.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO 'notify_articles' ('notify_text') VALUES (?)", (text,))
    conn.commit()
    conn.close()

def del_notify_article():
    conn = sqlite3.connect("cryptolibs.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM 'notify_articles'")
    conn.commit()
    conn.close()

def get_all_active_user_id():
    user_id = []
    conn = sqlite3.connect("cryptolibs.db")
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM active_users")
    data = cur.fetchall()
    for id in data:
        user_id.append(id[0])
    conn.commit()
    conn.close()
    return user_id
