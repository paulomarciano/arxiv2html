# arxiv2html

Automated script to download html version of arxiv paper from arxiv-vanity. The script searches the resulting HTML for image tags and alters them so images are loaded locally. Everything is saved in CWD/Downloads/<arxiv ID\>.


Usage:

`python3 arxiv2html.py <arxiv ID>`

After downloading, files can be converted to Kindle format with your favorite  tools (I recommend Calibre) for reading on e-ink screens.