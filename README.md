# 🚀 Python Project Setup Guide

Welcome to **Sentimental Analysis App**! Follow these steps to set up and run the project on your local machine.

---

## 🛠️ Prerequisites

Before running the project, ensure you have the following installed:

- **Python** (≥ 3.12) → [Download Here](https://www.python.org/downloads/)
- **pip** (Python package manager) → Installed with Python
- **virtualenv** (for creating virtual environments)

To check if Python and pip are installed, run:

```sh
python --version
pip --version
```

# Setup Instructions
## Clone the repository
```sh
git clone https://github.com/joboy-dev/social-media-sentimental-analysis-app.git
cd social-media-sentimental-analysis-app
```

## Set up virtual environment
### Windows
```sh
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux
```sh
python3 -m venv venv
source venv/bin/activate
```

💡 Note: If venv is missing, install it with:
```sh
pip install virtualenv
```

## Install dependencies
```sh
pip install -r requirements.txt
```

## Run app
```sh
streamlit run main.py
```
