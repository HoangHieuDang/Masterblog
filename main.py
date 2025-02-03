from flask import Flask, render_template
import os
import json

def get_blogposts_from_database():
    # Python Parse JSON
    with open("database.json", "r") as fileobj:
        data = json.load(fileobj)
        return data

app = Flask(__name__)

@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    blog_posts = get_blogposts_from_database()
    return render_template('index.html', posts = blog_posts)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
