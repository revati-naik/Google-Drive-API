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

def retrieve_revisions(service, file_id):
  """Retrieve a list of revisions.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to retrieve revisions for.
  Returns:
    List of revisions.
  """
  try:
    revisions = service.revisions().list(fileId=file_id).execute()
    # revisions_download = service.revisions().get(revisionId=revision_id).execute()
    revisions_details = revisions.get('items', [])
    # print(revisions_details)
    print((revisions_details[0].keys()))


    for i in range(1, len(revisions_details)):
      # print(revisions_details[i])
      revision_id = revisions_details[i]['id']
      print("Revision ID: ", revision_id)
        
      display_name = revisions_details[i]['lastModifyingUser']['displayName']
      print("Display Name: ", display_name)

      email_address = revisions_details[i]['lastModifyingUser']['emailAddress']
      print("Email Address: ", email_address)

      permission_id = revisions_details[i]['lastModifyingUser']['permissionId']
      print("Permission ID: ", permission_id)

      modified_time = revisions_details[i]['modifiedDate']
      print("Modified Date: ", modified_time)

      revision = service.revisions().get(
        fileId=file_id, revisionId=revision_id).execute()
      # print(revision)
      break

      print("---------------------------------------")

    # return revision_id, revisions_details
  except errors.HttpError, error:
    print ("An error occurred: ", error)
  return None


def print_revision(service, file_id, revision_id):
  """Print information about the specified revision.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to print revision for.
    revision_id: ID of the revision to print.
  """
  try:
    revision = service.revisions().get(
        fileId=file_id, revisionId=revision_id).execute()

    # print ('Revision ID: ', revision['id'])
    # print ('Modified Date: ',  revision['modifiedDate'])
    if revision.get('pinned'):
      print ('This revision is pinned')
    return revision
  except errors.HttpError, error:
    print ("An error occurred: ", error)