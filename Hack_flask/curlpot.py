import subprocess
from io import StringIO
import pycurl as pycurl
import requests
import urllib.request

from PIL import Image


def post3():
    args = ['curl', '-v', '-X', 'POST', 'http://api-soft.photolab.me/photolab_process.php', '-F image_url[1]=https://pp.userapi.com/c846216/v846216132/188c35/MZ1GOIOJY8Q.jpg', '-F', 'template_name="1511"']
    subprocess.call(args)


def post():
    headers = {
        'Content-Type': 'application/json',
    }
    params = (
        ('image_url[1]', 'https://pp.userapi.com/c849524/v849524582/10eb5f/crtkPzey4rQ.jpg'), ('template_name', 1511),)
    response = requests.post("http://api-soft.photolab.me/photolab_process.php", headers=headers, params=params)
    print(response.content)
    return


def post2():
    headers = {'Content-Type': 'application/json', }
    params = (('combo_id', '1791396,'),)
    response = requests.post("http://api-soft.photolab.me/photolab_steps.php", headers=headers, params=params)
    print(response.content)
    return


if __name__ == "__main__":
    post3()
