from flask import Flask, render_template, request
import sys

from db import Mongo
db = Mongo()

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/topics')
def topics():
    topics = db.get_topics()
    return render_template('topics.html', topics=topics)

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
    dummyuserid = db.get_users()[0]["_id"]
    db.add_comment(topic_id, dummyuserid, request.form['content'])
    return load_comments(topic_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
