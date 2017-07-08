from flask import Flask, render_template
import json
import re
import urllib2
import sys
from flask import request
from bs4 import BeautifulSoup  # $ pip install beautifulsoup4
from flask import Flask
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/result',methods = ['POST'])
def result():
    print "hello"
    name = request.form['text']
    print name
    usernames = name.split(',')
    print usernames
    posts = [  # fake array of posts
        {
            'username':  '',
            'userid': '',
            'userfullname': ''
        }
    ]
    for username in usernames:
        try:
            posts.append( # fake array of posts
            {
                'username': username,
                'userid': read_json(get_page_data(username)),
                'userfullname': read_json_name(get_page_data(username))
            }
        )
        except:
                posts.append( # fake array of posts
                {
                    'username': username,
                    'userid': 'No Details(Check Username)',
                    'userfullname': "No record"
                }
            )


    return render_template('result.html',posts=posts)

def read_json(html):
    soup = BeautifulSoup(html, "html5lib")
    script = soup.find('script', text=re.compile('window\._sharedData'))
    json_text = re.search(r'^\s*window\._sharedData\s*=\s*({.*?})\s*;\s*$',script.string, flags=re.DOTALL | re.MULTILINE).group(1)
    data = json.loads(json_text)
    return data["entry_data"]["ProfilePage"][0]["user"]["id"]


def read_json_name(html):
    soup = BeautifulSoup(html, "html5lib")
    script = soup.find('script', text=re.compile('window\._sharedData'))
    json_text = re.search(r'^\s*window\._sharedData\s*=\s*({.*?})\s*;\s*$',script.string, flags=re.DOTALL | re.MULTILINE).group(1)
    data = json.loads(json_text)
    return data["entry_data"]["ProfilePage"][0]["user"]["full_name"]


def get_page_data(username):
    master = "https://www.instagram.com/"
    some_url = master+username+"/"
    content = urllib2.urlopen(some_url).read()
    return content


if __name__ == "__main__":
    app.run()

