from urllib.parse import urlparse
import os

def getStartingPage(url):
    """
        Get the url page where image download stopped if any

        @param URL string url of base download site
        @return string starting or continuation link
    """

    parsedUrl = urlparse(url)
    link = ""
    if os.path.exists('data/stopurls/' + url.netloc):
        with open('data/stopurls/' + url.netloc, 'r') as urlFile:
            link = urlFile.read()
            if link == '':
                link = url
    else:
        link = url

    return link

