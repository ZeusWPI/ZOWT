from flask import Flask, render_template, request
import sass
import sys

from db import Mongo
db = Mongo()

app = Flask(__name__)

sass.compile(dirname=('/assets/', '/static/'))

@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/topics', methods=["GET"])
def topics():
    topics = db.get_topics()
    return render_template('topics.html', topics=topics)

@app.route('/topics', methods=["POST"])
def add_topic():
    db.add_topic(request.form["title"])
    return topics()

@app.route('/topics/<topic_id>/comments', methods=["GET"])
def load_comments(topic_id):
    # some cursed code lol
    comments = []
    # add usernames to comments
    for comment in db.get_comments(topic_id):
        comment["username"] = db.get_user(comment["user_id"])["name"]
        comments.append(comment)

    return render_template('comments.html', comments=comments, topic=db.get_topic(topic_id))

@app.route('/topics/<topic_id>/comments', methods=["POST"])
def post_comment(topic_id):
    # todo: when zauth added get userid from cookie
    user_id = db.get_users()[0]["_id"]

    # delete existing comment so the new one replaces it
    maybe_comment = [comment for comment in db.get_comments(topic_id) if comment["user_id"] == f"{user_id}"]
    if maybe_comment:
        db.delete_comment(maybe_comment[0]["_id"])

    db.add_comment(topic_id, user_id, request.form['content'])
    return load_comments(topic_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
