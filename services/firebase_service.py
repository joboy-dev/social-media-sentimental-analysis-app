import os, pyrebase
from secrets import token_hex
import streamlit as st

from utils.firebase_config import firebase_config


class FirebaseService:
    
    @classmethod
    def upload_file(
        cls, 
        file,
        # allowed_extensions: list | None, 
        upload_folder: str, 
        model_id: str
    ):
        '''Function to upload a file'''
            
        os.makedirs(st.secrets.dir.temp_dir, exist_ok=True)
        
        # Generate a new file name
        new_filename = f'{token_hex(16)}.jpg'
        
        # Save file temporarily
        save_path = os.path.join(st.secrets.dir.temp_dir, new_filename)
        
        with open(save_path, 'wb') as f:
            content = file.getbuffer()
            f.write(content)
        
        # Initailize firebase
        firebase = pyrebase.initialize_app(firebase_config)
        
        # Set up storage and a storage path for each file
        storage = firebase.storage()
        firebase_storage_path = f'sentiment-analysis-app/{upload_folder}/{model_id}/{new_filename}'
        
        # Store the file in the firebase storage path
        storage.child(firebase_storage_path).put(save_path)
        
        # Get download URL
        download_url = storage.child(firebase_storage_path).get_url(None)
        
        # Delete the temporary file
        os.remove(save_path)
        
        return download_url
        
        # return {
        #     'file_name': new_filename,
        #     'download_url': download_url
        # } 
        