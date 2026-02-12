from flask import Flask, render_template, abort, url_for, request, send_from_directory 
from flask_talisman import Talisman
from werkzeug.middleware.proxy_fix import ProxyFix
import markdown
import os
import re

app = Flask(__name__)

# ---------------------------------------------------------
# SECURITY CONFIGURATION (Railway/Production)
# 1. ProxyFix: Tells Flask it is behind a proxy (Railway)

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

# 2. Talisman: Forces HTTPS and sets security headers.
#    content_security_policy=None allows inline scripts/styles 
#    (which you use for Google Analytics and animations).

Talisman(app, content_security_policy=None, force_https=True)
# ---------------------------------------------------------



POSTS_DIR = 'posts' # Directory where markdown blog posts are stored

# Project-specific detailed metadata
PROJECTS = {
    "bachelor-thesis-awe": {
        "title": "Awe & The Overview Effect",
        "title_short": "Bachelor Thesis: A VR Study",
        "slug": "bachelor-thesis-awe", # used in URL
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

    # add other dedicated project pages similarly..
}


# All Projects
PROJECTS_LIST = [
    {
        "title": "Stock Portfolio Dashboard (INACTIVE)",
        "badges": ["Python", "Flask", "APIs", "HTML/CSS"],
        "desc": "A comprehensive full-stack web application built with Flask and HTML to track my stock portfolio. Features real-time data updates, Discounted Cash Flow (DCF) analysis, a wishlist for potential investments, a page for adding notes on stocks, and performance metrics.",
        "url": "https://github.com/Arashi20/Stock_Portfolio_Dashboard",
        "button": "VIEW CODE",
        "icon": "fab fa-github",
        "external": True
    },
    {
        "title": "AI Stock Research Agent",
        "badges": ["LangChain", "LLMs", "Agents", "Streamlit", "Python"],
        "desc": "An autonomous Multi-Agent System to research financial markets. Agents scrape news, analyze sentiment, check technical indicators, and compile reports. The system automatically generates a comprehensive stock research report for any ticker symbol entered.",
        "url": "https://github.com/Arashi20/stock-research-MAS",
        "button": "VIEW CODE",
        "icon": "fab fa-github",
        "external": True
    },
    {
        "title": "Personal Portfolio Website",
        "badges": ["Flask", "HTML/CSS", "Design"],
        "desc": "The website you are looking at now — minimalist, high-performance and responsive. Pages: Home, Projects, CV, and Blog. I built this website from scratch because I wanted full control over the design and functionality. It's built with Flask for easy content management and deployment.",
        "url": "https://github.com/Arashi20/Personal_Portfolio_Website",
        "button": "VIEW CODE",
        "icon": "fab fa-github",
        "external": True
    },
    {
        "title": "Bachelor Thesis: Awe & The Overview Effect",
        "badges": ["Research", "Awe", "Psychology", "Data Analysis", "Virtual Reality", "Python/R"],
        "desc": "For my Bachelor Thesis, I conducted a detailed investigation into awe and the Overview Effect, using the CAVE VR system at the DAF Technology lab. My research focused on how virtual reality experiences can induce feelings of awe and the Overview Effect.",
        "url": "/projects/bachelor-thesis-awe",
        "button": "OPEN PROJECT",
        "icon": "fa fa-external-link-alt",
        "external": False  # Internal Flask route, not an external link!
    },
    {
        "title": "EEG Exploration & Probabilistic Modeling",
        "badges": ["Python", "MNE", "Data Analysis", "PyMC", "Matplotlib/Seaborn"],
        "desc": "A project focused on exploring and analyzing EEG data using the MNE library in Python. Includes data preprocessing, visualization of brain activity, and extraction of meaningful insights from EEG signals.",
        "url": "https://github.com/Arashi20/EEG-Exploration",
        "button": "VIEW CODE",
        "icon": "fab fa-github",
        "external": True
    },
    {
        "title": "OWASP Juice Shop - ZAP Scan",
        "badges": ["Docker", "OWASP ZAP", "Security Testing", "Reporting"],
        "desc": "A small hands-on project to run OWASP Juice Shop (an intentionally vulnerable web app) and OWASP ZAP (free proxy/scanner) to learn basic web security concepts.",
        "url": "https://github.com/Arashi20/OWASP_Juice_Shop_ZAP_Training",
        "button": "VIEW CODE",
        "icon": "fab fa-github",
        "external": True
    },
    {
        "title": "S&P 500 Prediction Model",
        "badges": ["Machine Learning", "LSTM", "LightGBM", "Market Analysis", "Python"],
        "desc": "This project aimed to explore historical S&P 500 data and build machine learning models (An LSTM model and a LightGBM model) to identify patterns related to bull markets, bear markets, and crashes, investigating potential predictability in market movements.",
        "url": "https://github.com/Arashi20/sp500_Prediction",
        "button": "VIEW CODE",
        "icon": "fab fa-github",
        "external": True
    },
    {
        "title": "Valence Prediction from Raw Speech",
        "badges": ["LSTM", "Speech Processing", "Python", "Deep Learning"],
        "desc": "A deep learning project focused on predicting valence (emotional positivity or negativity) from raw speech data using a bidirectional LSTM model. The project involves preprocessing audio data, feature extraction, model training, and evaluation.",
        "url": "https://github.com/Arashi20/ValencePredictor_DL",
        "button": "VIEW CODE",
        "icon": "fab fa-github",
        "external": True
    },
    {
        "title": "Robot Benchmark - BB8 Pit Escape",
        "badges": ["Python", "Robot Simulation", "Autonomous Systems"],
        "desc": "A Tilburg University project for the course 'Autonomous Systems', involving the improvement of an autonomous robot agent designed to escape from a pit obstacle in a simulated environment (BB8 robot). The focus is on robot navigation, obstacle avoidance, and autonomous decision-making using Python.",
        "url": "https://github.com/Arashi20/RobotBenchmark-BB8",
        "button": "VIEW CODE",
        "icon": "fab fa-github",
        "external": True
    },
    {
        "title": "Australian Biodiversity Analysis",
        "badges": ["Geopandas", "Deep Learning", "Data Visualization", "Python", "Keras"],
        "desc": "A Tilburg University project for the course 'AI For Nature & Environment'. Main goal: Construct a predictive neural network model designed to analyze random occurrences spanning diverse locations in Australia.",
        "url": "https://github.com/Arashi20/AustralianBiodiversity_DL",
        "button": "VIEW CODE",
        "icon": "fab fa-github",
        "external": True
    },
    {
        "title": "Heart Attack Classification Model",
        "badges": ["Machine Learning", "Data Analysis", "Python", "Scikit-Learn", "Logistic Regression"],
        "desc": "A small-scale project using various machine learning techniques. The project involves developing a classification model to predict the likelihood of heart attacks based on various health parameters.",
        "url": "https://github.com/Arashi20/Heart-Diseases-Classification",
        "button": "VIEW CODE",
        "icon": "fab fa-github",
        "external": True
    },
    {
        "title": "Personal Workout Data Pipeline",
        "badges": ["Data Analysis", "Python", "Pandas", "Data Engineering", "Data Science"],
        "desc": "This project implements a complete data science workflow using 2.5 years of personal workout data from StrengthLog. It demonstrates the full pipeline from raw data ingestion through feature engineering to predictive modeling, with emphasis on code quality, modularity, and testing.",
        "url": "https://github.com/Arashi20/Workout_Data_Pipeline",
        "button": "VIEW CODE",
        "icon": "fab fa-github",
        "external": True
    },
    {
        "title": "Stock Analyzer Tool",
        "badges": ["Python", "APIs", "DCF", "Stocks", "HTML/CSS/JS"],
        "desc": "A lightweight stock analysis tool built in Python (Flask) that helps me perform DCF analyses on stocks quickly. Moreover, I can add stocks to my wishlist with real up-to-date data fetched from APIs. Finally, I can add due diligence notes for each stock.",
        "url": "https://github.com/Arashi20/Stock_Portfolio_Dashboard_V2",
        "button": "VIEW CODE",
        "icon": "fab fa-github",
        "external": True

    },
    {
        "title": "Workout Logger App",
        "badges": ["Python", "Flask", "HTML/CSS/JS", "PostgreSQL"],
        "desc": "A simple workout logging web application built with Flask and PostgreSQL. It allows users to log their workouts, view PRs, log their weight, and track progress over time.",
        "url": "https://github.com/Arashi20/Workout_Logging_App",
        "button": "VIEW CODE",
        "icon": "fab fa-github",
        "external": True
    }
]


# Manifest Route
@app.route('/manifest.json')
def manifest():
    """
    Serves the PWA manifest.json file.
    """
    return send_from_directory('static', 'manifest.json', mimetype='application/manifest+json')


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
    Optionally filters projects by search query (?q=...).
    """
    query = request.args.get('q', '').strip().lower()

    # Filtering logic (similar to blog index)
    def matches(proj):
        text = proj['title'] + ' ' + ' '.join(proj['badges']) + ' ' + proj['desc']
        return query in text.lower()

    projects_to_show = [p for p in PROJECTS_LIST if matches(p)] if query else PROJECTS_LIST

    return render_template('projects.html', projects=projects_to_show, search_query=query)


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


# Utility function to extract keywords from markdown file
def extract_keywords_from_file(filepath):
    """Extract keywords from the first line of a markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            # Match: <!-- keywords: word1, word2, word3 -->
            match = re.match(r'<!--\s*keywords:\s*(.+?)\s*-->', first_line, re.IGNORECASE)
            if match:
                keywords_str = match.group(1)
                return [k.strip() for k in keywords_str.split(',')]
    except Exception:
        pass
    return []


# Blog Post Route
@app.route('/blog')
def blog():
    """
    Renders the Blog Index page.
    Expects files named like: YYYY-MM-DD_post_title.md
    Example: 2025-12-09_welcome.md
    """
    query = request.args.get('q', '').strip().lower()
    posts = []
    
    if os.path.exists(POSTS_DIR):
        files = os.listdir(POSTS_DIR)
        
        for file in files:
            if file.endswith('.md'):
                slug = file[:-3]  # Remove .md extension
                
                # Extract keywords from file content
                filepath = os.path.join(POSTS_DIR, file)
                keywords = extract_keywords_from_file(filepath)

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
                    'filename': file,         # Needed for sorting
                    'keywords': keywords      # Extracted keywords

                })
    
    # Sort by filename in REVERSE order (Newest dates first)
    posts.sort(key=lambda x: x['filename'], reverse=True)

    # Search/filter functionality
    if query:
        def matches(post):
            searchspace = f"{post['title']} {post['date']} {' '.join(post['keywords'])}"
            return query in searchspace.lower()
        filtered_posts = [p for p in posts if matches(p)]
    else:
        filtered_posts = posts

    return render_template('blog.html', posts=filtered_posts, search_query=query)
    

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