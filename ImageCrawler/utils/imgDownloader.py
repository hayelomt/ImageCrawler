import os
import urllib
import urllib.request
from urllib.parse import urlparse
from time import gmtime, strftime, sleep


class ImageDownloader:

    def __init__(self):
        self.chrome_user_agent = """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"""
        self.headers = {'User-Agent': self.chrome_user_agent}
        os.makedirs('imgs', exist_ok=True)
        self.dir_name = 'imgs'
        self.log_file = open('data/logFile.log', 'at')
        self.log_file.write(strftime("%a, %d %b %Y %H:%M:%S->", gmtime()) + ' Opened\n')

    def download(self, img_link, print_progress=True):
        parsed_url = urlparse(img_link)

        # Recurssively create parent folder to store image
        parent_folder = self.dir_name + '/' + parsed_url.netloc
        # for dir_name in parsed_url.path.split('/'):
        #     if dir_name != '':
        #         parent_folder = parent_folder + '/' + dir_name

        os.makedirs(parent_folder, exist_ok=True)

        # Split url path and join with - to form file name
        file_name = '-'.join(parsed_url.path.split('/'))
        
        # Append parent folder to file folder
        file_path = parent_folder + '/' + file_name

        if print_progress:
            print('Downloading image:', img_link)
        self.log_file.write(strftime("%a, %d %b %Y %H:%M:%S-> ", gmtime()) + 'Downloading image:' + img_link + '\n')

        # If file is Downloaded skip redownload
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            if print_progress:
                print('Already downloaded:', img_link)
            self.log_file.write(strftime("%a, %d %b %Y %H:%M:%S-> ", gmtime()) + 'Already downloaded:' +
                                img_link + '\n')
        else:
            try:
                with open(file_path, 'wb') as img_out:
                    # Open image output file for writing
                    image_req = urllib.request.Request(img_link, headers=self.headers)
                    # Download image from link and save to output file
                    with urllib.request.urlopen(image_req) as image_file:
                        img_out.write(image_file.read())
                        sleep(0.2)
            except:
                if print_progress:
                    print('Error downloading:', img_link)
                self.log_file.write(strftime("%a, %d %b %Y %H:%M:%S-> ", gmtime()) + 'Error downloading:' + img_link)
