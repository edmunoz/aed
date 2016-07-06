import facebook
import urllib2
import json
import mysql.connector

def connect_db():
    #fill this out with your db connection info
    connection = mysql.connector.connect(user='JohnDoe',
                                         password='abc123',
                                         host = '127.0.0.1',
                                         database='facebook_data')
    return connection

def printAllComments(comments, next_url):
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
            print "****************************************************"
            print from_name
        url = comments['paging']['next']
        printAllComments('', url)
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
                print "****************************************************"
                print from_name
            url = response_data['paging']['next']
            printAllComments('', url)
        except Exception:
            print "Done collecting"



if __name__ == "__main__":
    accessToken = 'EAACEdEose0cBAAkCZBieZCmFWOykmzaKYetTtGimiq69V4DJLSO9rDZAEYoxM4q8Rlur0DiGFEXrZBAO3v1zgLH0PlupHO37To7dkQD3GNbPscKzuETx4c49IgxCrHFUZCZBSSNGOG6rApqs2a18QEePZAJyWQe1Tq0zhxomCBmugZDZD'
    graph = facebook.GraphAPI(access_token=accessToken, version='2.2')
    post = graph.get_object(id='789150404520214')
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
    printAllComments(comments, '')