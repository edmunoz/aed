# -*- coding: utf-8 -*-
#!/usr/bin/python2.7

import facebook #sudo pip install facebook
import urllib2
import MySQLdb as mdb #sudo apt-get install python-mysqldb
import json
from mysql.connector import Error #sudo apt-get install python-mysql.connector
import codecs

#password:SK5CTTs8zXV9
#user:connie_usr_aed
#base:connie_facebook
#server:108.167.133.34
def connect_db():
    connection = mdb.connect('108.167.133.34', 'connie_usr_aed', 'SK5CTTs8zXV9', 'connie_facebook')
    #connection = mdb.connect('localhost', 'root', 'root', 'facebook_data')
    connection.set_character_set('utf8mb4')
    return connection

def get_cursor(connect):
    cursor = connect.cursor()
    cursor.execute('SET NAMES utf8mb4;')
    cursor.execute('SET CHARACTER SET utf8mb4;')
    cursor.execute('SET character_set_connection=utf8mb4;')
    return cursor

def insert_post():
    # insert_info = ("INSERT INTO post "
    #                "(id, message, picture, link, name, caption, description, icon, type, status_type, created_time, updated_time, shares)"
    #                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    insert_info = ()

    return insert_info

def insert_post_from():
    insert_info = ("INSERT INTO post_from "
                   "(id_post, category, id, name)"
                   "VALUES (%s, %s, %s, %s)")
    return insert_info

def insert_post_like():
    insert_info = ("INSERT INTO post_like "
                   "(id_post, id, name)"
                   "VALUES (%s, %s, %s)")
    return insert_info

def insert_comment():
    insert_info = ("INSERT INTO comment "
                   "(id_post, can_remove, created_time, id, like_count, message, user_likes)"
                   "VALUES (%s, %s, %s,%s, %s, %s, %s)")
    return insert_info

def insert_comment_from():
    insert_info = ("INSERT INTO comment_from "
                   "(id_comment, id, name)"
                   "VALUES (%s, %s, %s)")
    return insert_info

def printAllComments(comments, next_url, connection, id_post):
    cursor = get_cursor(connection)
    if next_url == '':
        data_comments = comments['data']
        for comment in data_comments:
            can_remove = getValue(comment, 'can_remove', '')
            created_time = getValue(comment, 'created_time', '')
            id = getValue(comment, 'id', '')
            like_count = getValue(comment, 'like_count', '')
            message = getValue(comment, 'message', '')
            user_likes = getValue(comment, 'user_likes', '')
            from_id = getValue(comment, 'from', 'id')
            from_name = getValue(comment, 'from', 'name')
            data_comment = (id_post, can_remove, created_time, id, like_count, message, user_likes)
            try:
                cursor.execute(insert_comment(), data_comment)
                connection.commit()
            except Exception, e:
                print e
                continue
            data_comment_from = (cursor.lastrowid, from_id, from_name)
            try:
                cursor.execute(insert_comment_from(), data_comment_from)
                connection.commit()
            except Exception, e:
                print e
                continue
        url = getValue(comments, 'paging', 'next')
        if url != '':
            printAllComments('', url, connection, id_post)
        else:
            return 1
    else:
        response = urllib2.urlopen(next_url)
        response_data = json.loads(response.read())
        data_comments = response_data['data']
        try:
            for comment in data_comments:
                can_remove = getValue(comment, 'can_remove', '')
                created_time = getValue(comment, 'created_time', '')
                id = getValue(comment, 'id', '')
                like_count = getValue(comment, 'like_count', '')
                message = getValue(comment, 'message', '')
                user_likes = getValue(comment, 'user_likes', '')
                from_id = getValue(comment, 'from', 'id')
                from_name = getValue(comment, 'from', 'name')
                data_comment = (id_post, can_remove, created_time, id, like_count, message, user_likes)
                try:
                    cursor.execute(insert_comment(), data_comment)
                    connection.commit()
                except Exception, e:
                    print e
                    continue
                data_comment_from = (cursor.lastrowid, from_id, from_name)
                try:
                    cursor.execute(insert_comment_from(), data_comment_from)
                    connection.commit()
                except Exception, e:
                    print e
                    continue
            url = getValue(response_data, 'paging', 'next')
            if url != '':
                printAllComments('', url, connection, id_post)
            else:
                return 1
        except Exception:
            return 1

def extract_data_like_post(likes, next_url, connection, id_post):
    cursor = get_cursor(connection)
    if next_url == '':
        data_likes = likes['data']
        for like in data_likes:
            id = getValue(like, 'id', '')
            name = getValue(like, 'name', '')
            data_like = (id_post, id, name)
            try:
                cursor.execute(insert_post_like(), data_like)
                connection.commit()
            except Exception, e:
                print e
                continue
        url = getValue(likes, 'paging', 'next')
        if url != '':
            extract_data_like_post('', url, connection, id_post)
        else:
            return 1
    else:
        response = urllib2.urlopen(next_url)
        response_data = json.loads(response.read())
        data_likes = getValue(response_data, 'data', '')
        try:
            for like in data_likes:
                id = getValue(like, 'id', '')
                name = getValue(like, 'name', '')
                data_like = (id_post, id, name)
                try:
                    cursor.execute(insert_post_like(), data_like)
                    connection.commit()
                except Exception, e:
                    print e
                    continue
            url = getValue(response_data, 'paging', 'next')
            if url != '':
                extract_data_like_post('', url, connection, id_post)
            else:
                return 1
        except Exception:
            return 1

