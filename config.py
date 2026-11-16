from dotenv import load_dotenv
import os


load_dotenv()

db_config = {
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'host': os.getenv('HOST'),
    'port': os.getenv('PORT')
             }

COUNTRIES = ['Iceland', 'Norway', 'Switzerland', 'Denmark']