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
    # print(revisions)

    # return revisions.get('items', [])
    return revisions
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