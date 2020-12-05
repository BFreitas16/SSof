from flask_mysqldb import MySQL
from __init__ import app, mysql
from views import error

import logging
logging.basicConfig(level=logging.DEBUG)

# fetchall, fetchmany(), fetchone()

# INIT DB
def init_db():
    cur = mysql.connection.cursor()
    cur.execute("DROP DATABASE IF EXISTS %s;" % app.config['MYSQL_DB'])
    cur.execute("CREATE DATABASE %s;" % app.config['MYSQL_DB'])
    cur.execute("USE %s;" % app.config['MYSQL_DB'])
    cur.execute("DROP TABLE IF EXISTS Users;")
    cur.execute('''CREATE TABLE Users ( 
                    username VARCHAR(20) NOT NULL,
                    password VARCHAR(255) NOT NULL, 
                    name TEXT,
                    about TEXT, 
                    photo varchar(255) DEFAULT '{}',
                    PRIMARY KEY (username)
                    );'''.format(app.config['default_photo']))
    cur.execute("INSERT INTO Users(username, password, name, about) VALUES (%s, %s, %s, %s)", ('administrator', 'ae1c7454615ab0c074c6ff3d1ccba90ded5ef517ee48162a654e179d', "Admin", "I have no friends."))
    cur.execute("INSERT INTO Users(username, password, name) VALUES (%s, %s, %s)", ('investor', 'e627b59480327a9500ba22392725c36c1425139501bfca07affa1b19', "Mr. Smith"))
    cur.execute("INSERT INTO Users(username, password, name, about) VALUES (%s, %s, %s, %s)", ('ssofadmin', '5f86d097eabe909d63727a3396cc5bebb44be8b57e9603cdfd696031', "SSofAdmin", "A 12-year experienced sys-admin that has developed and secured this application."))
    cur.execute("DROP TABLE IF EXISTS Posts;")
    cur.execute('''CREATE TABLE Posts ( 
                    id int(11) NOT NULL AUTO_INCREMENT,
                    author VARCHAR(20) NOT NULL,
                    content TEXT,
                    type ENUM ('Public','Private','Friends') DEFAULT 'Public',
                    created_at timestamp default now(),
                    updated_at timestamp default now() ON UPDATE now(),
                    PRIMARY KEY (id),
                    FOREIGN KEY (author) REFERENCES Users(username)
                    );''')
    cur.execute("INSERT INTO Posts(author, content, type) VALUES (%s, %s, %s)", ('administrator', 'No one will find that I have no secrets.', "Private"))
    cur.execute("INSERT INTO Posts(author, content, type) VALUES (%s, %s, %s)", ('investor', 'This is a great platform', "Public"))
    cur.execute("INSERT INTO Posts(author, content, type) VALUES (%s, %s, %s)", ('investor', 'Lets keep it for us but I believe that after this app Instagram is done', "Friends"))
    cur.execute("INSERT INTO Posts(author, content, type) VALUES (%s, %s, %s)", ('investor', 'TikTok might also be done but do not want ot make this bold claim in Public', "Private"))
    cur.execute("INSERT INTO Posts(author, content, type) VALUES (%s, %s, %s)", ('SSofAdmin', 'There are no problems with this app. It works perfectly', "Public"))
    cur.execute("INSERT INTO Posts(author, content, type) VALUES (%s, %s, %s)", ('SSofAdmin', 'Cannot put this app running. Can any of my friends help me', "Friends"))
    cur.execute("INSERT INTO Posts(author, content, type) VALUES (%s, %s, %s)", ('SSofAdmin', 'Just found a great new thing. Have a look at it. It might be of help. https://www.guru99.com/install-linux.html', "Public"))
    cur.execute("INSERT INTO Posts(author, content, type) VALUES (%s, %s, %s)", ('SSofAdmin', 'This one is also great. https://www.youtube.com/watch?v=oHg5SJYRHA0&', "Public"))
    cur.execute("DROP TABLE IF EXISTS Friends;")
    cur.execute('''CREATE TABLE Friends ( 
                    id int(11) NOT NULL AUTO_INCREMENT,
                    username1 VARCHAR(20) NOT NULL,
                    username2 VARCHAR(20) NOT NULL,
                    PRIMARY KEY (id),
                    FOREIGN KEY (username1) REFERENCES Users(username),
                    FOREIGN KEY (username2) REFERENCES Users(username)
                    );''')
    cur.execute("INSERT INTO Friends(username1, username2) VALUES (%s, %s)", ('investor', "SSofAdmin"))
    cur.execute("DROP TABLE IF EXISTS FriendsRequests;")
    cur.execute('''CREATE TABLE FriendsRequests ( 
                    id int(11) NOT NULL AUTO_INCREMENT,
                    username1 VARCHAR(20) NOT NULL,
                    username2 VARCHAR(20) NOT NULL,
                    PRIMARY KEY (id),
                    FOREIGN KEY (username1) REFERENCES Users(username),
                    FOREIGN KEY (username2) REFERENCES Users(username)
                    );''')
    cur.execute("INSERT INTO Users(username, password, name, about) VALUES (%s, %s, %s, %s)", ('randomjoe1', '300d01f3a910045fefa16d6a149f38167b2503dbc37c1b24fd6f751e', "Random Joe Smith1", "I am the real Random Joe"))
    cur.execute("INSERT INTO Users(username, password, name) VALUES (%s, %s, %s)", ('randomjoe2', 'f3ff4f073ed24d62051c8d7bb73418b95db2f6ff9e4441af466f6d98', "Random Joe Smith2"))
    cur.execute("INSERT INTO Users(username, password, name) VALUES (%s, %s, %s)", ('randomjoe3', 'b6f194539618d1e5eec08a56b8c7d09b8198fe1faa3f16e9703b91bd', "Random Joe Smith3"))
    cur.execute("INSERT INTO Users(username, password, name) VALUES (%s, %s, %s)", ('randomjoe4', '51bbf7daffa13cd37d2517dd38b1be95b200053bd4e36492b5566bda', "Random Joe Smith4"))
    cur.execute("INSERT INTO FriendsRequests(username1, username2) VALUES (%s, %s)", ('randomjoe1', "investor"))
    cur.execute("INSERT INTO FriendsRequests(username1, username2) VALUES (%s, %s)", ('randomjoe2', "investor"))
    cur.execute("INSERT INTO FriendsRequests(username1, username2) VALUES (%s, %s)", ('randomjoe3', "investor"))
    cur.execute("INSERT INTO FriendsRequests(username1, username2) VALUES (%s, %s)", ('randomjoe4', "investor"))
   
    mysql.connection.commit()
    cur.close()


 # SELECT QUERIES -- Probably deleted in the end