def get_last_id_post(id, connection):
    cursor = get_cursor(connection)
    cursor.execute("SELECT COUNT(id) FROM post WHERE id = (%s)", id)
    row = cursor.fetchall()
    last_id = row[0][0]
    if(last_id == 0):
        return True
    else:
        return False

def read_all_post(posts, next_url, connection):
    cursor = get_cursor(connection)
    if next_url == '':
        data_posts = posts['data']
        for post in data_posts:
            if(get_last_id_post(getValue(post, 'id', ''), connection)):#Si no esta en la base lo guardo
                #post
                id = getValue(post, 'id', '')
                message = getValue(post, 'message', '')
                picture = getValue(post, 'picture', '')
                link = getValue(post, 'link', '')
                name = getValue(post, 'name', '')
                caption = getValue(post, 'caption', '')
                description = getValue(post, 'description', '')
                icon = getValue(post, 'icon', '')
                type = getValue(post, 'type', '')
                status_type = getValue(post, 'status_type', '')
                created_time = getValue(post, 'created_time', '')
                updated_time = getValue(post, 'updated_time', '')
                shares = getValue(post, 'shares', 'count')
                data_post = (id, message, picture, link, name, caption, description, icon, type, status_type, created_time, updated_time, shares)
                try:
                    cursor.execute(insert_post(), data_post)
                    id_post = cursor.lastrowid
                except Exception, e:
                    print e
                    continue
                #post_from
                from_category = getValue(post, 'from', 'category')
                from_id = getValue(post, 'from', 'id')
                from_name = getValue(post, 'from', 'name')
                data_from = (id_post, from_category, from_id, from_name)
                try:
                    cursor.execute(insert_post_from(), data_from)
                    connection.commit()
                except Exception, e:
                    print e
                    continue
                # comment
                comments = getValue(post, 'comments', '')
                # post_like
                likes = getValue(post, 'likes', '')
                #result1 = extract_data_like_post(likes, '', connection, id_post)
                result2 = printAllComments(comments, '', connection, id_post)
        url = getValue(posts, 'paging', 'next')
        if url != '':
            read_all_post('', url, connection)
        else:
            return 1
    else:
        response = urllib2.urlopen(next_url)
        response_data = json.loads(response.read())
        data_posts = response_data['data']
        try:
            for post in data_posts:
                if (get_last_id_post(getValue(post, 'id', ''), connection)):  # Si no esta en la base lo guardo
                    # post
                    id = getValue(post, 'id', '')
                    message = getValue(post, 'message', '')
                    picture = getValue(post, 'picture', '')
                    link = getValue(post, 'link', '')
                    name = getValue(post, 'name', '')
                    caption = getValue(post, 'caption', '')
                    description = getValue(post, 'description', '')
                    icon = getValue(post, 'icon', '')
                    type = getValue(post, 'type', '')
                    status_type = getValue(post, 'status_type', '')
                    created_time = getValue(post, 'created_time', '')
                    updated_time = getValue(post, 'updated_time', '')
                    shares = getValue(post, 'shares', 'count')
                    data_post = (
                    id, message, picture, link, name, caption, description, icon, type, status_type, created_time,
                    updated_time, shares)
                    try:
                        cursor.execute(insert_post(), data_post)
                        id_post = cursor.lastrowid
                    except Exception, e:
                        print e
                        continue
                    # post_from
                    from_category = getValue(post, 'from', 'category')
                    from_id = getValue(post, 'from', 'id')
                    from_name = getValue(post, 'from', 'name')
                    data_from = (id_post, from_category, from_id, from_name)
                    try:
                        cursor.execute(insert_post_from(), data_from)
                        connection.commit()
                    except Exception, e:
                        print e
                        continue
                    # comment
                    comments = getValue(post, 'comments', '')
                    # post_like
                    likes = getValue(post, 'likes', '')
                    #result1 = extract_data_like_post(likes, '', connection, id_post)
                    result2 = printAllComments(comments, '', connection, id_post)
            url = getValue(response_data, 'paging', 'next')
            if url != '':
                read_all_post('', url, connection)
            else:
                return 1
        except Exception:
            return 1

def create_post_url(graph_url, APP_ID, APP_SECRET):
    #create authenticated post URL
    post_args = "/posts/?key=value&access_token=" + APP_ID + "|" + APP_SECRET
    post_url = graph_url + post_args

def render_to_json(graph_url):
    #render graph url call to JSON
    web_response = urllib2.urlopen(graph_url)
    readable_page = web_response.read()
    json_data = json.loads(readable_page)
    return json_data

def getValue(data, attribute1, attribute2):
    value = ''
    try:
        if(attribute2 == ''):
            value = data[attribute1]
        else:
            value = data[attribute1][attribute2]
    except:
        return value
    return value

if __name__ == "__main__":
    codecs.register(lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)
    accessToken = 'EAACEdEose0cBAKoZBSES1UanaVdRMIZBEQCVswbFjIlxaYlZBWPfK3ZBsXpEwgKcOq8JqDghvaZAp52cyzorRlW5Nv3RqFNMPdlx4pmJsEttSdydDxVtnAA3d1meMPQZBwVVQNLd25zlejj5hdA9XZBFDKawumYZAhYIpkjqFdeuZBQZDZD'
    graph_url = "https://graph.facebook.com/2016CopaAmericaCentenario/posts?access_token=" + accessToken
    posts = render_to_json(graph_url)
    connection = connect_db()
    #ass = get_last_id_post('612616258840297_791041607664427', connection)
    read_all_post(posts, '', connection)

#Use cursor.lastrowid to get the last row ID inserted on the cursor object,
# or connection.insert_id() to get the ID from the last insert on that connection.

#https://graph.facebook.com/cocacolaec/posts?access_token=id
