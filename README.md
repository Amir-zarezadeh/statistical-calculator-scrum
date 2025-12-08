# 📊 Statistical Calculator

Calculator (Geo statistics, Hypothesis Tests, …)
A full-stack web application for performing statistical Geo statistics calculations and hypothesis testing. Built with Python Flask backend and HTML/CSS/JavaScript frontend.


## 📥 Installation from GitHub

### Step 1: Clone the Repository
```bash
# Clone the project
git clone https://github.com/dayald434/Statistical_Calculator.git

# Navigate into the project folder
cd stat-calculator
```

### Step 2: Set Up Python Virtual Environment

#### Windows:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your terminal
```

#### macOS/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your terminal
```

### Step 3: Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
# Check Flask installation
python -c "import flask; print('Flask version:', flask.__version__)"

# Should output: Flask version: 3.0.x
```

---

## 🎯 Running the Application

### Start the Server
```bash
# Make sure virtual environment is activated (you should see (venv))
python app.py
```

You should see:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### Access the Application

Open your web browser and go to:
```
http://localhost:5000
```

### Stop the Server

Press `Ctrl + C` in the terminal where the server is running.

---

## 📁 Project Structure
```
stat-calculator/
├── app.py                      # Flask application & API endpoints
├── requirements.txt            # Python dependencies
├── Procfile                    # Deployment configuration
├── DS_Project.HTML             # COVID-19 presentation slides
├── README.md                   # Project documentation
├── templates/
│   └── index.html              # Main HTML page
├── static/
│   ├── style.css               # CSS styling
│   └── script.js               # JavaScript functionality
├── tests/
│   ├── __init__.py             # Tests package initialization
│   ├── test_app.py             # Unit tests (47 test cases)
│   └── README.md               # Testing documentation
├── .github/
│   ├── workflows/
│   │   ├── ci.yml              # CI pipeline (test, lint, security)
│   │   ├── deploy.yml          # Deployment pipeline
│   │   └── code-coverage.yml   # Coverage reporting
│   └── PIPELINE_GUIDE.md       # GitHub Actions guide
└── __pycache__/                # Python bytecode cache
