# catfacts-snowden

<h2>Installation</h2>
This requires tesseract for optical character recognition

<h4>Debian/Ubuntu</h4>
apt-get install tesseract-ocr

<h4>CentOS</h4>
install epel repo
yum install tesseract-ocr

<h4>Other</h4>
Try your package manager or the source is here:
https://github.com/tesseract-ocr/tesseract

<h2>Usage</h2>
```bash
git clone https://github.com/IDSninja/catfacts-snowden
```
edit the config.ini file of the stream.py. Input your twitter application's API credentials.
The stream API does output full tweets, but only the raw numbers will be saved in numbers.txt. Either run it in screen or a seperate terminal or direct the output to /dev/null
```bash
python stream.py
bash woem.sh
```
Only US numbers will be used and commercial numbers like 877 and 800 will be stripped from the numbers file when the script is ran. The scripts are pretty short and easy to read.
