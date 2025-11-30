import json
import string
import random
from pathlib import Path

db_file = Path("database.json")

def load_db():
    if db_file.exists():
        return {}
    with open(db_file, "r") as f:
        return json.load(f)

def save_db(db):
    with open(db_file, "w") as f:
        json.dump(db, f)

def generate_code(length=6):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))

def shorten_url(url):
    db = load_db()

    while True:
        code = generate_code()
        if code not in db:
            break
    db[code] = url
    save_db(db)
    return code

def retrieve_url(short_code):
    db = load_db()
    return db.get(short_code, None)

if __name__ == "__main__":
    print("1) Shorten URL")
    print("2) Retrieve URL")
    choice = input("Enter your choice: ")
    if choice == "1":
        url = input("Enter the URL to shorten: ")
        code = shorten_url(url)
        print(f"Shortened URL: http://short.ly/{code}")
    elif choice == "2":
        code = input("Enter the short code: ")
        url = retrieve_url(code)
        print(f"original URL: {url}")
    else:
        print("Invalid choice")