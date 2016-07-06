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
                   "(created_time, icon, id, link, message, multi_share_optimized, name, picture)"
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
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
            can_remove = comment['can_remove']
            created_time = comment['created_time']
            id = comment['id']
            like_count = comment['like_count']
            message = comment['message']
            user_likes = comment['user_likes']
            from_id = comment['from']['id']
            from_name = comment['from']['name']
            data_comment = (id_post, can_remove, created_time, id, like_count, message, user_likes)
            cursor.execute(insert_comment(), data_comment)
            data_comment_from = (cursor.lastrowid, from_id, from_name)
            cursor.execute(insert_comment_from(), data_comment_from)
            connection.commit()
        url = comments['paging']['next']
        printAllComments('', url, connection, id_post)
    else:
        response = urllib2.urlopen(next_url)
        response_data = json.loads(response.read())
        data_comments = response_data['data']
        try:
            for comment in data_comments:
                can_remove = comment['can_remove']
                created_time = comment['created_time']
                id = comment['id']
                like_count = comment['like_count']
                message = comment['message']
                user_likes = comment['user_likes']
                from_id = comment['from']['id']
                from_name = comment['from']['name']
                data_comment = (id_post, can_remove, created_time, id, like_count, message, user_likes)
                cursor.execute(insert_comment(), data_comment)
                data_comment_from = (cursor.lastrowid, from_id, from_name)
                cursor.execute(insert_comment_from(), data_comment_from)
                connection.commit()
            url = response_data['paging']['next']
            printAllComments('', url, connection, id_post)
        except Exception:
            return 1

def extract_data_like_post(likes, next_url, connection, id_post):
    cursor = get_cursor(connection)
    if next_url == '':
        data_likes = likes['data']
        for like in data_likes:
            id = like['id']
            name = like['name']
            data_like = (id_post, id, name)
            cursor.execute(insert_post_like(), data_like)
            connection.commit()
        url = likes['paging']['next']
        extract_data_like_post('', url, connection, id_post)
    else:
        response = urllib2.urlopen(next_url)
        response_data = json.loads(response.read())
        data_likes = response_data['data']
        try:
            for like in data_likes:
                id = like['id']
                name = like['name']
                data_like = (id_post, id, name)
                cursor.execute(insert_post_like(), data_like)
                connection.commit()
            url = response_data['paging']['next']
            extract_data_like_post('', url, connection, id_post)
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

if __name__ == "__main__":
    accessToken = 'EAACEdEose0cBALLFRZCWeL8iCovlurXAHVO61e2LnQDebAaSRxNgAWznMxg94ZCmUe6Hct63dlLZCtdM0HjNtYkXVat6cm8tVvNHffjGFSkg99TFHkpKjNFyrMmbZAP2XgamtdCp1ZCusocDEdUS7ZBXA0asQALEN9WFUv0QtN3gZDZD'
    graph = facebook.GraphAPI(access_token=accessToken, version='2.2')
    post = graph.get_object(id='790489781052943')
    created_time = post['created_time']
    icon = post['icon']
    id = post['id']
    link = post['link']
    message = post['message']
    multi_share_optimized = post['multi_share_optimized']
    name = post['name']
    picture = post['picture']
    from_category = post['from']['category']
    from_id = post['from']['id']
    from_name = post['from']['name']
    comments = post['comments']
    likes = post['likes']
    #create db connection
    connection = connect_db()
    # insert the data we pulled into db
    cursor = get_cursor(connection)
    data_post = (created_time, icon, id, link, message, multi_share_optimized, name, picture)

    #data_like = (created_time, icon, id, link, message, multi_share_optimized, name, picture)
    try:
        cursor.execute(insert_post(), data_post)
        id_post = cursor.lastrowid
        data_from = (id_post, from_category, from_id, from_name)
        cursor.execute(insert_post_from(), data_from)
        #cursor.execute(insert_post_like(), data_like)
    except Error as error:
        print(error)
    # commit the data to the db
    connection.commit()
    result1 = extract_data_like_post(likes, '', connection, id_post)
    print "Termino de extraer los likes del post"
    result1 = printAllComments(comments, '', connection, id_post)
    print "Termino de extraer los comments del post"



#Use cursor.lastrowid to get the last row ID inserted on the cursor object,
# or connection.insert_id() to get the ID from the last insert on that connection.


#https://graph.facebook.com/cocacolaec/posts?access_token=id