#def get_all_resultsProf(q):
 #   cur = mysql.connection.cursor()
 #   cur.execute(q)
 #   mysql.connection.commit()
 #   data = cur.fetchall()
 #   cur.close()
#    return data

# # UPDATE and INSERT QUERIES -- Probably deleted in the end
# def commit_results(q):
#     cur = mysql.connection.cursor()
#     cur.execute(q)
#     mysql.connection.commit()
#     cur.close()

# PREPARED SELECT QUERIES
def get_all_results(query_statement, query_args):
    cur = mysql.connection.cursor()
    cur.execute(query_statement, query_args)
    mysql.connection.commit()
    data = cur.fetchall()
    cur.close()
    return data

# PREPARED UPDATE AND INSERT QUERIES
def commit_results(query_statement, query_args):
    cur = mysql.connection.cursor()
    cur.execute(query_statement, query_args)
    mysql.connection.commit()
    cur.close()


##### Returns a user for a given username
### in: username
### out: User
def get_user(username):
    q = """
            SELECT * FROM Users 
            WHERE username = %s
        """

    logging.debug("get_user query: %s" % q)
    data = get_all_results(q, (username, ))

    if len(data) == 1:
        user = User(*(data[0]))
        return user
    else:
        logging.debug("get_user: Something wrong happened with (username):(%s)" % (username))
        return None


##### Returns a user for a given pair username:password
### in: username, password
### out: User
def login_user(username, password):
    q = """
            SELECT * FROM Users
            WHERE username = %(username)s
            AND password = %(password)s
        """
    
    q_args = {
        'username': username,
        'password': password
    }

    logging.debug("login_user query: %s \nwith args: %s" % (q, q_args))
    data = get_all_results(q, q_args,)

    if len(data) == 1:
        user = User(*(data[0]))
        return user
    else:
        logging.debug("login_user: Something wrong happened with (username, password):(%s %s)" % (username, password))
        return None


