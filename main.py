import requests
import json
import sqlite3
import time

conn = sqlite3.connect('qmusic.db')
print "Opened database successfully"
c = conn.cursor()
c.execute('''
  CREATE TABLE  IF NOT EXISTS  top_songs(
  topID INT PRIMARY KEY NOT NULL ,
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
  albumid INT,
  singer TEXT,
  songmid TEXT,
  date TEXT,
  tid INT  
)''')

conn.commit()


def get_top():
    url_top = "https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_opt.fcg?page=index&format=html&tpl=macv4&v8debug=1" \
              "&jsonCallback= "
    json_top = requests.get(url_top).content[14:-1]
    dic_top = json.loads(json_top)
    pretty_json(dic_top)
    for group in dic_top:
        for song in group['List']:
            # sql = "INSERT INTO top_songs VALUES(%d,'%s',%d,'%s','%s','%s','%s',%d)"%(song['topID'],
            #                                                                        song['ListName'],
            #                                                                        song['listennum'],
            #                                                                        song['pic'],
            #                                                                        song['update_key'],
            #                                                                        song['showtime'],
            #                                                                        group['GroupName'],
            #                                                                        group['Type'])
            # c.execute(sql)
            type = ""
            if song['type'] == 0:
                type = "top"
            else:
                type = "global"
            get_top_songs(song['topID'], song['update_key'], type)

    # conn.commit()
    return dic_top


def pretty_json(dic):
    print json.dumps(dic, indent=4, sort_keys=False, ensure_ascii=False)


def get_top_songs(tid, update_Key, type):
    """
    https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?tpl=3&page=detail&date=2017_38
    &topid=108&type=global&song_begin=0&song_num=30&g_tk=5381&jsonpCallback=MusicJsonCallbacktoplist
    &loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0
    songid INT PRIMARY KEY NOT NULL ,
  albumname TEXT,
  songorig TEXT,
  songname TEXT,
  albumid INT,
  singer TEXT,
  songmid TEXT
    date TEXT
    """
    url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?tpl=3&page=detail&date=%s&topid=%s&type=%s' \
          '&song_begin=0&song_num=100&g_tk=5381&jsonpCallback=&loginUin=0&hostUin=0&format' \
          '=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0 ' % (update_Key, tid, type)
    dic_top_songs = json.loads(requests.get(url).content)
    # pretty_json(dic_top_songs)
    for s in dic_top_songs['songlist']:
        data = s['data']
        try:
            sql = "INSERT INTO top_song_list VALUES (%d,'%s','%s','%s',%d,'%s','%s','%s',%d)" % (data['songid'],
                                                                                                 data['albumname'],
                                                                                                 data['songorig'],
                                                                                                 data['songname'],
                                                                                                 data['albumid'],
                                                                                                 json.dumps(
                                                                                                     data['singer']),
                                                                                                 data['songmid'],
                                                                                                 update_Key,
                                                                                                 tid)
            c.execute(sql)
        except Exception as ex:
            print ex.message

    conn.commit()


def get_song_detail(sid):
    params = '''
    {"comm":
    {"g_tk":1677012956,"uin":0,"format":"json","inCharset":"utf-8","outCharset":"utf-8",
    "notice":0,"platform":"h5","needNewCode":1},"song_detail":{"module":"music.pf_song_detail_svr",
    "method":"get_song_detail","param":{"song_id":%s}}}
    ''' % (sid)

    url = "https://u.y.qq.com/cgi-bin/musicu.fcg?_=%s" % sid
    dic_detail = json.loads(requests.post(url, params).content)
    pretty_json(dic_detail)
    return dic_detail


get_top()
# https://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg?songmid=003hvIkL1QiILk&tpl=yqq_song_detail&format=jsonp&callback=getOneSongInfoCallback&g_tk=5381&jsonpCallback=getOneSongInfoCallback&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0

# get_song_detail("203691607")
conn.close()
