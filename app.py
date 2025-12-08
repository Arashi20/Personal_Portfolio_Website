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
    Scans the 'posts' directory and lists all markdown files.
    """
    posts = []
    
    # robust check to ensure directory exists
    if os.path.exists(POSTS_DIR):
        # Get all files in the directory
        files = os.listdir(POSTS_DIR)
        
        for file in files:
            if file.endswith('.md'):
                # Extract the slug (filename without .md)
                slug = file[:-3]
                
                # Create a pretty title (replace underscores with spaces)
                title = slug.replace('_', ' ').title()
                
                # Add to our list
                posts.append({'slug': slug, 'title': title})
    
    # Sort posts alphabetically (or you could reverse sort to show newest if named by date)
    posts.sort(key=lambda x: x['title']) 
    
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