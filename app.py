from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/topics')
def topics():
    topics = ['This is the first topic.',
                'This is the second topic.',
                'This is the third topic.',
                'This is the fourth topic.'
                ]
    return render_template('topics.html', topics=topics)


if __name__ == '__main__':
    app.run()
