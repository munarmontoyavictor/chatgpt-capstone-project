import os
from dotenv import find_dotenv, load_dotenv
from flask import Flask
from flask_cors import CORS
from transcribe_view import transcribe_controller_blueprint
import logging

# Configurar el nivel de registro para la biblioteca pymongo
logging.getLogger('pymongo').setLevel(logging.CRITICAL)
app = Flask(__name__)
CORS(app)
app.register_blueprint(transcribe_controller_blueprint)

# def create_database():
#     load_dotenv()
#     client = MongoClient(os.getenv("MONGO_DB_URI"))
#     database_name = os.getenv('DB_NAME')
#     logging.info(f"Database '{database_name}'---------------------------------------------")
#     # Check if the database already exists
#     if database_name not in client.list_database_names():
#         try:
#             # Create the database
#             client[database_name].command("ping")
#             logging.info(f"Database '{database_name}' created successfully.")
#         except Exception as e:
#             logging.error(f"Error creating database '{database_name}': {e}")
#     else:
#         logging.info(f"Database '{database_name}' already exists.")

if __name__ == '__main__':
    load_dotenv(find_dotenv())
    port = int(os.getenv("PORT"))
    debug = os.getenv("APP_DEBUGGING")
    app.run(debug=debug, host="0.0.0.0", port=port)
