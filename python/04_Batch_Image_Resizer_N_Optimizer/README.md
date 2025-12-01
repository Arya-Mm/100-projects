# 📸 Batch Image Resizer & Optimizer

A fast, powerful Python tool to **resize, compress, convert, and watermark images in bulk** using a clean CLI, GUI (Tkinter), and Web UI (Streamlit).

Supports: JPG, PNG, WEBP, BMP, TIFF
Features: Resize • Compress • Watermark • Format Convert • EXIF Preserve • Multithreading • Logging

---

## 🚀 Features

### ✔ Bulk Resize

Resize thousands of images using width or height:

```
--width 1080
--height 720
```

### ✔ Smart Compression

Automatically compresses images while keeping quality.

### ✔ Watermark Support

Add your name or brand watermark:

```
--watermark "Arya"
```

### ✔ Format Conversion

Convert PNG → JPG or any format → any format:

```
--format jpg
```

### ✔ EXIF Preservation

Keeps metadata such as:

* Image orientation
* Camera info
* GPS location
* Timestamps

### ✔ Multithreading

Uses all CPU cores for **maximum speed**:

```
--workers 8
```

### ✔ Error Logging

Bad/corrupt images are logged in:

```
errors.log
```

### ✔ Three Interfaces

| Interface  | File         | Use-case                              |
| ---------- | ------------ | ------------------------------------- |
| **CLI**    | `resizer.py` | Fastest, automation, batch processing |
| **GUI**    | `gui.py`     | Easy for non-technical users          |
| **Web UI** | `web_ui.py`  | Clean modern browser interface        |

---

# 🛠 Installation

Make sure you have Python installed.

Install dependencies:

```
pip install pillow tqdm streamlit
```

---

# ▶️ How to Use

---

# 1️⃣ **CLI Usage**

Run:

```
python resizer.py -i input -o output --width 1080
```

### Examples

### Resize:

```
python resizer.py -i input -o output --width 1080
```

### Resize + Watermark:

```
python resizer.py -i input -o output --width 1080 --watermark "Arya"
```

### Convert PNG → JPG:

```
python resizer.py -i input -o output --format jpg
```

### Use 8 Threads:

```
python resizer.py -i input -o output --workers 8
```

---

# 2️⃣ **GUI Version**

Run:

```
python gui.py
```

Features:

* Select input folder
* Select output folder
* Apply resize
* Apply watermark
* One-click batch processing

---

# 3️⃣ **Web UI (Streamlit)**

Run:

```
streamlit run web_ui.py
```

Browser opens at:

```
http://localhost:8501
```

---

# 📂 Folder Structure

```
03_IMAGE_RESIZER/
│
├── resizer.py      # Main CLI tool
├── gui.py          # Tkinter GUI
├── web_ui.py       # Streamlit browser UI
├── README.md       # Documentation
├── errors.log      # Logged errors
├── input/          # Put raw images here
└── output/         # Processed images appear here
```

---

# 🧠 How It Works (Internals)

### 🔹 `Pillow`

Handles:

* Loading images
* Resizing
* Watermark
* Saving formats
* Compression
* EXIF metadata

### 🔹 `tqdm`

Shows progress bars for large batches.

### 🔹 Multithreading

Uses:

```
ThreadPoolExecutor
```

to process multiple images at once.

### 🔹 EXIF Copy

We extract original EXIF:

```
img.getexif()
```

and reattach it so metadata is preserved.

### 🔹 Error Logging

Any failed image is appended to:

```
errors.log
```



# 🧪 Testing Checklist

| Test         | Should Work          |
| ------------ | -------------------- |
| Resize       | Output size changes  |
| Compression  | File size smaller    |
| Watermark    | Visible bottom-right |
| PNG → JPG    | Format converted     |
| EXIF         | Metadata preserved   |
| 8 workers    | Faster               |
| GUI          | Works on Tkinter     |
| Streamlit UI | Works in browser     |
| Logging      | errors.log created   |



# 📌 Future Enhancements (Optional)

* Preserve PNG ICC color profiles
* Add watermark opacity & scaling
* Batch rename options
* Drag & drop GUI
* Cloud upload (S3/Drive/Dropbox)


# 💡 Summary

This project teaches:

* Image processing
* CLI design
* GUIs with Tkinter
* Web apps with Streamlit
* Multithreading
* File formats (PNG, JPEG, EXIF)
* Real-world automation skills

