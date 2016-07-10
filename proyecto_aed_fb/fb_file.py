# -*- coding: utf-8 -*-
import facebook
import urllib2
import MySQLdb as mdb
import json
from mysql.connector import Error

def connect_db():
    connection = mdb.connect('localhost', 'root', 'root', 'facebook_data')
    connection.set_character_set('utf8mb4')
    return connection

def get_cursor(connect):
    cursor = connect.cursor()
    cursor.execute('SET NAMES utf8mb4;')
    cursor.execute('SET CHARACTER SET utf8mb4;')
    cursor.execute('SET character_set_connection=utf8mb4;')
    return cursor

def insert_post():
    insert_info = ("INSERT INTO post "
                   "(id, message, picture, link, name, caption, description, icon, type, status_type, created_time, updated_time, shares)"
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
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
            cursor.execute(insert_comment(), data_comment)
            data_comment_from = (cursor.lastrowid, from_id, from_name)
            cursor.execute(insert_comment_from(), data_comment_from)
            connection.commit()
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
                cursor.execute(insert_comment(), data_comment)
                data_comment_from = (cursor.lastrowid, from_id, from_name)
                cursor.execute(insert_comment_from(), data_comment_from)
                connection.commit()
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
            cursor.execute(insert_post_like(), data_like)
            connection.commit()
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
                cursor.execute(insert_post_like(), data_like)
                connection.commit()
            url = getValue(response_data, 'paging', 'next')
            if url != '':
                extract_data_like_post('', url, connection, id_post)
            else:
                return 1
        except Exception:
            return 1

def read_all_post(posts, next_url, connection):
    cursor = get_cursor(connection)
    if next_url == '':
        data_posts = posts['data']
        for post in data_posts:
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
            except Error as error:
                print(error)
            #post_from
            from_category = getValue(post, 'from', 'category')
            from_id = getValue(post, 'from', 'id')
            from_name = getValue(post, 'from', 'name')
            data_from = (id_post, from_category, from_id, from_name)
            try:
                cursor.execute(insert_post_from(), data_from)
                connection.commit()
            except Error as error:
                print(error)
            # comment
            comments = getValue(post, 'comments', '')
            # post_like
            likes = getValue(post, 'likes', '')
            result1 = extract_data_like_post(likes, '', connection, id_post)
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
                except Error as error:
                    print(error)
                # post_from
                from_category = getValue(post, 'from', 'category')
                from_id = getValue(post, 'from', 'id')
                from_name = getValue(post, 'from', 'name')
                data_from = (id_post, from_category, from_id, from_name)
                try:
                    cursor.execute(insert_post_from(), data_from)
                    connection.commit()
                except Error as error:
                    print(error)
                # comment
                comments = getValue(post, 'comments', '')
                # post_like
                likes = getValue(post, 'likes', '')
                result1 = extract_data_like_post(likes, '', connection, id_post)
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
    accessToken = 'EAACEdEose0cBAC1gQRzA8hkVZCSl1w4EptBsdm8zLZAAl0xdRiu1xvNsW4GcWtb9eDoz0tlYcYsxNEJRdwUxg5ZCpFPSZAxVTzIWIhLa3RZBLKkgHVShe2uJs8mRnYyxMgDEwxyO3crC9aDv984xiOhn0ZBIgeyGtaacKgv1auIAZDZD'
    graph_url = "https://graph.facebook.com/2016CopaAmericaCentenario/posts?access_token=" + accessToken
    posts = render_to_json(graph_url)
    connection = connect_db()
    read_all_post(posts, '', connection)




#Use cursor.lastrowid to get the last row ID inserted on the cursor object,
# or connection.insert_id() to get the ID from the last insert on that connection.


#https://graph.facebook.com/cocacolaec/posts?access_token=id
