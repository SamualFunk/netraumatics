from flask import render_template
from app.blog import blog
import os
import yaml
import markdown
from datetime import datetime


def _load_markdown_dir(folder):
    """Load all markdown entries from a top-level folder (e.g. posts/, divination/)"""
    items = []
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    content_dir = os.path.join(base_dir, folder)

    if not os.path.exists(content_dir):
        return items

    for filename in sorted(os.listdir(content_dir), reverse=True):
        if not filename.endswith('.md'):
            continue
        with open(os.path.join(content_dir, filename), 'r', encoding='utf-8') as f:
            content = f.read()

        frontmatter, body = {}, content
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1]) or {}
                body = parts[2].strip()

        items.append({
            'id': filename.replace('.md', ''),
            'title': frontmatter.get('title', 'Untitled'),
            'author': frontmatter.get('author', 'Anonymous'),
            'date': frontmatter.get('date', datetime.now()),
            'content': markdown.markdown(body),
            'meta': frontmatter,
        })
    return items


def load_posts():
    return _load_markdown_dir('posts')


def load_divinations():
    return _load_markdown_dir('divination')


@blog.route('/')
def index():
    """Display blog posts and divination entries on a single page"""
    posts = load_posts()
    divinations = load_divinations()
    return render_template('index.html', posts=posts, divinations=divinations)
