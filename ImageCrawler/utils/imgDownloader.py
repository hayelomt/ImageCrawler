import os
import urllib
import urllib.request
import sys
from urllib.parse import urlparse
from time import gmtime, strftime, sleep

def chunk_report(bytes_so_far, chunk_size, total_size):
    percent = float(bytes_so_far) / total_size
    percent = round(percent*100, 2)
    sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%)\r" %
                    (bytes_so_far, total_size, percent))
    
    if bytes_so_far >= total_size:
        sys.stdout.write('\n')

def chunk_read(response, chunk_size=8192, report_hook=None):
    total_size = int(response.getheader('Content-Length'))
    bytes_so_far = 0
    img = b''
    
    while 1:
        chunk = response.read(chunk_size)
        img = img + chunk
        bytes_so_far += len(chunk)
        
        if not chunk:
            break
            
        if report_hook:
            report_hook(bytes_so_far, chunk_size, total_size)
            
    return img

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

        # Create parent folder to store image
        parent_folder = self.dir_name + '/' + parsed_url.netloc

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
            print('\t\t', file_path)
            if print_progress:
                print('Already downloaded:', img_link)
            self.log_file.write(strftime("%a, %d %b %Y %H:%M:%S-> ", gmtime()) + 'Already downloaded:' +
                                img_link + '\n')
        else:
            retry = 0
            while retry <= 3:
                try:
                    with open(file_path, 'wb') as img_out:
                        print(img_link)
                        # Open image output file for writing
                        image_req = urllib.request.Request(img_link, headers=self.headers)
                        # Download image from link and save to output file
                        with urllib.request.urlopen(image_req) as image_response:
                            img_read = chunk_read(image_response, report_hook=chunk_report)
                            img_out.write(img_read)
                            sleep(0.2)
                    retry = 4
                except:
                    sleep(1)
                    retry += 1
                    if print_progress:
                        print('Error downloading:', img_link)
                    self.log_file.write(strftime("%a, %d %b %Y %H:%M:%S-> ", gmtime()) + 'Error downloading:' + img_link)
                    if retry <= 3:
                        if print_progress:
                            print('Retrying' +str(retry) + ':', img_link)
                        self.log_file.write(strftime("%a, %d %b %Y %H:%M:%S-> ", gmtime()) + 'Retrying ' + str(retry) + ':' + img_link)
                    else:
                        if print_progress:
                            print('Failed downloading:', img_link)
                        self.log_file.write(strftime("%a, %d %b %Y %H:%M:%S-> ", gmtime()) + 'Failed downloading:' + img_link)
                        
# d = ImageDownloader()
# d.download('http://localhost:4000/imgs/course/cover/etabs.jpg')