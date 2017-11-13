#!/usr/bin/python
# -*- coding: UTF-8 -*-


import requests
import json
import sqlite3
import time
import pygame
import webbrowser
import schedule
import qmusic as qm

conn = sqlite3.connect('qmusic.db')
print "Opened database successfully"
c = conn.cursor()
c.execute('''
  CREATE TABLE  IF NOT EXISTS  top_songs(
  topID INT  PRIMARY KEY  NOT NULL ,
  ListName TEXT, 
  listennum INT,
  pic TEXT,
  update_key TEXT,
  showtime DATE,
  GroupName TEXT,
  Type INT
)''')
c.execute('''
  CREATE TABLE IF NOT EXISTS  top_song_list(
  songid INT PRIMARY KEY NOT NULL ,
  albumname TEXT, 
  songorig TEXT,
  songname TEXT,
  albumid TEXT,
  singer TEXT,
  songmid TEXT,
  date TEXT,
  tid TEXT,
  lyric TEXT,
  shortcut TEXT 
)''')

conn.commit()

num = 0


def get_top():
    url_top = "https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_opt.fcg?page=index&format=html&tpl=macv4&v8debug=1" \
              "&jsonCallback= "
    json_top = requests.get(url_top).content[14:-1]
    dic_top = json.loads(json_top)
    # pretty_json(dic_top)
    for group in dic_top:
        for song in group['List']:
            d = (song['topID'],
                 song['ListName'],
                 song['listennum'],
                 song['pic'],
                 song['update_key'],
                 song['showtime'],
                 group['GroupName'],
                 group['Type'])
            try:
                c.execute("INSERT OR IGNORE INTO top_songs VALUES(?,?,?,?,?,?,?,?)", d)
                conn.commit()
            except Exception, ex:
                print "apply top song list with errors", ex.message
            type = ""
            if song['type'] == 0:
                type = "top"
            else:
                type = "global"
            get_top_songs(song['topID'], song['update_key'], type)
    return dic_top


def pretty_json(dic):
    print json.dumps(dic, indent=4, sort_keys=False, ensure_ascii=False)


def get_top_songs(tid, update_Key, type):
    url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?tpl=3&page=detail&date=%s&topid=%s&type=%s' \
          '&song_begin=0&song_num=100&g_tk=5381&jsonpCallback=&loginUin=0&hostUin=0&format' \
          '=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0 ' % (update_Key, tid, type)
    content = requests.get(url).content
    dic_top_songs = json.loads(content)
    # pretty_json(dic_top_songs)
    if dic_top_songs['code'] == -1:
        return
    for s in dic_top_songs['songlist']:
        data = s['data']
        id = data['songid']
        d = (id,
             data['albumname'],
             data['songorig'],
             data['songname'],
             data['albumid'],
             json.dumps(
                 data['singer']),
             data['songmid'],
             update_Key,
             tid)
        try:
            print "execute song with id = %s" % (data['songid'])
            c.execute(
                "INSERT OR IGNORE INTO top_song_list(songid,albumname,songorig,songname,albumid,singer,songmid,date,tid) VALUES ( ?,?,?,?,?,?,?,?,?)",
                d)

            conn.commit()
        except Exception, ex:
            print "apply song list data with errors:", ex.message
            return
        lyric = get_song_detail(id)
        try:
            c.execute("UPDATE top_song_list SET lyric = ? WHERE songid = ?", (lyric, id))
            conn.commit()
        except Exception as ex:
            print "append lyric with errors:", ex.message

def get_song_detail(sid):
    params = '''
    {"comm":
    {"g_tk":1677012956,"uin":0,"format":"json","inCharset":"utf-8","outCharset":"utf-8",
    "notice":0,"platform":"h5","needNewCode":1},"song_detail":{"module":"music.pf_song_detail_svr",
    "method":"get_song_detail","param":{"song_id":%s}}}
    ''' % (sid)

    url = "https://u.y.qq.com/cgi-bin/musicu.fcg?_=%s" % sid
    dic_detail = json.loads(requests.post(url, params).content)
    # pretty_json(dic_detail)
    for info in dic_detail["song_detail"]["data"]["info"]:
        if info["type"] == "lyric":
            lyric = info["content"][0]["value"]
            return lyric
    return ""


def get_single_song_local(songmid):
    return "ws.stream.qqmusic.qq.com/C100%s.m4a?fromtag=38" % (songmid)


def get_single_song(songmid):
    url = "https://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg?songmid=%s&tpl=yqq_song_detail&format" \
          "=json&callback=&g_tk=5381&jsonpCallback=&loginUin=0&hostUin=0" \
          "&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0 " % (songmid)
    content = requests.get(url).content
    dic_single_song = json.loads(content)
    pretty_json(dic_single_song)
    urls = dic_single_song["url"]
    id = dic_single_song["data"][0]["id"]
    return urls[str(id)]


def play_song(url):
    track = pygame.mixer.music.load(url)
    pygame.mixer.music.play()


def download_file(url, path):
    r = requests.get(url, stream=True)
    f = open(path, "wb")
    for chunk in r.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)
    f.close()


def show_lyric(lyric):

    return


if __name__ == "__main__":
    # get_top()
    # newSong = qm.get_new_songs()
    # print "Size","=",newSong["size"]
    # for v in newSong["song_list"]:
    #     print get_single_song(v["mid"])
    qm.search("生命要继续")
    # r = c.execute("SELECT lyric FROM top_song_list WHERE songmid = ?", ("001bhwUC1gE6ep",))
    # lyric = ""
    # for d in r:
    #     lyric = d[0]
    #     print  lyric
    #     break
    # show_lyric(lyric)
    # import datetime
    #
    # l = "[04:43.18]LOvesadsa"
    # print l[0:10]
    # now = datetime.datetime.strptime("[00:00.00]", "[%M:%S.%f]")
    # print datetime.datetime.strptime("[04:35.78]", "[%M:%S.%f]")
    # # schedule.every(1).seconds.do()
    # # url = "http://" + get_single_song_local("001bhwUC1gE6ep")
    # # webbrowser.open(url)
    #
    # # download_file(url, "./music.m4a")
    # # play_song("./music.m4a")
    # conn.close()
