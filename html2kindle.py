import requests
import re
import sys
import os
import time
from bs4 import BeautifulSoup

if __name__ == "__main__":

    if len(sys.argv)<2:

        print('Please specify an arxiv paper ID.')

    else:
        print('Trying to fetch {}...'.format(sys.argv[1]))

        while True:
            file = requests.get('https://www.arxiv-vanity.com/papers/'
                                + sys.argv[1] + '/' ,
                                stream=True)
            soup = BeautifulSoup(file.content,'lxml')
            if len(soup.findAll("p",
                   text=("This paper doesn't have LaTeX source code, "
                         "so it can't be rendered as a web page.")
                         )
                  ) > 0:
                  print(("This paper doesn't have LaTeX source code, "
                        "so it can't be rendered as a web page."))
                  exit()
            elif len(soup.findAll("div", {"class": "waiter-spinner"})) == 0:
                print('Got your paper. Getting images...')
                break
            else:
                print(
                'arxiv-vanity is rendering your paper. Waiting...'
                )
                time.sleep(60)

        # getting the path to download folder.
        cwd = os.getcwd()
        path=cwd + '/Downloads/' + sys.argv[1] + '/'

        # creating relevant directories.
        try:
            os.mkdir(cwd + '/Downloads/')
        except:
            pass

        try:
            os.mkdir(path)
        except:
            pass

        # Writing file.
        with open(path+'newfile.html','wb') as f:
            for chunk in file:
                f.write(chunk)

        # Editing the resulting HTML file to make images local.
        with open(path + 'newfile.html','r') as f:
            a=''
            i=1;
            for line in f:
                s = re.search("""src=\"http(s)?:(.+)\.png\"""",line)
                if s:
                    print('Fetching '+s.string[s.start(0)+5:s.end(0)-1])
                    response=requests.get(s.string[s.start(0)+5:s.end(0)-1],
                                          stream=True)
                    wf = open(path+'fig'+str(i)+'.png','wb')
                    for chunk in response:
                        wf.write(chunk)
                    wf.close()
                    a += line.replace(s.string[s.start(0) + 5:s.end(0)-1],
                                      './fig' + str(i) + '.png')
                    i += 1
                else:
                    a+=line
        # Saving.
        with open(path + sys.argv[1] + '.html','w') as f:
            print('writing to {} ...'.format(path + sys.argv[1] + '.html'))
            f.write(a)

        # Removing Temp Files.
        os.remove(path+'newfile.html')
        print("...And you're done. Enjoy!")
