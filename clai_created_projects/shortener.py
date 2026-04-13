import json
import os
import random
import string
import re

DATA_FILE = 'urls.json'

def set_data_file(filename):
    global DATA_FILE
    DATA_FILE = filename

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def generate_short_key(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def is_valid_url(url):
    # Simple regex for URL validation
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def shorten_url(original_url):
    if not is_valid_url(original_url):
        raise ValueError("Invalid URL")
    
    data = load_data()
    
    # Check if URL already shortened
    for key, url in data.items():
        if url == original_url:
            return key
            
    short_key = generate_short_key()
    while short_key in data:
        short_key = generate_short_key()
        
    data[short_key] = original_url
    save_data(data)
    return short_key

def resolve_url(short_key):
    data = load_data()
    return data.get(short_key)
