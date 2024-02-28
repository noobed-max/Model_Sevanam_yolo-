import requests
import base64

import os
# Make the POST request to your FastAPI server

def encode_and_store_files(directory_path):
    encoded_content = []
    API_URL = "http://127.0.0.1:8000/upload/"
    #change the API_URL 
    try:
        
        # Iterate over each file in the specified directory
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)

            if os.path.isfile(file_path):
                # Read the content of the file
                with open(file_path, 'rb') as file:
                    file_content = file.read()

                # Encode the file content to base64
                encoded_file_content = base64.b64encode(file_content)

                # Append the encoded content to the list
                encoded_content.append(encoded_file_content)
        datae = {"encoded_content": encoded_content}
        # Pass the list of encoded content to the next file
        response = requests.post(API_URL, data=datae)
        print(response.text)
    
    except Exception as e:
        print(f"Error: {e}")

#MODIFY THE BELOW PARAMETERS TO TEST UPLOAD FUCNTION 
if __name__ == "__main__":
    directory_path = '/home/deadsec/YOLO/yolo/newdir'
    #change path also 
    encode_and_store_files(directory_path)
