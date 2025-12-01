import os
from pathlib import Path
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

import markdown
import frontmatter
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime


def markdown_to_html(md_text):
    md = markdown.Markdown(extensions=["fenced_code", "tables", "toc"])
    return md.convert(md_text)

def build_site(content_dir, template_dir, assets_dir, output_dir, log_widget):
    content_dir = Path(content_dir)
    template_dir = Path(template_dir)
    assets_dir = Path(assets_dir)
    output_dir = Path(output_dir)

    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(["html", "xml"])
    )

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)


    if assets_dir.exists():
        shutil.copytree(assets_dir, output_dir / "assets", dirs_exist_ok=True)

    pages_meta = []

    for md_file in content_dir.rglob("*.md"):
        post = frontmatter.load(md_file)
        html_body = markdown_to_html(post.content)
        metadata = post.metadata
        
        title = metadata.get("title", md_file.stem)
        date = metadata.get("date", "")

        rel_path = md_file.relative_to(content_dir).with_suffix(".html")
        out_path = output_dir / rel_path
        out_path.parent.mkdir(parents=True, exist_ok=True)

        template = env.get_template("base.html")

        rendered = template.render(
            content=html_body,
            title=title,
            date=date,
            site_title="My Static Site",
            year=datetime.date.today().year
        )

        out_path.write_text(rendered, encoding="utf-8")

        pages_meta.append({
            "title": title,
            "url": "/" + str(rel_path).replace("\\", "/"),
            "date": date
        })

        log_widget.insert(tk.END, f"[BUILT] {out_path}\n")
        log_widget.see(tk.END)


    index_items = ["<h2>Pages</h2><ul>"]
    for p in pages_meta:
        index_items.append(f'<li><a href="{p["url"]}">{p["title"]}</a></li>')
    index_items.append("</ul>")

    template = env.get_template("base.html")
    index_html = template.render(
        content="\n".join(index_items),
        title="Home",
        site_title="My Static Site",
        year=datetime.date.today().year
    )

    (output_dir / "index.html").write_text(index_html, encoding="utf-8")
    log_widget.insert(tk.END, "[BUILT] index.html\n")
    log_widget.see(tk.END)

    messagebox.showinfo("Success", "Site built successfully!")

root = tk.Tk()
root.title("Markdown → Static Site Generator")
root.geometry("700x550")

def choose_dir(entry_widget):
    path = filedialog.askdirectory()
    if path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, path)


tk.Label(root, text="Content Folder (Markdown)").pack()
content_entry = tk.Entry(root, width=80)
content_entry.pack()
tk.Button(root, text="Browse", command=lambda: choose_dir(content_entry)).pack()

tk.Label(root, text="Templates Folder").pack()
template_entry = tk.Entry(root, width=80)
template_entry.pack()
tk.Button(root, text="Browse", command=lambda: choose_dir(template_entry)).pack()

tk.Label(root, text="Assets Folder").pack()
assets_entry = tk.Entry(root, width=80)
assets_entry.pack()
tk.Button(root, text="Browse", command=lambda: choose_dir(assets_entry)).pack()

tk.Label(root, text="Output Folder (site/)").pack()
output_entry = tk.Entry(root, width=80)
output_entry.pack()
tk.Button(root, text="Browse", command=lambda: choose_dir(output_entry)).pack()


tk.Button(
    root,
    text="Build Site",
    bg="green",
    fg="white",
    font=("Arial", 14),
    command=lambda: build_site(
        content_entry.get(),
        template_entry.get(),
        assets_entry.get(),
        output_entry.get(),
        log_area
    )
).pack(pady=10)

log_area = scrolledtext.ScrolledText(root, width=80, height=15)
log_area.pack(pady=10)

root.mainloop()
