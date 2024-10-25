import os
import sys

def create_directory_structure():
    root_dir = "social_media_optimizer"
    subdirs = ["utils", "logs"]
    
    # Create root directory
    os.makedirs(root_dir, exist_ok=True)
    
    # Create subdirectories
    for subdir in subdirs:
        os.makedirs(os.path.join(root_dir, subdir), exist_ok=True)
    
    print(f"Created directory structure in {root_dir}")

def create_file(filepath, content):
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Created file: {filepath}")

def main():
    create_directory_structure()
    
    root_dir = "social_media_optimizer"
    
    # Create main.py
    main_content = '''
import schedule
import time
import logging
from utils.content_calendar import ContentCalendar
from utils.social_media_api import post_content, update_engagement_metrics
from utils.nlp_utils import generate_content_suggestions, apply_insights_to_future_content
from utils.ml_utils import create_ab_tests, analyze_ab_test_results, incorporate_ab_test_results

logging.basicConfig(filename='logs/content_optimization.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

content_calendar = ContentCalendar()

def run_content_optimization():
    logging.info("Running content optimization process...")
    suggestions = generate_content_suggestions(content_calendar)
    if suggestions:
        create_ab_tests(content_calendar, suggestions)
        apply_insights_to_future_content(content_calendar, suggestions)
    winning_post = analyze_ab_test_results(content_calendar)
    incorporate_ab_test_results(content_calendar, winning_post)
    logging.info("Content optimization process completed.")

def schedule_posts():
    for index, row in content_calendar.df.iterrows():
        if pd.isnull(row['post_id']):
            schedule.every().day.at(row['time_slot']).do(post_content, content_calendar, row).tag(f"{row['platform']}-{row['due_date']}-{row['time_slot']}")

def run_scheduler():
    schedule_posts()
    schedule.every(15).minutes.do(update_engagement_metrics, content_calendar)
    schedule.every().day.at("00:00").do(run_content_optimization)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    logging.info("Starting social media scheduler and content optimization system with A/B testing...")
    run_scheduler()
'''
    create_file(os.path.join(root_dir, "main.py"), main_content)
    
    # Create gui.py
    gui_content = '''
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, 
                             QLabel, QHBoxLayout, QComboBox, QMessageBox, QTabWidget, QTableWidget, 
                             QTableWidgetItem, QLineEdit, QFormLayout, QDateEdit, QTimeEdit, QDialog)
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QDate, QTime
import logging
from main import run_scheduler, run_content_optimization
from utils.content_calendar import ContentCalendar
from utils.nlp_utils import generate_ab_variant, analyze_content
from utils.ml_utils import get_feature_importance
import pandas as pd
import json
from config import *

# ... (rest of the GUI code as provided in the previous response)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
'''
    create_file(os.path.join(root_dir, "gui.py"), gui_content)
    
    # Create config.py
    config_content = '''
import os

# API credentials
TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY', '')
TWITTER_API_SECRET = os.environ.get('TWITTER_API_SECRET', '')
TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN', '')
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET', '')

LINKEDIN_API_KEY = os.environ.get('LINKEDIN_API_KEY', '')
LINKEDIN_API_SECRET = os.environ.get('LINKEDIN_API_SECRET', '')
LINKEDIN_ACCESS_TOKEN = os.environ.get('LINKEDIN_ACCESS_TOKEN', '')

FACEBOOK_ACCESS_TOKEN = os.environ.get('FACEBOOK_ACCESS_TOKEN', '')

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')

# Other configuration settings
SAMPLE_SIZE_AB_TEST = float(os.environ.get('SAMPLE_SIZE_AB_TEST', '0.2'))
SIGNIFICANCE_LEVEL = float(os.environ.get('SIGNIFICANCE_LEVEL', '0.05'))
'''
    create_file(os.path.join(root_dir, "config.py"), config_content)
    
    # Create requirements.txt
    requirements_content = '''
pandas==1.3.3
numpy==1.21.2
tweepy==4.4.0
python-linkedin==4.1
facebook-sdk==3.1.0
schedule==1.1.0
scikit-learn==0.24.2
transformers==4.11.3
spacy==3.1.3
textstat==0.7.2
gensim==4.1.2
pyLDAvis==3.3.1
openai==0.27.0
scipy==1.7.1
PyQt5==5.15.4
pyinstaller==4.5.1
'''
    create_file(os.path.join(root_dir, "requirements.txt"), requirements_content)
    
    # Create run.py
    run_content = '''
import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
'''
    create_file(os.path.join(root_dir, "run.py"), run_content)
    
    # Create utils/__init__.py
    create_file(os.path.join(root_dir, "utils", "__init__.py"), "")
    
    # Create utils/content_calendar.py, utils/social_media_api.py, utils/nlp_utils.py, utils/ml_utils.py
    # (You'll need to fill these with the appropriate content)
    for util_file in ["content_calendar.py", "social_media_api.py", "nlp_utils.py", "ml_utils.py"]:
        create_file(os.path.join(root_dir, "utils", util_file), f"# TODO: Implement {util_file}")
    
    # Create an empty log file
    open(os.path.join(root_dir, "logs", "content_optimization.log"), 'a').close()
    
    print("Project structure and files created successfully!")

if __name__ == "__main__":
    main()