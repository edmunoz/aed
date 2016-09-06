import MySQLdb as mdb

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

def get_comment(id, inicio, fin):
    query_comment = "SELECT message FROM comment WHERE id_post = " + str(id) + " AND STR_TO_DATE(created_time, '%Y-%m-%dT%H:%i:%s+0000') BETWEEN STR_TO_DATE('"+ str(inicio) +"', '%Y-%m-%dT%H:%i:%s+0000') AND STR_TO_DATE('"+ str(fin) +"', '%Y-%m-%dT%H:%i:%s+0000');"
    return query_comment

def get_post(inicio, fin):
    query_post = "SELECT id_post, message AS POSTS FROM post WHERE STR_TO_DATE(created_time, '%Y-%m-%dT%H:%i:%s+0000') BETWEEN STR_TO_DATE('"+ str(inicio) +"', '%Y-%m-%dT%H:%i:%s+0000') AND STR_TO_DATE('"+ str(fin) +"', '%Y-%m-%dT%H:%i:%s+0000');"
    return query_post

if __name__ == '__main__':
    connection = connect_db()
    cursor = get_cursor(connection)


    query_post = "SELECT id_post, message AS POSTS FROM post WHERE STR_TO_DATE(created_time, '%Y-%m-%dT%H:%i:%s+0000') BETWEEN "
    query_post2 = "STR_TO_DATE('2016-06-17T01:22:44+0000', '%Y-%m-%dT%H:%i:%s+0000') AND "
    query_post3 = "STR_TO_DATE('2016-06-17T04:01:30+0000', '%Y-%m-%dT%H:%i:%s+0000');"
    #query_comment = "SELECT message AS COMMENTS FROM comment WHERE id_post = %s AND STR_TO_DATE(created_time, '%Y-%m-%dT%H:%i:%s+0000') BETWEEN STR_TO_DATE('2016-06-17T01:22:44+0000', '%Y-%m-%dT%H:%i:%s+0000') AND STR_TO_DATE('2016-06-17T04:01:30+0000', '%Y-%m-%dT%H:%i:%s+0000');"
    query_comment = "SELECT message FROM comment WHERE id_post = %d AND STR_TO_DATE(created_time, '%Y-%m-%dT%H:%i:%s+0000') BETWEEN STR_TO_DATE('2016-06-17T01:22:44+0000', '%Y-%m-%dT%H:%i:%s+0000') AND STR_TO_DATE('2016-06-17T04:01:30+0000', '%Y-%m-%dT%H:%i:%s+0000');"

    inicio = '2016-06-26T00:24:34+0000'
    fin = '2016-06-26T03:50:36+0000'
    cursor.execute(get_post(inicio, fin))
    posts = cursor.fetchall()
    count = 0
    for post in posts:
        count = count + 1
        name = "post" + str(count) + ".txt"
        f = open(name, 'w')
        id_post = post[0]
        message = post[1]
        f.write(message+'\n')
        relation = (id_post)
        cursor.execute(get_comment(id_post, inicio, fin))
        comments = cursor.fetchall()
        for comment in comments:
            c_message = comment[0]
            f.write(c_message + '\n')
    f.close()


