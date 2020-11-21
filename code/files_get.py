from __future__ import print_function
from apiclient import errors
from apiclient import http
import httplib2
import os, io
import files_get
import get_file_id

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload


import sys

sys.dont_write_bytecode = True
# ...

def uploadFile(service, filename, filepath, mimetype_target, mimetype_current):
    file_metadata = {'title': filename,
                    'mimeType': mimetype_target}
    media = MediaFileUpload(filepath,
                            mimetype=mimetype_current,
                            resumable=True)
    file = service.files().insert(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    file_id = file.get('id')
    # print('File ID: %s' % file.get('id'))
    print('File ID: ', file_id)
    return file_id

def downloadFile(service,file_id,filepath):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download ", int(status.progress() * 100))
    with io.open(filepath,'wb') as f:
        fh.seek(0)
        f.write(fh.read())

def createFolder(service,name):
    file_metadata = {
    'name': name,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body=file_metadata,
                                        fields='id').execute()
    print ('Folder ID: ', file.get('id'))
    return (file.get('id'))

def searchFile(service,size,query):
    results = service.files().list(
    pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            # print(item)
            print('{0} ({1})'.format(item['name'], item['id']))


def print_file_metadata(service, file_id):
  """Print a file's metadata.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to print metadata for.
  """
  try:
    file = service.files().get(fileId=file_id).execute()
    # print(file.keys())
    print("Title: ", file['title'])
    print("MIME type: ", file['mimeType'])
    print("Last Modifying User: ", file['lastModifyingUserName'])
    print("Last Modifying User Email: ", file['lastModifyingUser']['emailAddress'])
    print("Last Modified Time (UTC): ", file['modifiedDate'])
    print("User Role: ", file['userPermission']['role'])
    print("User Permission ID: ", file['lastModifyingUser']['permissionId'])
    # print("File Name: ", file['name'])
  except errors.HttpError, error:
    print ("An error occurred: ", error)


def listFiles(size):
    results = service.files().list(
        pageSize=size,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))


def print_file_content(service, file_id):
  """Print a file's content.

  Args:
    service: Drive API service instance.
    file_id: ID of the file.

  Returns:
    File's content if successful, None otherwise.
  """
  try:
    print(service.files().get_media(fileId=file_id).execute())
    # print service.files().get_media(fileId=file_id).execute()
  except errors.HttpError, error:
    print ("An error occurred: ", error)


def download_file(service, file_id, local_fd):
  """Download a Drive file's content to the local filesystem.

  Args:
    service: Drive API Service instance.
    file_id: ID of the Drive file that will downloaded.
    local_fd: io.Base or file object, the stream that the Drive file's
        contents will be written to.
  """
  request = service.files().get_media(fileId=file_id)
  media_request = http.MediaIoBaseDownload(local_fd, request)

  while True:
    try:
      download_progress, done = media_request.next_chunk()
    except errors.HttpError, error:
      print ("An error occurred: ", error)
      return
    if download_progress:
      print ("Download Progress: ",int(download_progress.progress() * 100))
    if done:
      print ("Download Complete")
      return

def rename_file(service, file_id, new_title):
  """Rename a file.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to rename.
    new_title: New title for the file.
  Returns:
    Updated file metadata if successful, None otherwise.
  """
  try:
    file = {'title': new_title}

    # Rename the file.
    updated_file = service.files().update(
        fileId=file_id, fields='title').execute()

    # updated_file = service.files().update(
        # fileId=file_id,
        # body=file,
        # fields='title').execute()

    return updated_file
  except errors.HttpError, error:
    print ("An error occurred: ", error)
    return None

def print_about(service):
  """Print information about the user along with the Drive API settings.

  Args:
    service: Drive API service instance.
  """
  try:
    about = service.about().get().execute()

    print ("Current user name: ", about['name'])
    print ("Root folder ID: ", about['rootFolderId'])
    print ("Total quota (bytes): ", about['quotaBytesTotal'])
    print ("Used quota (bytes): ", about['quotaBytesUsed'])
  except errors.HttpError, error:
    print ("An error occurred: ", error)



