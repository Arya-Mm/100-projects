# 🏗️ **Simple Markdown Static Site Generator (with GUI + Live Reload Dev Server)**

This project is a **beginner-friendly, powerful static site generator** built entirely in Python.
It converts **Markdown → HTML**, applies **Jinja2 templates**, handles assets, and includes:

✅ A GUI
✅ A dev server
✅ Automatic rebuild-on-change
✅ Live browser reloading

This gives you a workflow similar to **Hugo, Jekyll, Astro, or Vite** — but simplified and coded by YOU.

---

# ⭐ Features

### 🔹 **1. Markdown → HTML Conversion**

* Converts all `.md` files inside the `/content` folder.
* Uses **Jinja2** templates for layout control.
* Output is written to `/site`.

### 🔹 **2. Template System**

* The `/templates/base.html` file is used as the default page wrapper.
* You can add CSS/JS in `/assets`.

### 🔹 **3. GUI App (Tkinter)**

The GUI allows you to:

* Select Markdown files
* Preview Markdown
* Build the full static site
* View live HTML output
* Build without using terminal

### 🔹 **4. Dev Server with Live Reload**

* Serves the static site at:

```
http://localhost:8000
```

* Watches the following folders for changes:

  * `/content`
  * `/templates`
  * `/assets`

Whenever a change is detected:

* The site is rebuilt
* Browser auto-refreshes (like Vite/Hugo)

### 🔹 **5. Auto-Rebuild on File Change**

Powered by Python’s `watchdog` library.

---

# 📂 Project Structure

```
05_SSG/
│
├── content/              # Your markdown files
├── templates/
│   └── base.html         # Jinja2 template
│
├── assets/               # CSS, JS, images
│
├── site/                 # Generated HTML output (auto-created)
│   └── .reload           # Timestamp file for live reload
│
├── build.py              # Markdown → HTML converter
├── gui_ssg.py            # GUI builder app
├── dev_server.py         # Live reload development server
└── README.md             # This file
```

---

# 🚀 How to Use

## 1️⃣ Install required dependencies

```
pip install markdown jinja2 watchdog
```

---

## 2️⃣ Run the GUI (Optional)

```
python gui_ssg.py
```

The GUI lets you:

* Choose markdown files
* Build static site
* Preview output

---

## 3️⃣ Build the site (Manual mode)

```
python build.py
```

Generates HTML files inside `/site`.

---

## 4️⃣ Start the Dev Server (Live Reload)

```
python dev_server.py
```

You will see:

```
[SERVER] Live server → http://localhost:8000
[WATCH] Watching content/
[WATCH] Watching templates/
[WATCH] Watching assets/
```

Open browser:

👉 [http://localhost:8000](http://localhost:8000)

Edit any `.md`, `.html`, or asset → page auto rebuilds + refreshes.

---

# 🧠 How It Works (Concept Summary)

### ✔ Markdown Conversion

We use `markdown` library to turn `.md` → raw HTML.

### ✔ Jinja2 Templating

Wrap the raw HTML inside `base.html`:

```
{{ content }}
```

### ✔ File Watching

`watchdog` listens for file changes.

### ✔ Live Reload

`.reload` timestamp is updated → browser checks every second
If changed → browser reloads automatically.

---

# 🛠 Technologies Used

| Feature         | Library     |
| --------------- | ----------- |
| Markdown → HTML | `markdown`  |
| Templates       | `jinja2`    |
| File watching   | `watchdog`  |
| GUI             | Tkinter     |
| Live server     | http.server |
| Auto reload     | custom JS   |

---

# 📌 Future Enhancements

✔ Add CSS minimizer
✔ Add support for blog index pages
✔ Multi-page template support
✔ Add a sidebar navigation generator
✔ Export to PDF (optional)

---
