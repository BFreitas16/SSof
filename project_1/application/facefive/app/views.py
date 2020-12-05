from flask import render_template, request, session, redirect, url_for, flash, make_response, escape
from flask_mysqldb import MySQL
import random, string
import html
import sha3

from __init__ import app, mysql, current_user
import model

import logging
logging.basicConfig(level=logging.DEBUG)

@app.before_request
def filter_scanner_boys():
    user_agent = request.headers.get('User-Agent')
    if "sqlmap" in user_agent:
        return abort(404)


##### auxiliar to render errors
def error(msg):
   return render_template('error_response.html', msg = msg)


##### initializes db
@app.route('/init', methods=['GET', 'POST'])
def init():
   model.init_db()
   flash("Initialisation DONE!", 'error')
   return redirect(url_for('login'))


##### home
### shows all posts if user is logged in
### redirects to login otherwise
@app.route('/')
def home():
   if 'username' in session:
      username = session['username']
      user = model.get_user(username)
      logging.debug("user in homepage: (%s)" % current_user)
      try:
         posts_to_show = model.get_all_posts(username)
      except Exception as e:
         logging.debug("home: Found exception(%s)" % e)
         return error(e)

      if user and current_user:
         return render_template('home.html', current_user=current_user, posts=posts_to_show)
   return redirect(url_for('login'))


##### login user
### in[POST]: username, password
### redirects to home if login is succesful
### redirects to login otherwise
@app.route('/login', methods=['GET', 'POST'])
def login():
   global current_user

   if request.method == 'GET':
      return render_template('login.html')

   username = html.escape(request.form['username'])
   password = hashPassword(html.escape(request.form['password']))
   logging.debug("login: Trying (%s, %s)" % (username, password))

   if username == "" or password == "":
      flash("You need to provide a 'username' and a 'password' to login.", 'error')
      return redirect(url_for('login'))

   try:
      user = model.login_user(username, password)
   except Exception as e:
      logging.debug("login: Found exception(%s)" % e)
      return error(e)
   
   if not user:
      flash('Username or Password are invalid', 'error')
      return redirect(url_for('login'))

   logging.debug("login: Succesfull (%s, %s)" % (username, password))
   session['username'] = username
   current_user = user
   return redirect(url_for('home'))


##### register a new user
### in[POST]: username, password
### redirects to home if registration is succesful
### redirects to register otherwise
@app.route('/register', methods=['GET', 'POST'])
def register():
   global current_user

   if request.method == 'GET':
      return render_template('register.html')

   username = html.escape(request.form['username'])
   password = hashPassword(html.escape(request.form['password']))
   logging.debug("register: Trying (%s, %s)" % (username, password))

   if username == "" or password == "":
      flash("You need to provide a 'username' and a 'password' to register.", 'error')
      return redirect(url_for('register'))

   try:
      user = model.get_user(username)
   except Exception as e:
      logging.debug("register1: Found exception(%s)" % e)
      return error(e)

   if user:
      flash("User '%s' already exists." % user.username, 'error')
      return redirect(url_for('register'))

   try:
      user = model.register_user(username, password)
   except Exception as e:
      logging.debug("register2 Found exception(%s)" % e)
      return error(e)
   
   logging.debug("register: Succesfull (%s, %s)" % (username, password))
   session['username'] = username
   current_user = user
   return redirect(url_for('home'))


##### logout
### removes the username from the session if it is there
@app.route('/logout')
def logout():
   global current_user

   session.pop('username', None)
   current_user = None
   return redirect(url_for('home'))

   
##### show the user profile
### in[GET]: username
### shows the user profile if user is logged in
### redirects to login otherwise
@app.route('/profile', methods=["GET"])
def profile():
   if 'username' in session:
      username = session['username']
      current_user = model.get_user(username)
      if current_user:
         return render_template('profile.html', current_user=current_user)
   return redirect(url_for('login'))


##### update user profile
### in[POST]: username, name, about, photo, current_password, new_password
### updates the user profile
### redirects to profile
@app.route('/update_profile', methods=["POST"])
def update_profile():
   global current_user
   
   if 'username' in session:
      username = session['username']
      current_user = model.get_user(username)

   logging.debug("update_profile: Trying (%s)" % (username))

   if current_user.username == "administrator":
      flash("Profile updating has been disabled for user admin.", 'error')
      return render_template('profile.html', current_user=current_user)

   new_name = html.escape(request.form['name'])
   if not new_name:
      new_name = current_user.name
   
   new_about = html.escape(request.form['about'])
   if new_name == 'None':
      new_about = None
   
   new_photo = request.files['photo']
   if not new_photo:
      new_photo_filename = current_user.photo
   else:
      new_photo_filename = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '_' + new_photo.filename
      new_photo_filename = html.escape(new_photo_filename)
      new_photo.save(app.config['photos_folder'] + new_photo_filename)

      logging.debug("update_profile: filename (%s)" % new_photo_filename)
      logging.debug("update_profile: file (%s)" % new_photo)
   
   current_password = hashPassword(html.escape(request.form['currentpassword']))
   
   new_password = hashPassword(html.escape(request.form['newpassword']))
   if not new_password:
      new_password = current_password

   if current_password != current_user.password:
      flash("Current password does not match registered password.", 'error')
      return render_template('profile.html', current_user=current_user)

   try:
      current_user = model.update_user(username, new_name, new_password, new_about, new_photo_filename)
   except Exception as e:
      logging.debug("update_profile: Found exception(%s)" % e)
      return error(e)

   logging.debug("update_profile: Succesful (%s)" % (username))

   if current_user:
      flash("Succesfully updated user %s profile" % username,)
      return render_template('profile.html', current_user=current_user)


