# Backend code for Personal Portfolio Website

from flask import Flask, render_template
import markdown
import os

app = Flask(__name__)


POSTS_DIR = 'posts' # Directory where markdown blog posts are stored

# Home Route
@app.route('/')
def home():
    """
    Renders the homepage.
    This will be the main landing page with your hero section.
    """
    return render_template('home.html')


# Projects Route
@app.route('/projects')
def projects():
    """
    Renders the Portfolio/Projects page.
    """
    return render_template('projects.html')

# CV Route
@app.route('/cv')
def cv():
    """
    Renders the CV page.
    """
    return render_template('cv.html')


# Blog Post Route
@app.route('/blog')
def blog():
    """
    Renders the Blog Index page.
    Expects files named like: YYYY-MM-DD_post_title.md
    Example: 2025-12-09_welcome.md
    """
    posts = []
    
    if os.path.exists(POSTS_DIR):
        files = os.listdir(POSTS_DIR)
        
        for file in files:
            if file.endswith('.md'):
                slug = file[:-3]  # Remove .md extension
                
                # Default values
                date_part = ""
                title_part = slug
                
                # Split filename by the first underscore
                # "2025-12-09_welcome" -> ["2025-12-09", "welcome"]
                if '_' in slug:
                    parts = slug.split('_', 1)
                    # Check if the first part looks like a date (simple length check)
                    if len(parts[0]) == 10: 
                        date_part = parts[0]
                        title_part = parts[1]
                
                # Pretty format the title
                pretty_title = title_part.replace('_', ' ').title()
                
                posts.append({
                    'slug': slug,            # Needed for the link URL
                    'title': pretty_title,   # Needed for display "Welcome"
                    'date': date_part,       # Needed for display "2025-12-09"
                    'filename': file         # Needed for sorting
                })
    
    # Sort by filename in REVERSE order (Newest dates first)
    posts.sort(key=lambda x: x['filename'], reverse=True)
    
    return render_template('blog.html', posts=posts)

# Individual Blog Post Route
@app.route('/blog/<title>')
def post(title):
    """
    Renders a specific blog post.
    It looks for a file named {title}.md in the posts directory.
    """
    # Construct the file path
    file_path = os.path.join(POSTS_DIR, f"{title}.md")
    
    # Check if file exists
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Convert markdown content to HTML
            html_content = markdown.markdown(content)
            # Pass the HTML content and the title to the template
            return render_template('post.html', content=html_content, title=title)
    else:
        # Simple 404 handling for now
        return "Post not found", 404

if __name__ == "__main__":
    app.run(debug=True)