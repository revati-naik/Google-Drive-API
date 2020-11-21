
from __future__ import print_function
import httplib2
import os, io
import files_get
import get_file_id
import permissions
import revisions
import comments

import auth
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload


import sys

sys.dont_write_bytecode = True

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
# import auth
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'CareersInPlay'
authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = authInst.getCredentials()
http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v2', http=http)



############### UPLAOD-A-FILE ##################
# file_id = files_get.uploadFile(service=drive_service,filename='sample_text.txt', filepath='sample_text.txt', mimetype_target='application/vnd.google-apps.document', mimetype_current='text/plain')
# updated_file_id = uploadFile('people.ipynb','people.ipynb','application/x-ipynb+json')


################ DOWNLOAD-A-FILE ##################
#files_get.downloadFile(file_id,'./Downloads/Test_Assignment_submitted.ipynb')


################ UPLOAD_A_FILE ##################
# file_id = files_get.uploadFile(filename='Test_Assignment.ipynb', filepath='Test_Assignment.ipynb', mimetype='application/x-ipynb+json')

################ CREATING-A-FOLDER ##################
# files_get.createFolder('Google')
# folder_id = files_get.createFolder(service=drive_service, name='INST126')
# print(folder_id)

################ PRINT_FILE_METADATA ##################
# file_id = '1qjy-Ys6r23J-DggcKaLM6q1ur_11Md-ZAuYlvD7FGnE'
file_id = '1mqjMez91mi-2Gee08b_6z3tGBVUhM0g6j4frh0VtAO0'
# file_id = '1wqU9his6uDfsxLO3LSm0evNtjbcLeG7ZUEQ6Q4yS1MM'
# files_get.print_file_metadata(service=drive_service, file_id=folder_id)
# files_get.print_file_metadata(service=drive_service, file_id=file_id)

############### PRINT_FILE_CONTENT ##################
# files_get.print_file_content(service=drive_service, file_id=file_id)

################ FILE_RENAME ##################
# updated_file = files_get.rename_file(service=drive_service, file_id=file_id, new_title="Revati")
# print(updated_file)

################ SEARCH-A-FILE ##################
# files_get.searchFile(10,"name contains 'Revati'")


################ PRINT-FILE-ABOUT ##################
# files_get.print_about(service=drive_service)


################ RETRIEVE-FILE-REVISIONS ##################
# revision_id, revisions_details = revisions.retrieve_revisions(service=drive_service, file_id=file_id)
# revisions.retrieve_revisions(service=drive_service, file_id=file_id)
# print(revisions_details)
# # 

################ PRINT-FILE-REVISIONS ##################

# print_revisions = revisions.print_revision(service=drive_service, file_id=file_id, revision_id=revision_id)
# print(print_revisions)

################ RETRIEVE-FILE-COMMENTS ##################
dict_to_print = comments.retrieve_comments(service=drive_service, file_id=file_id)
print(dict_to_print)
comments.viz_graph(dict_to_print)
# print(type(comment_details))
# file1 = open("comments.txt","w")
# file1.write(comment_details)
# file1.close 

################ GET-FILE-ID ##################
# get_file_id.get_file_id(drive_service=drive_service)

################ CREATE-FILE-PERMISSIONS ##################

# permissions.create_permissions(service=drive_service, file_id=file_id)

################ INSERT-FILE-PERMISSIONS ##################

# permissions.insert_permission(service=drive_service, file_id=file_id, value="revatin@umd.edu", perm_type="user", role="writer")

################ RETRIEVE-FILE-PERMISSIONS ##################
# permission_id = files_get.retrieve_permissions(service=drive_service, file_id='1z09xiXdBtAXpfEwor01TdezfOg6Dxiwp')
# print(permission_id)

################ PERMISSION-ID-FOR-EMAIL ##################

# permissions.print_permission_id_for_email(service=drive_service, email="kushalm@terpmail.umd.edu")

################ UPDATE-FILE-PERMISSIONS ##################
# files_get.update_permission(service=drive_service, file_id='1z09xiXdBtAXpfEwor01TdezfOg6Dxiwp', permission_id=permission_id, new_role='writer')


