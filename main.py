import os
from time import sleep

from src.base.base import Base

if __name__ == '__main__':
    os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
    os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
    a = Base()
    a.url_get('https://www.baidu.com')
    sleep(5)
    a.quit()