##### Registers a new user with a given pair username:password
### in: username, password
### out: User
def register_user(username, password):
    q = """
            INSERT INTO Users (username, password)
            VALUES (%s, %s)
        """

    logging.debug("register_user query: %s" % q)
    commit_results(q, (username, password))
    return User(username, password)


##### Updates a user with the given characteristics
### in: username, new_name, new_password, new_about, new_photo
### out: User
def update_user(username, new_name, new_password, new_about, new_photo):
    q = """
            UPDATE Users
            SET username=%s, password=%s, name=%s, about=%s, photo=%s
            WHERE username = %s
        """

    logging.debug("update_user query: %s" % q)
    commit_results(q, (username, new_password, new_name, new_about, new_photo, username))
    return User(username, new_password, new_name, new_about, new_photo)
    

##### Creates a new post
### in: username, new_content, type
### out: True
def new_post(username, new_content, post_type):
    q = """
            INSERT INTO Posts (author, content, type)
            VALUES (%s, %s, %s)
        """

    logging.debug("new_post query: %s" % q)
    commit_results(q, (username, new_content, post_type))
    return True


##### Gets the post with the given post_id
### in: post_id
### out: Post
def get_post(post_id):
    q = """
            SELECT * FROM Posts
            WHERE id = %s
        """

    logging.debug("get_post query: %s" % q)
    data = get_all_results(q, (post_id,))

    if len(data) == 1:
        post = Post(*(data[0]))
        return post
    else:
        logging.debug("get_post: Something wrong happened with (post_id):(%d)" % (post_id))
        return None


##### Edits the post with the given post_id
### in: post_id, new_content, type
### out: True
def edit_post(post_id, new_content, post_type):
    q = """
            UPDATE Posts
            SET content=%s, type=%s
            WHERE id = %s
        """

    logging.debug("edit_post query: %s" % q)
    commit_results(q, (new_content, post_type, post_id,))
    return True


##### Returns all posts of a user, from his friends, or public
### in: username
### out: List of Posts_to_show
def get_all_posts(username):
    q = """
            SELECT Posts.id, Users.username, Users.name, Users.photo, Posts.content, Posts.type, Posts.created_at
            FROM Users INNER JOIN Posts
            ON Users.username = Posts.author
            WHERE Posts.author = %s
            OR (Posts.type = 'Public')
            OR (
                Posts.type = 'Friends' AND Posts.author IN (
                    SELECT username1 from Friends WHERE username2 = %s
                    UNION SELECT username2 from Friends WHERE username1 = %s
                )
            )
        """

    logging.debug("get_all_posts query: %s" % q)
    data = get_all_results(q, (username, username, username,))
    posts_to_show = []

    for x in data:
        posts_to_show.append(Post_to_show(*x))

    logging.debug("get_all_posts: %s" % (posts_to_show))
    return posts_to_show


##### Creates a new friend request
### in: username (requester), username (new_friend)
### out: True
def new_friend_request(username, new_friend):
    q = """
            INSERT INTO FriendsRequests (username1, username2)
            VALUES (%(username)s, %(new_friend)s)
        """

    q_args = {
        'username': username,
        'new_friend': new_friend
    }

    logging.debug("new_friend_request query: %s\nwith args:%s" % (q, q_args))
    commit_results(q, q_args)
    return True


##### Checks if there is a friend request pending
### in: username (requester), username (new_friend)
### out: data
def is_request_pending(requester, username):
    q = """
            SELECT username1 
            FROM FriendsRequests
            WHERE username1 = %s
            AND username2 = %s
        """
    
    logging.debug("is_request_pending query: %s" % q)
    data = get_all_results(q, (requester, username,))
    return data


#### Returns pending friendship requests for the user
### in: username (new_friend)
### out: List of Users
def get_pending_requests(username):
    q = """
            SELECT * 
            FROM Users
            WHERE username IN (
                SELECT username1 
                FROM FriendsRequests
                WHERE username2 = %s
            )
        """
    
    logging.debug("get_pending_requests query: %s" % q)
    data = get_all_results(q, (username,))
    users = []

    for x in data:
        users.append(User(*x))

    logging.debug("get_pending_requests: %s" % (users))
    return users


