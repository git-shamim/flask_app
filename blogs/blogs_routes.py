# blogs/blogs_routes.py
import os
import json
import markdown
from flask import Blueprint, render_template, current_app

blogs_bp = Blueprint("blogs", __name__, template_folder="../templates")

BLOGS_DATA_PATH = os.path.join(os.path.dirname(__file__), "blogs_data.json")
MARKDOWN_DIR = os.path.join(os.path.dirname(__file__), "markdown")

@blogs_bp.route("/blogs/<blog_slug>")
def blog_article(blog_slug):
    try:
        with open(BLOGS_DATA_PATH, 'r') as f:
            blogs = json.load(f)
    except Exception as e:
        current_app.logger.error(f"❌ Error loading blogs_data.json: {e}")
        return render_template("404.html"), 404

    blog = next((b for b in blogs if b["slug"] == blog_slug), None)
    if not blog:
        return render_template("404.html"), 404

    markdown_path = os.path.join(MARKDOWN_DIR, blog["markdown_file"])
    if not os.path.exists(markdown_path):
        current_app.logger.error(f"Markdown not found: {markdown_path}")
        return render_template("404.html"), 404

    try:
        with open(markdown_path, 'r') as f:
            md_content = f.read()
            html_content = markdown.markdown(md_content, extensions=["fenced_code", "codehilite", "tables"])
    except Exception as e:
        current_app.logger.error(f"❌ Error reading markdown file: {e}")
        return render_template("404.html"), 404

    return render_template(
        "blog_article.html",
        title=blog["title"],
        description=blog["description"],
        content=html_content,
        medium_url=blog["medium_url"],
        image=blog["image"]
    )
