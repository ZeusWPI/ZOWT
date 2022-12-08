from flask import Flask, render_template
import sys

from db import Mongo
db = Mongo()

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/topics')
def topics():
    # topics = [{'name': 'Wordt het belastingsgeld nuttig gebruikt?', 'id': "uuid1"},
    #           {'name': 'This is the second topic.', 'id': "uuid2"},
    #           {'name': 'This is the third topic.', 'id': "uuid3"},
    #           {'name': 'This is the fourth topic.', 'id': "uuid4"}]
    topics = db.get_topics()
    return render_template('topics.html', topics=topics)

@app.route('/topics/<topic_id>/comments')
def load_comments(topic_id):
    # comments = [{'value': 'This is the first comment.', 'id': "uuid1"},
    #           {'value': 'This is the second comment.', 'id': "uuid2"},
    #           {'value': 'This is the third comment.', 'id': "uuid3"},
    #           {'value': 'This is the fourth comment.', 'id': "uuid4"}]
    comments = db.get_comments(topic_id)
    # todo get topic name through topic id
    return render_template('comments.html', comments=comments, topic_name=db.get_topic(topic_id)["name"])
#app.jinja_env.globals.update(load_topic=load_topic)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