##### Accepts a pending friendship requests for the user
### in: username, accept_friend (requester)
### out: True
def accept_friend_request(username, accept_friend):
    q = """
            INSERT INTO Friends (username1, username2)
            VALUES (%s, %s);
        """
    
    logging.debug("accept_friend_request query1: %s" % q)
    cur = mysql.connection.cursor()
    cur.execute(q, (accept_friend, username))

    q = """
            DELETE FROM FriendsRequests
            WHERE username1=%s AND username2=%s;
        """

    logging.debug("accept_friend_request query2: %s" % q)
    cur.execute(q, (accept_friend, username))
    mysql.connection.commit()

    cur.close()
    return True


##### Returns all friends of user that match the search query
### in: username, search_query
### out: List of Users
#def get_friends(username, search_query):
#    q = """
#            SELECT * FROM Users
#            WHERE username LIKE %(search_query)s
#            AND username IN (
#                SELECT username1 FROM Friends
#                WHERE username2 = %(username2)s
#                UNION SELECT username2 FROM Friends
#                WHERE username1 = %(username1)s
#            )
#        """
#
#    q_args = {
#        'search_query': '%' + search_query + '%',
#        'username2': username, 
#        'username1': username
#    }
#
#    logging.debug("get_friends query: %s\nwith args:%s" % (q, q_args))
#    data = get_all_results(q, q_args,)
#    friends = []
#
#    for x in data:
#        friends.append(User(*x))
#
#    logging.debug("get_friends: %s" % (friends))
#    return friends


def get_friends(username, search_query):
    q = "SELECT * FROM Users"
    q+= " WHERE username LIKE '%%%s%%'" % (search_query)
    q+= " AND username IN" 
    q+= " (SELECT username1 FROM Friends"
    q+= "  WHERE username2 = '%s'" % (username)
    q+= "  UNION SELECT username2 FROM Friends"
    q+= "  WHERE username1 = '%s')" % (username)

    logging.debug("get_friends query: %s" % q)
    data = get_all_results(q)
    friends = []

    for x in data:
        friends.append(User(*x))

    logging.debug("get_friends: %s" % (friends))
    return friends


##### Returns the usernames of all friends of user
### in: username
### out: List of usernames
def get_friends_aux(username):
    q = """
            SELECT username2 FROM Friends
            WHERE username1 = %(username1)s
            UNION
            SELECT username1 FROM Friends
            WHERE username2 = %(username2)s
        """
    
    q_args = {
        'username2': username, 
        'username1': username
    }

    logging.debug("get_friends_aux query: %s\nwith args:%s" % (q, q_args))
    data = get_all_results(q, q_args,)
    friends = []

    for x in data:
        friends.append(x[0])

    logging.debug("get_friends_aux query: %s" % q)
    return friends


##### class User
class User():
    def __init__(self, username, password, name='', about='', photo=''):
        self.username = username
        self.password = password # @TODO: Hash me! PLEASE!
        self.name = name
        self.about = about
        self.photo = photo
    
    def __repr__(self):
        return '<User: username=%s, password=%s, name=%s, about=%s, photo=%s>' % (self.username, self.password, self.name, self.about, self.photo)


##### class Post
class Post():
    def __init__(self, id, author, content, type, created_at, updated_at):
        self.id = id
        self.author = author
        self.content = content
        self.type = type
        self.created_at = created_at
        self.updated_at = updated_at
    
    def __repr__(self):
        return '<Post: id=%s, author=%s, content=%s, type=%s, created_at=%s, updated_at=%s>' % (self.id, self.author, self.content, self.type, self.created_at, self.updated_at)


##### class Post_to_show (includes Users and Posts information)
class Post_to_show():
    def __init__(self, id, author, name, photo, content, type, created_at):
        self.id = id
        self.author = author
        self.name = name
        self.photo = photo
        self.content = content
        self.type = type
        self.created_at = created_at
        
    def __repr__(self):
        return '<Post_to_show: id=%d, author=%s, name=%s, photo=%s, content=%s, type=%s, created_at=%s>' % (self.id, self.author, self.name, self.photo, self.content, self.type, self.created_at)

