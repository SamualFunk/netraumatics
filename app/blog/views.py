from flask import render_template
from app.blog import blog
import os
import yaml
import markdown
from datetime import datetime


def load_posts():
    """Load all markdown posts from posts/ directory"""
    posts = []
    posts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'posts')
    
    if not os.path.exists(posts_dir):
        return posts
    
    for filename in sorted(os.listdir(posts_dir), reverse=True):
        if filename.endswith('.md'):
            filepath = os.path.join(posts_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Parse frontmatter
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        frontmatter = yaml.safe_load(parts[1])
                        post_content = parts[2].strip()
                    else:
                        frontmatter = {}
                        post_content = content
                else:
                    frontmatter = {}
                    post_content = content
                
                # Convert markdown to HTML
                html_content = markdown.markdown(post_content)
                
                post = {
                    'id': filename.replace('.md', ''),
                    'title': frontmatter.get('title', 'Untitled'),
                    'author': frontmatter.get('author', 'Anonymous'),
                    'date': frontmatter.get('date', datetime.now()),
                    'content': html_content
                }
                posts.append(post)
    
    return posts


@blog.route('/')
def index():
    """Display all blog posts on single page"""
    posts = load_posts()
    return render_template('index.html', posts=posts)
