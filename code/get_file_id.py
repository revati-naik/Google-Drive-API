
import sys

sys.dont_write_bytecode = True


def get_file_id(drive_service):

  page_token = None
  while True:
      response = drive_service.files().list(q="mimeType='application/x-ipynb+json'",
                                            spaces='drive',
                                            fields='nextPageToken, items(id, title)',
                                            pageToken=page_token).execute()
      for file in response.get('items', []):
          # Process change
          print ('Found file: %s (%s)' % (file.get('title'), file.get('id')))
      page_token = response.get('nextPageToken', None)
      if page_token is None:
          break