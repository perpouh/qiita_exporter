# -*- coding: utf-8 -*-
#
# Update an article via Qiita API
#
import sys
import os
import logging
import json
import requests
import qiita_api

QIITA_URL = 'https://qiita.com/api/v2/items'

TAGS = ["id", "title", "tags"]

def parse(item):
    return {
        'title': item['title'],
        'qiita_id': item['id'],
        'tags': item['tags'],
        'body': f'''
        この記事はGitHub Pagesへ移動しました。\n
        "https://perpouh.github.io/blog/qiita/{item['title']}.html"
        ''',
        'tweet': False,
        'private': False,
    }

def submit(item, token, url=QIITA_URL, article_id=None):
    u'''Submit to Qiita v2 API'''
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }

    if article_id is None or article_id == '':
        return
    else:
        url = "{}/{}".format(url, article_id)
        res = requests.patch(url, headers=headers, json=parse(item))
    if res.status_code >= 400:
        logging.error(res.json())
    res.raise_for_status()

    logging.info(json.dumps(res.json(), indent=2))

    return res

def execute(item, token):
    if item is None:
        logging.warning("SKIP. No qiita_id tag found.")
        return
    item_id = item['id']

    res = submit(item, token=token, article_id=item_id)

if __name__ == "__main__":
    argvs = sys.argv
    token = argvs[1]
    user = argvs[2]
    qiitaApi = qiita_api.QiitaApi(token)

    items = qiitaApi.query_user_items(user)
    for item in items:
      execute(item, token)
      break