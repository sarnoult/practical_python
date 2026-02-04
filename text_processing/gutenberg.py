import urllib.request
import os
import re
import json
from more_itertools import split_at

chapter_pattern = re.compile(r'Chapter [IXVL]+', flags=re.I)


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


def novel_lines(text):
    lines = text.splitlines()
    i_start = [i for i, line in enumerate(lines) if "*** START" in line][0]
    i_end = [i for i, line in enumerate(lines) if "*** END" in line][0]
    return lines[i_start + 1:i_end]


def is_chapter_header(line):
    return re.match(chapter_pattern, line) is not None


def split_novel_by_chapter(text):
    lines = novel_lines(text)
    chapter_lines = list(split_at(lines, is_chapter_header))
    chapters = [' '.join(group) for group in chapter_lines]
    headers = [line for line in lines if is_chapter_header(line)]
    return zip(headers, chapters)

def to_json(text, output_path=os.path.join('text_processing', 'data', 'chapters.json')):
    chapters = split_novel_by_chapter(text)
    chapter_dict = {header: chapter for header, chapter in chapters}
    with open(output_path, 'w') as f:
        json.dump(chapter_dict, f, indent=2, ensure_ascii=False)

        
if __name__ == '__main__':
    url = "https://www.gutenberg.org/ebooks/1342.txt.utf-8"
    text = read_text(url)
    to_json(text)