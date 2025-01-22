import base64

def parse(text):
    return base64.urlsafe_b64decode(text.encode('ASCII')).decode('utf-8')
