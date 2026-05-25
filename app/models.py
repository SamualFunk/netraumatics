from datetime import datetime
from app import db


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), default='Anonymous')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Post {self.title}>'

    @staticmethod
    def create(title, content, author='Anonymous'):
        """Create a new blog post"""
        post = Post(title=title, content=content, author=author)
        db.session.add(post)
        db.session.commit()
        return post

    @staticmethod
    def find_all():
        """Get all posts, sorted by creation date (newest first)"""
        return Post.query.order_by(Post.created_at.desc()).all()

    @staticmethod
    def find_by_id(post_id):
        """Find a post by ID"""
        return Post.query.get(post_id)

    @staticmethod
    def update(post_id, title=None, content=None, author=None):
        """Update a post"""
        post = Post.query.get(post_id)
        if not post:
            return False

        if title is not None:
            post.title = title
        if content is not None:
            post.content = content
        if author is not None:
            post.author = author
        
        post.updated_at = datetime.utcnow()
        db.session.commit()
        return True

    @staticmethod
    def delete(post_id):
        """Delete a post"""
        post = Post.query.get(post_id)
        if not post:
            return False
        
        db.session.delete(post)
        db.session.commit()
        return True
