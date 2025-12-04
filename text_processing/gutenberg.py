import urllib.request

def read_text(url):
    with urllib.request.urlopen(url) as f:
        text = f.read().decode('utf8')
    return text
