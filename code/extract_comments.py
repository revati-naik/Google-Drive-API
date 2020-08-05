from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors
import pandas as pd


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly',
          'https://www.googleapis.com/auth/drive'
]

# # The ID of a sample document.
# # DOCUMENT_ID = '195j9eDD3ccgjQRttHhJPymLJUCOUjs-jmwTrekvdjFE'
# # real document
# DOCUMENT_ID = '1T5QXpUIMv6f4JgWZYX1qeW8Tp5-TJLANTcoxWWzOQ_8'

# ...

def retrieve_comments(service, file_id):
  """Retrieve a list of comments.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to retrieve comments for.
  Returns:
    List of comments.
  """
  try:
    comments = service.comments().list(fileId=file_id).execute()
    return comments.get('items', [])
#   except errors.HttpError, error:
  except:
    print('An error occurred')
  return None

def main():
   
    # 1: Set up the service connection to the API
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # service = build('docs', 'v1', credentials=creds)
    service_comments = build('drive', 'v3', credentials=creds)

    # 2: Extract comments

    # read in list of interviews (with doc ids)
    interviews = pd.read_csv("KNEXT master data tracking - interviews.csv")

    # list of comments we've processed so far
    processed = pd.read_csv("KNEXT User Insights - Info needs clustering.csv")

    # truncate the super long comments so they can sort of show up when pasted into miro
    for index, row in processed.iterrows():
        l = len(row['Info needs clustering'])
        c = row['Info needs clustering']
        # hard coded length limit for truncating
        if l < 100:
            processed.at[index, 'trunc'] = c[:l]
        else:
            processed.at[index, 'trunc'] = c[:100]
    processed.to_csv("KNEXT User Insights - Info needs clustering-trunc.csv")

    # init list to hold extracted comments
    extractions = []

    # for each interview
    # idx = 1
    for index, row in interviews.iterrows():
        
        # skip the ones that we don't have links for yet
        if not isinstance(row['google doc auto-transcript'], float):

            # get the id
            DOCUMENT_ID = row['google doc auto-transcript'].split("/")[-1].split("=")[-1]

            # # connect to the document
            # document = service.documents().get(documentId=DOCUMENT_ID).execute()
            # # print('The title of the document is: {}'.format(document.get('title')))

            # extract and parse the comments
            comments = service_comments.comments().list(fileId=DOCUMENT_ID, fields="comments", pageSize=100).execute()
            if comments != None and len(comments['comments']) > 1:
                print("Extracting %i comments from %s" %(len(comments['comments']), row['interview']))      

                for comment in comments['comments']:
                    
                    # added this to leave out the partial comments that still exist
                    if comment.get('resolved') == False and comment.get('deleted') == False:
                    
                        compound = "%s: %s (%s)" %(comment['id'], comment['content'], row['interview_id'])

                        trunc = ""
                        if len(compound) < 100:
                            trunc = compound[:len(comment['content'])]
                        else:
                            trunc = compound[:100]
                        
                        is_processed = 0
                        if trunc in processed['trunc'].values:
                            is_processed = 1
                            
                        
                        clink = "https://docs.google.com/document/d/%s/edit?disco=%s" %(DOCUMENT_ID, comment['id'])
                        #print(comment['content'])
                        extractions.append({
                            'interview': row['interview'],
                            'interview_id': row['interview_id'],
                            'social_actor': row['social actor'],
                            'extraction': comment['content'],
                            'anchor': comment['quotedFileContent']['value'],
                            'doc_link': row['google doc auto-transcript'],
                            'comment_link': clink,
                            'compound': compound,
                            'comment_id': comment['id'],
                            'is_processed': is_processed,
                            'trunc': trunc
                        })
                        # idx += 1
            else:
                print("No comments yet for", row['interview'])
        else:
            print("No transcript yet for", row['interview'])

    # tie up into dataframe
    extractions = pd.DataFrame(extractions)

    # convenience columns for noting down tag occurrences
    for index, row in extractions.iterrows():
        for tag in ['info', 'source', 'texture']:
            v = 0
            if "#%s" %tag in row['extraction']:
                v = 1
            extractions.at[index, tag] = v

    # export and done!
    extractions.to_excel("KNEXT-extractions-2019-6-18-b.xlsx")
    print("Finished!")

    


if __name__ == '__main__':
    main()