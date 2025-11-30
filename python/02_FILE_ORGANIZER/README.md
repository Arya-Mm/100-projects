Project 02 — Python File Organizer

A fully automated Python tool that organizes files in your Downloads folder by sorting them into category-based subfolders.
This project demonstrates automation, file handling, code modularity, and clean project structure — similar to what real software engineers build for system utilities.

Why This Project Exists

Your Downloads folder becomes messy over time and fills with hundreds of random files — images, PDFs, installers, code files, videos, torrents, etc.

Manually cleaning it is:

Slow
Boring
Error-prone
Not scalable

This Python automation tool solves that problem by instantly organizing all files into neatly structured folders based on their file types.

## **How It Works**

The script scans your Downloads folder, reads each file’s extension, categorizes it using a predefined mapping, creates the target folder if it doesn’t exist, and then moves the file into the correct category.


## **Supported Categories**

* Images
* Videos
* Documents
* Audio
* Archives
* Installers
* Code Files
* Torrents
* Others (fallback)


## **How to Use**

1. Update the `folder` path in `organizer.py`.
2. Run the script:

   ```
   python organizer.py
   ```
3. Your files will be moved into organized category folders automatically.


## **Project Structure (Short)**

```
02_FILE_ORGANIZER/
│── organizer.py    # Main script
│── README.md       # Project documentation
```


## **Future Improvements**

* Add a GUI
* Add logging & error tracking
* Add undo/restore feature
* Add configuration via JSON
* Add support for custom user-defined categories



**Tech Used**

* Python 3
* pathlib
* shutil


 **Author**
**Arya M** 

