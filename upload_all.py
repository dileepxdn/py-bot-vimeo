from __future__ import print_function
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import socket
import os


socket.setdefaulttimeout(600)  # set timeout to 10 minutes
SCOPES = ['https://www.googleapis.com/auth/drive']

# # # DEFAULT DIR >> BOT 1
# my_folder_id = '16m8_vJaE--4LludRLZNSVVP86j1XrAkT'

###BOT 2 DIR
# my_folder_id ='1Sd-JId7NYoBBz0nBk59vU_GCrITWFdgK'


### BOT 3 DIR
my_folder_id = '1suwKK83mqkEaQ29Fuy3GE7AKwndz8TTz'

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# conver sting paths..
BASE_DIR = '/'.join(BASE_DIR.split('\\'))
TEMP_DIR = '/'.join(TEMP_DIR.split('\\'))
OUTPUT_DIR = '/'.join(OUTPUT_DIR.split('\\'))

creds = None


print("\n\n\n\nExecuting Drive UPLOAD.py")
print("Getting tokne.pickle")

print(f"BASE DIR :: {BASE_DIR}")
print(f"TEMP_DIR :: {TEMP_DIR}")
print(f"OUTPUT_DIR :: {OUTPUT_DIR}\n\n")



if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
       creds = pickle.load(token)
else:
    print("NO TOKEN >>> :(")

service = build('drive', 'v3', credentials=creds)


def upload_video_old(file_name):
    # file_name = file_name+'.mp4'
    print(f"Uploading {file_name} to my_folder.. :: {my_folder_id}")
    file_metadata = {
    'name': file_name,
    'parents': [my_folder_id]
    }
    file_path = os.path.join(OUTPUT_DIR, file_name)
    file_path = '/'.join(file_path.split('\\'))
    print(f"File path : {file_path}")
    media = MediaFileUpload(file_path, mimetype='video/mp4',)
    file_res = service.files().create(body=file_metadata, media_body=media,).execute() # pylint: disable=maybe-no-member
    print('File ID: %s' % file_res.get('id'))
    print(f"File upload done : {file_name} :: \n {file_res}")
    print(f"deleting file : {file_path}")
    media =None # to close connection with file
    os.remove(file_path)

# upload_video_to_this_folder(my_folder_id, 'bramu')


def upload_video(file_name):
    # file_name = file_name+'.mp4'
    print(f"Uploading {file_name} to my_folder.. :: {my_folder_id}")
    
    file_metadata = {
    'name': file_name,
    'parents': [my_folder_id]
    }

    file_path = os.path.join(OUTPUT_DIR, file_name)
    file_path = '/'.join(file_path.split('\\'))

    print(f"File path : {file_path}")

    media = MediaFileUpload(file_path, mimetype='video/mp4', resumable=True)
    request = service.files().create(body=file_metadata, media_body=media,) # pylint: disable=maybe-no-member
    response = None

    # print('File ID: %s' % response.get('id'))
    # print(f"File upload done : {file_name} :: \n {file_res}")
    # print(f"deleting file : {file_path}")

    while response is None:
        status, response = request.next_chunk()
        # print(status)
        # print(response)

        if status is None:
            # print("Status is none\n")
            value = 1
            # print(value)
        else:
            # print("Status is not none")
            value = status.progress()
            # print(value)
            percent = str(int(value * 100))
            print("Uploaded : "+percent +'%')

    print("Upload Completed::")
    print(response)
    media =None # to close connection with file
    print("DELETING THIS FILE...")
    os.remove(file_path)
    return [True, 'Successfully Uploaded to Gdrive.. :)']




def upload_allfiles():
    if os.path.exists(OUTPUT_DIR) and os.path.isdir(OUTPUT_DIR):
        total_files = str(len(os.listdir(OUTPUT_DIR)))
        print(f"\n\nTotal files {total_files}")

        for index, filename in enumerate(os.listdir(OUTPUT_DIR)):
            num = index+1
            print("\n\nUploadingFile :: "+filename)
            print(str(num)+'/'+total_files+'\n Uploading File..\n'+filename)
            upload_video(filename)
        return "All files uploads complete"
    else:
        print("No OUTPUT Directory Exist")
        return "No Directory Exist"

upload_allfiles()

# httplib2==0.15.0 << Down graded.