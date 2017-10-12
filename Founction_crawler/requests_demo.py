# -*- coding: utf-8 -*-
import requests


def get_json():
    r = requests.get('https://api.github.com/events')
    print(r.status_code)
    print(r.headers['Content-Type'])
    print(r.text)
    print(r.json())


def get_querystring():
    params = {'qs1': 'value1', 'qs2': 'value2'}
    r = requests.get('http://httpbin.org/get', params=params)
    print(r.status_code)
    print(r.content)


def get_custom_headers():
    headers = {'x-header1': 'value1', 'x-header2': 'value2'}
    r = requests.get('http://httpbin.org/get', headers=headers)
    print(r.status_code)
    print(r.content)


def get_cookie():
    headers = {'User-Agent': 'Chrome'}
    url = 'http://www.douban.com'
    r = requests.get(url, headers=headers)
    print(r.status_code)
    print(r.cookies)
    requests.get(url, headers=headers)
    print(r.status_code)
    print(r.cookies)


def post():
    r = requests.post('http://httpbin.org/post', data={'user': 'username', 'pass': 'password'})
    print(r.status_code)
    print(r.headers['Content-Type'])
    print(r.content)


if __name__ == '__main__':
    get_json()
    get_querystring()
    get_custom_headers()
    get_cookie()
    post()