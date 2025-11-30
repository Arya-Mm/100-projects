# 📌 Project 03 — URL Shortener (Python)

A simple offline URL shortener that converts long URLs into short codes and stores them in a local JSON database.
You can shorten URLs, retrieve them, and automatically open the original link in your browser.



## ⭐ Features

✔ Shorten any URL
✔ Automatically adds `https://` if missing
✔ Generates unique random short codes
✔ Stores URL mappings in `database.json`
✔ Retrieve URL using short code
✔ Detects if user pastes full short link
✔ Optionally opens URL in browser
✔ Beginner-friendly, clean Python code


## 📂 Project Structure

```
03_URL_Shortener/
│── shortener.py
│── database.json
│── README.md
```

## 🧠 How It Works

### 🔹 1. Code Generator

Creates a 6-character short code using:

```
a-z A-Z 0-9
```

### 🔹 2. JSON Database

All shortened URLs are stored in `database.json` as:

```json
{
    "Xy28Lm": "https://google.com"
}
```

### 🔹 3. Two Main Operations

1. **Shorten URL**
2. **Retrieve URL**

The script also fixes user mistakes:

* Adds `https://` if missing
* Extracts code if user pastes full link
* Opens in browser if user chooses yes

## 🚀 Usage

### 👉 1. Run the script

```
python shortener.py
```

### 👉 2. Shorten URL

```
1) Shorten URL
Enter the URL to shorten: google.com
```

Output:

```
Short URL created: http://short.ly/Xy28Lm
```

### 👉 3. Retrieve URL

```
2) Retrieve URL
Enter the short code: Xy28Lm
```

Output:

```
Original URL: https://google.com
```

## 🧰 Requirements

No external libraries.
Everything uses Python’s built-in modules:

* json
* random
* string
* pathlib
* webbrowser

## 🎯 What You Learned

* JSON as a mini-database
* How to generate random codes
* Dictionaries for key–value storage
* Pathlib for safe file handling
* Input sanitization
* Browser automation via Python
* Writing CLI-based tools

