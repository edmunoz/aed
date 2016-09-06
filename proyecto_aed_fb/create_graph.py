import MySQLdb as mdb
import networkx as nx
import matplotlib.pyplot as plt
import community


def connect_db():
    connection = mdb.connect('108.167.133.34', 'connie_usr_aed', 'SK5CTTs8zXV9', 'connie_facebook')
    return connection


def get_cursor(connect):
    cursor = connect.cursor()
    return cursor


def get_post(inicio, fin):
    query_post = "SELECT id_post AS POSTS FROM post WHERE STR_TO_DATE(created_time, '%Y-%m-%dT%H:%i:%s+0000') BETWEEN STR_TO_DATE('"+ str(inicio) +"', '%Y-%m-%dT%H:%i:%s+0000') AND STR_TO_DATE('"+ str(fin) +"', '%Y-%m-%dT%H:%i:%s+0000');"
    return query_post


def get_comment(id, inicio, fin):
    query_comment = "SELECT DISTINCT cf.id FROM comment as c INNER JOIN comment_from as cf ON c.id_comment = cf.id_comment WHERE c.id_post = " + str(id) + " AND STR_TO_DATE(c.created_time, '%Y-%m-%dT%H:%i:%s+0000') BETWEEN STR_TO_DATE('"+ str(inicio) +"', '%Y-%m-%dT%H:%i:%s+0000') AND STR_TO_DATE('"+ str(fin) +"', '%Y-%m-%dT%H:%i:%s+0000');"
    return query_comment


def get_communities(partition, list_posts):
    for item in list_posts:
        for key, value in partition.items():
            if value == item:
                print "Escriir"

if __name__ == '__main__':
    '''
    inicio = '2016-06-17T01:22:44+0000' fin = '2016-06-17T04:01:30+0000'#EEUU_VS_Ecuador
    inicio = '2016-06-17T23:42:20+0000' fin = '2016-06-18T02:55:17+0000'#Colombia_VS_Peru
    inicio = '2016-06-19T01:26:00+0000' fin = '2016-06-19T04:23:23+0000'#Mexico_VS_Chile
    inicio = '2016-06-22T02:02:20+0000' fin = '2016-06-22T04:20:43+0000'#EEUU_VS_Argentina
    inicio = '2016-06-22T23:40:45+0000' fin = '2016-06-23T05:12:30+0000'#Chile_VS_Colombia
    inicio = '2016-06-26T00:24:34+0000' fin = '2016-06-26T03:50:36+0000'#EEUU_VS_Colombia
    inicio = '2016-06-26T23:24:26+0000' fin = '2016-06-27T05:42:49+0000'#Argentina_VS_Chile
    '''
    inicio = '2016-06-19T01:26:00+0000'
    fin = '2016-06-19T04:23:23+0000'  # Mexico_VS_Chile

    connection = connect_db()
    cursor = get_cursor(connection)
    cursor.execute(get_post(inicio, fin))
    posts = cursor.fetchall()
    grafo = nx.Graph()
    list_posts = list()
    list_comments = list()
    my_edges = list()
    parada = 0
    for post in posts:
        parada += 1
        id_post = post[0]
        #print id_post
        #list_posts.append(id_post)
        grafo.add_node(id_post)
        cursor.execute(get_comment(id_post, inicio, fin))
        comments_users = cursor.fetchall()
        for comment_user in comments_users:
            id_user = comment_user[0]
            #list_comments.append(id_user)
            #valor = (id_post, id_user)
            #my_edges.append(valor)
            grafo.add_node(id_user)
            grafo.add_edge(id_post, id_user)
        #if parada == 100:
        #    break
    #nx.draw(grafo)
    #pos = nx.spring_layout(grafo)
    #nx.draw_networkx_nodes(grafo, pos, nodelist=list_posts, node_color='r')
    #nx.draw_networkx_nodes(grafo, pos, nodelist=list_comments, node_color='c')
    #nx.draw_networkx_edges(grafo, pos, edgelist=my_edges, edge_color='r')
    parts = community.best_partition(grafo)
    values = [parts.get(node) for node in grafo.nodes()]
    nx.draw_spring(grafo, node_color=values, with_labels=False)
    '''
    for item in list_posts:
        ssss = parts[item]
        for key, value in parts.items():
            if value == ssss:
                print "Escriir"'''



    print nx.info(grafo)
    plt.axis('off')
    plt.show()

