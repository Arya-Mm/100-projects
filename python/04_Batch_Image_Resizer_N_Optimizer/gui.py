import tkinter as tk
from tkinter import filedialog, messagebox
from resizer import process_images
from pathlib import Path

def select_input():
    path = filedialog.askdirectory()
    input_entry.set(path)

def select_output():
    path = filedialog.askdirectory()
    output_entry.set(path)

def start_processing():
    input_path = Path(input_entry.get())
    output_path = Path(output_entry.get())

    if not input_path.exists():
        messagebox.showerror("Error", "Invalid input folder")
        return

    process_images(
        input_path, output_path,
        width=1080,
        height=None,
        quality=85,
        format=None,
        watermark="Arya",
        workers=4,
        recursive=True
    )

    messagebox.showinfo("Done", "Processing Completed!")

root = tk.Tk()
root.title("Image Resizer & Optimizer")

tk.Label(root, text="Input Folder").pack()
input_entry = tk.Entry(root, width=40)
input_entry.pack()
tk.Button(root, text="Browse", command=select_input).pack()

tk.Label(root, text="Output Folder").pack()
output_entry = tk.Entry(root, width=40)
output_entry.pack()
tk.Button(root, text="Browse", command=select_output).pack()

tk.Button(root, text="Start", command=start_processing).pack(pady=10)

root.mainloop()
