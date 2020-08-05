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



def retrieve_permissions(service, file_id):
  """Retrieve a list of permissions.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to retrieve permissions for.
  Returns:
    List of permissions.
  """
  try:
    permissions = service.permissions().list(fileId=file_id).execute()
    # print(permissions)
    permissions_details = permissions['permissions']
    for i in range(0, len(permissions_details)):
	    user_role = permissions_details[i]['role']
	    user_type = permissions_details[i]['type']
	    permission_id = permissions_details[i]['id']

	    print("user_role: ", user_role)
	    print("user_type: ", user_type)
	    print("permission_id: ", permission_id)

    # return permissions.get('items', [])
    return permission_id
  except errors.HttpError, error:
    print ("An error occurred: ", error)
  return None


def update_permission(service, file_id, permission_id, new_role):
  """Update a permission's role.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to update permission for.
    permission_id: ID of the permission to update.
    new_role: The value 'owner', 'writer' or 'reader'.

  Returns:
    The updated permission if successful, None otherwise.
  """
  try:
    # First retrieve the permission from the API.
    permission = service.permissions().get(
        fileId=file_id, permissionId=permission_id).execute()
    permission['role'] = new_role
    return service.permissions().update(
        fileId=file_id, permissionId=permission_id, body=permission).execute()
  except errors.HttpError, error:
    print ("An error occurred: ", error)
  return None

def create_permissions(service, file_id):
  try:
    # permission = service.permissions().get(fileId=file_id).execute()
    body = {"role": "writer","type": "user","emailAddress": "revati.naik1501@gmail.com"}
    return service.permissions().insert(fileId=file_id, body=body).execute()
  except errors.HttpError, error:
    print ("An error occurred: ", error)
  return None

def insert_permission(service, file_id, value, perm_type, role):
  """Insert a new permission.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to insert permission for.
    value: User or group e-mail address, domain name or None for 'default'
           type.
    perm_type: The value 'user', 'group', 'domain' or 'default'.
    role: The value 'owner', 'writer' or 'reader'.
  Returns:
    The inserted permission if successful, None otherwise.
  """
  new_permission = {
      'value': value,
      'type': perm_type,
      'role': role
  }
  try:
    return service.permissions().insert(
        fileId=file_id, body=new_permission).execute()
  except errors.HttpError, error:
    print ("An error occurred: ", error)
  return None


def print_permission_id_for_email(service, email):
  """Prints the Permission ID for an email address.

  Args:
    service: Drive API service instance.
    email: Email address to retrieve ID for.
  """
  try:
    id_resp = service.permissions().getIdForEmail(email=email).execute()
    # print id_resp['id']
    print (id_resp)
  except errors.HttpError, error:
    print ("An error occurred: ", error)