# catfacts-snowden

<h2>Installation</h2>
This requires tesseract for optical character recognition to automate a captcha.

It also requires tor to be running and having torsocks. It checks for tor, but not much else is written for good error messages. 

<h4>Debian/Ubuntu</h4>
```bash
apt-get install tesseract-ocr
```
<h4>CentOS</h4>
install epel repo
```bash
yum install tesseract-ocr
```
<h4>Other</h4>
Try your package manager or the source is here:
https://github.com/tesseract-ocr/tesseract

<h2>Configuration</h2>
```bash
git clone https://github.com/IDSninja/catfacts-snowden
```
edit the config.ini: input your twitter application's API credentials.

https://apps.twitter.com/

Near the top of both scripts, there is an unsub variable. You can change it but keep it under 52 characters, and use +'s for spaces in woem.sh. If you want to disable unsubscribing, remove the elif construct at the bottom of on_data.

<h2>Usage</h2>
The stream API does output full tweets, but only the raw numbers will be saved in numbers.txt. Either run it in screen or a seperate terminal or direct the output to /dev/null

It's recommended to let the stream.py run until at least a few hundred numbers are collected, because woem will keep looping as fast as possible.

```bash
python stream.py
bash woem.sh
```

Only US numbers will be used and commercial numbers like 877 and 800 will be stripped from the numbers file when the script is ran. The scripts are pretty short and easy to read.