##### create a new post
### in[POST]: content, type
### creates new post for user
### redirects to home
@app.route('/create_post', methods=["GET", "POST"])
def create_post():
   if 'username' in session:
      username = session['username']
      current_user = model.get_user(username)

   if request.method == 'GET':
      return render_template('create_post.html', current_user=current_user)

   new_content = html.escape(request.form['content'])
   type = html.escape(request.form['type'])

   logging.debug("create_post: Trying (%s, %s, %s)" % (username, new_content, type))

   if not new_content:
      flash("You need to introduce some content.", 'error')
      return render_template('create_post.html', current_user=current_user)

   try:
      new_post = model.new_post(username, new_content, type)
   except Exception as e:
      logging.debug("create_post: Found exception(%s)" % e)
      return error(e)
   
   if new_post:
      flash("Succesfully created new post",)
      logging.debug("create_post: Succesful (%s)" % (username))
   else:
      flash("Could not create new post",)

   return redirect(url_for('home'))


##### edit an existing post
### in[GET]: post_id
### shows current content of post with given id
### in[POST]: content, type, id
### edits post with given id. redirects to home
@app.route('/edit_post', methods=["GET", "POST"])
def edit_post():
   if 'username' in session:
      username = session['username']
      current_user = model.get_user(username)

   if request.method == 'GET':
      post_id = request.args.get('id')
      try:
         post = model.get_post(post_id)
      except Exception as e:
         logging.debug("edit_post1: Found exception(%s)" % e)
         return error(e)
      return render_template('edit_post.html', current_user=current_user, post=post)

   new_content = html.escape(request.form['content'])
   new_type = html.escape(request.form['type'])
   post_id = html.escape(request.form['id'])

   logging.debug("edit_post: Trying (%s, %s)" % (new_content, new_type))

   if not new_content:
      flash("You need to introduce some content.", 'error')
      return render_template('edit_post.html', current_user=current_user, post=post)

   try:
      new_post = model.edit_post(post_id, new_content, new_type)
   except Exception as e:
      logging.debug("edit_post2: Found exception(%s)" % e)
      return error(e)
   
   if new_post:
      flash("Succesfully edited post",)
      logging.debug("edit_post: Succesful (%s)" % (username))
   else:
      flash("Could not edit post",)

   return redirect(url_for('home'))


##### request a new friendship
### in[POST]: username
### adds a new friendship request
### redirects to home
@app.route('/request_friend', methods=["GET", "POST"])
def request_friend():
   if 'username' in session:
      username = session['username']
      current_user = model.get_user(username)

   if request.method == 'GET':
      return render_template('request_friend.html', current_user=current_user)

   new_friend = html.escape(request.form['username'])
   logging.debug("request_friend: Trying (%s, %s)" % (username, new_friend))

   ### missing handling exception
   if not new_friend or not model.get_user(new_friend) or new_friend == username:
      flash("Introduce an existing username different from yours.", 'error')
      return render_template('request_friend.html', current_user=current_user)

   ### missing handling exception
   if new_friend in model.get_friends_aux(username) or model.is_request_pending(new_friend, username):
      flash("%s is already your friend, or a request from him is pending." % new_friend, 'error')
      return render_template('request_friend.html', current_user=current_user)

   try:
      new_request = model.new_friend_request(username, new_friend)
   except Exception as e:
      logging.debug("request_friend: Found exception(%s)" % e)
      return error(e)


   if new_request:
      flash("Succesfully created friend request to %s" % new_friend,)
      logging.debug("request_friend: Succesful (%s)" % (username))
   else:
      flash("Could not create friend request to %s" % new_friend,)

   return redirect(url_for('home'))


##### accept a friendship request
### in[POST]: username
### accepts the friendship request
### redirects to home
@app.route('/pending_requests', methods=["GET", "POST"])
def pending_requests():
   if 'username' in session:
      username = session['username']
      current_user = model.get_user(username)

   logging.debug("pending_requests: (%s)" % (current_user))

   try:
      friends_pending = model.get_pending_requests(username)
   except Exception as e:
      logging.debug("pending_requests1: Found exception(%s)" % e)
      return error(e)

   if request.method == 'GET':
      return render_template('pending_requests.html', current_user=current_user, friends_pending=friends_pending)

   accept_friend = html.escape(request.form['username'])

   if not accept_friend or not model.is_request_pending(accept_friend, username):
      flash("Introduce an existing friend request.", 'error')
      return render_template('pending_requests.html', current_user=current_user, friends_pending=friends_pending)

   try:
      new_friend = model.accept_friend_request(username, accept_friend)
   except Exception as e:
      logging.debug("pending_requests1: Found exception(%s)" % e)
      return error(e)

   logging.debug("pending_requests: Accepted %s:%s" % (username, accept_friend))
   
   if new_friend:
      flash("Succesfully accepted friend request of %s" % accept_friend,)
   else:
      flash("Could not accept friend request from %s" % accept_friend,)

   return redirect(url_for('home'))


##### show user's friends
### in[GET]: search_query
### searchs user's friends that match the search query
@app.route('/friends', methods=["GET"])
def friends():
   if 'username' in session:
      username = session['username']
      current_user = model.get_user(username)

   logging.debug("friends: current_user: %s" % (current_user))
   
   search_query = request.args.get('search', default = "")

   try:
      friends = model.get_friends(username, search_query)
   except Exception as e:
      logging.debug("friends: Found exception(%s)" % e)
      return error(e)

   return render_template('friends.html', current_user=current_user, friends=friends)

#def hashPassword(password):
#   m = hashlib.sha256()
#   m.update(password.encode("utf-8"))
#   return m.digest().decode("utf-8", "ignore")


def hashPassword(password):
   return '' if password == '' else sha3.sha3_224(password.encode('utf-8')).hexdigest()
    