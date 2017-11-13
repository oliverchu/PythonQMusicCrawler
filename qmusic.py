#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
import urllib

requestCateParam = {"comm": {"ct": 24}, "category": {
    "method": "get_hot_category",
    "param": {
        "qq": ""
    },
    "module": "music.web_category_svr"
},
                    "recomPlaylist": {
                        "method": "get_hot_recommend",
                        "param": {
                            "async": 1,
                            "cmd": 2
                        },
                        "module": "playlist.HotRecommendServer"
                    },
                    "playlist": {
                        "method": "get_playlist_by_category",
                        "param": {
                            "id": 8,
                            "curPage": 1,
                            "size": 40,
                            "order": 5,
                            "titleid": 8
                        },
                        "module": "playlist.PlayListPlazaServer"
                    },
                    "new_song": {
                        "module": "QQMusic.MusichallServer",
                        "method": "GetNewSong",
                        "param": {
                            "type": 0
                        }
                    },
                    "new_album": {
                        "module": "QQMusic.MusichallServer",
                        "method": "GetNewAlbum",
                        "param": {
                            "type": 0,
                            "category": "-1",
                            "genre": 0,
                            "year": 1,
                            "company": -1,
                            "sort": 1,
                            "start": 0,
                            "end": 39
                        }
                    },
                    "toplist": {
                        "module": "music.web_toplist_svr",
                        "method": "get_toplist_index",
                        "param": {}
                    },
                    "focus": {
                        "module": "QQMusic.MusichallServer",
                        "method": "GetFocus",
                        "param": {}
                    }}

URL_CATEGORY = "https://u.y.qq.com/cgi-bin/musicu.fcg?%s"
URL_SEARCH = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?%s"

global_song = None


def get_top():
    if global_song is None:
        param = json.dumps(requestCateParam, encoding="utf-8").replace(" ", "")
        params = urllib.urlencode({"data": param})
        res = urllib.urlopen(URL_CATEGORY % params).read()
        global global_song
        global_song = json.loads(res, encoding="utf-8")
    return global_song


def get_new_songs():
    '''{
    "size": 100,
      "song_list": [
        {
          "action": {
            "alert": 100007,
            "icons": 0,
            "msgdown": 0,
            "msgfav": 0,
            "msgid": 14,
            "msgpay": 3,
            "msgshare": 0,
            "switch": 602883
          },
          "album": {
            "id": 2326850,
            "mid": "00459BEP32YDr9",
            "name": "流行",
            "subtitle": "",
            "time_public": "2017-11-07",
            "title": "流行"
          },
          "bpm": 0,
          "data_type": 0,
          "file": {
            "media_mid": "102WYrkV3TrVnK",
            "size_128mp3": 3157035,
            "size_192aac": 4766726,
            "size_192ogg": 4753252,
            "size_24aac": 612512,
            "size_320mp3": 7892304,
            "size_48aac": 1201179,
            "size_96aac": 2403666,
            "size_ape": 24883817,
            "size_dts": 0,
            "size_flac": 24872390,
            "size_try": 0,
            "try_begin": 0,
            "try_end": 0
          },
          "fnote": 4009,
          "genre": 1,
          "id": 204672190,
          "index_album": 1,
          "index_cd": 0,
          "interval": 197,
          "isonly": 1,
          "ksong": {
            "id": 0,
            "mid": ""
          },
          "label": "0",
          "language": 0,
          "mid": "002WYrkV3TrVnK",
          "modify_stamp": 0,
          "mv": {
            "id": 1379619,
            "name": "",
            "title": "",
            "vid": "f00251kjvu4"
          },
          "name": "流行",
          "pay": {
            "pay_down": 1,
            "pay_month": 0,
            "pay_play": 0,
            "pay_status": 0,
            "price_album": 2000,
            "price_track": 0,
            "time_free": 0
          },
          "singer": [
            {
              "id": 4615,
              "mid": "002ZOuVm3Qn20Y",
              "name": "李宇春",
              "title": "李宇春",
              "type": 1,
              "uin": 0
            }
          ],
          "status": 0,
          "subtitle": "",
          "time_public": "2017-11-07",
          "title": "流行",
          "trace": "",
          "type": 0,
          "url": "http://stream10.qqmusic.qq.com/216672190.wma",
          "version": 0,
          "volume": {
            "gain": -9.67,
            "lra": 5.079,
            "peak": 0.999}}
    :return: dictionary of new song
    '''
    if global_song is None:
        get_top()
    return global_song["new_song"]["data"]


def search(words):
    params = urllib.urlencode({"w": words})
    j = urllib.urlopen(URL_SEARCH % params).read()[9:-1]
    return json.loads(j)
