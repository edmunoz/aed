import MySQLdb as mdb
import networkx as nx
import matplotlib.pyplot as plt


def connect_db():
    connection = mdb.connect('108.167.133.34', 'connie_usr_aed', 'SK5CTTs8zXV9', 'connie_facebook')
    connection.set_character_set('utf8mb4')
    return connection


def get_cursor(connect):
    cursor = connect.cursor()
    cursor.execute('SET NAMES utf8mb4;')
    cursor.execute('SET CHARACTER SET utf8mb4;')
    cursor.execute('SET character_set_connection=utf8mb4;')
    return cursor


def get_post(inicio, fin):
    query_post = "SELECT id_post AS POSTS FROM post WHERE STR_TO_DATE(created_time, '%Y-%m-%dT%H:%i:%s+0000') BETWEEN STR_TO_DATE('"+ str(inicio) +"', '%Y-%m-%dT%H:%i:%s+0000') AND STR_TO_DATE('"+ str(fin) +"', '%Y-%m-%dT%H:%i:%s+0000');"
    return query_post


def get_comment(id, inicio, fin):
    query_comment = "SELECT cf.id FROM comment as c INNER JOIN comment_from as cf ON c.id_comment = cf.id_comment WHERE c.id_post = " + str(id) + " AND STR_TO_DATE(c.created_time, '%Y-%m-%dT%H:%i:%s+0000') BETWEEN STR_TO_DATE('"+ str(inicio) +"', '%Y-%m-%dT%H:%i:%s+0000') AND STR_TO_DATE('"+ str(fin) +"', '%Y-%m-%dT%H:%i:%s+0000');"
    return query_comment


if __name__ == '__main__':
    inicio = '2016-06-17T01:22:44+0000'
    fin = '2016-06-17T04:01:30+0000'
    connection = connect_db()
    cursor = get_cursor(connection)
    cursor.execute(get_post(inicio, fin))
    posts = cursor.fetchall()
    grafo = nx.Graph()
    for post in posts:
        id_post = post[0]
        grafo.add_node(id_post)
        cursor.execute(get_comment(id_post, inicio, fin))
        comments_users = cursor.fetchall()
        for comment_user in comments_users:
            id_user = comment_user[0]
            grafo.add_node(id_user)
            grafo.add_edge(id_post, id_user)
    nx.draw(grafo)
    plt.draw()
    plt.show()

