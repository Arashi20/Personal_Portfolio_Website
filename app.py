# Backend code for Personal Portfolio Website

from flask import Flask, render_template, abort, url_for
import markdown
import os

app = Flask(__name__)


POSTS_DIR = 'posts' # Directory where markdown blog posts are stored

# Simple in-memory metadata. For many projects, read from JSON/YAML/db.
PROJECTS = {
    "bachelor-thesis-awe": {
        "title": "Awe & The Overview Effect",
        "title_short": "Bachelor Thesis: A VR Study",
        "slug": "bachelor-thesis-awe",
        "subtitle": """How effectively can awe and the Overview Effect be elicited
                    in a Cave Automatic Virtual Environment (CAVE) and what
                    are the resulting impacts of such experiences on one’s
                    self-size perception?""",
        "description_html": """
            <p>This thesis studies the psychological phenomenon of awe and the Overview Effect.
               It contains chapters on theory, experimental design and results.</p>
            
        """,
        "file": "docs/Bachelor_Thesis_Awe.pdf",  # file inside static/docs/
    
        
    },
    # add other dedicated project pages similarly
}


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


@app.route('/projects/<slug>')
def project_detail(slug):
    project = PROJECTS.get(slug)
    if not project:
        abort(404)
    # project.file is a path relative to static/
    # url_for will be used in template to get correct static URL
    return render_template('project_detail.html', project=project)


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
        return render_template('404.html'), 404 
    

@app.errorhandler(404)
def page_not_found(error):
    """
    Custom 404 error page handler.
    Shows a user-friendly error page instead of Flask's default.
    """
    # Render the custom 404 template
    return render_template('404.html'), 404



if __name__ == "__main__":
    app.run(debug=False)  # Set debug=True for development only