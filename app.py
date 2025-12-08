# Backend code for Personal Portfolio Website

from flask import Flask, render_template
import markdown
import os

app = Flask(__name__)

# Configuration
# We point to the 'posts' folder to read markdown files
POSTS_DIR = 'posts'

@app.route('/')
def home():
    """
    Renders the homepage.
    This will be the main landing page with your hero section.
    """
    return render_template('home.html')

@app.route('/projects')
def projects():
    """
    Renders the Portfolio/Projects page.
    """
    return render_template('projects.html')


@app.route('/cv')
def cv():
    """
    Renders the CV page.
    """
    return render_template('cv.html')




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