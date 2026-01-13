import urllib.request
import os

"""
Reads and returns the text from a url.

The text is loaded from a local cache; one downloads the text from the url 
only if the cache does not exist yet.

We are setting default parameters for the cache's directory and file name. 
Note that the cache's path is different when calling the function from the notebook.
"""
def read_text(url, save_dir=os.path.join('text_processing', 'data'), 
              file_name='pride_and_prejudice.txt'):
    cache = os.path.join(save_dir, file_name)
    
    # check if cache exists locally
    if os.path.exists(cache):
        # read the text from a local cache file
        with open(cache, encoding='utf-8') as f:
            text = f.read()
    else:
        # download the text from the url
        with urllib.request.urlopen(url) as f:
            text = f.read().decode('utf8')

        # save the text to a local file
        os.makedirs(save_dir)   
        with open(cache, mode='w', encoding='utf-8') as f:
            f.write(text)

    return text
