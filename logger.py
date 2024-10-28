import logging
from datetime import datetime
import os
# Create a directory for logs if it doesn't exist
log_directory = "./log"
os.makedirs(log_directory, exist_ok=True)

# Generate a unique log filename with a timestamp
log_filename = f"{log_directory}/data_insertion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

# Example logger functions
def log_start_process(process_name):
    logging.info(f"Starting {process_name} process.")


def log_end_process(process_name):
    logging.info(f"Finished {process_name} process.")

def log_connection():
    logging.info("successfully connected to the database.")

def log_selction_data(length):
    logging.info(f"successfully selected the {length} data from the database.")

def log_disconnection():
    logging.info("successfully disconnected from the database.")

def log_insert_github(owner, repo, endpoint):
    logging.info(f"Successfully inserted \'{endpoint}\' data - owner : {owner} | repo : {repo}.")

def log_insert_twitter(near_address,twitter_link):
    logging.info(f"Successfully inserted twitter link - near : {near_address} | twitter {twitter_link}.")

def log_insert_project(near_address):
    logging.info(f"Successfully inserted project data - near_address : {near_address}")

def log_error(record_id, error):
    logging.error(f"Failed to insert record with ID: {record_id}. Error: {error}")

