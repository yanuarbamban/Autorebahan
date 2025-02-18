from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

class BloggerManager:
    def __init__(self, credential_file='data/credentials.json'):
        store = file.Storage('data/token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(credential_file, 'https://www.googleapis.com/auth/blogger')
            creds = tools.run_flow(flow, store)
        self.service = build('blogger', 'v3', http=creds.authorize(Http()))
    
    def create_post(self, blog_id, title, content):
        body = {
            "kind": "blogger#post",
            "blog": {"id": blog_id},
            "title": title,
            "content": content
        }
        return self.service.posts().insert(blogId=blog_id, body=body).execute()