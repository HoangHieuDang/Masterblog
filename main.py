from flask import Flask, render_template, request, redirect, url_for
import json


def get_blogposts_from_database():
    """
    Retrieve all blog posts from the database (JSON file).

    Returns:
        list: A list of dictionaries representing blog posts.
    """
    with open("database.json", "r") as fileobj:
        data = json.load(fileobj)
        return data


def add_blogpost_to_database(title, author, content):
    """
    Add a new blog post to the database.

    Args:
        title (str): The title of the blog post.
        author (str): The author of the blog post.
        content (str): The content of the blog post.
    """
    data = get_blogposts_from_database()
    max_id = max([blog_entry['id'] for blog_entry in data], default=0)
    new_data_entry = {"id": max_id + 1, "author": author, "title": title, "content": content, "likes": 0}
    data.append(new_data_entry)
    with open("database.json", "w") as fileobj:
        json.dump(data, fileobj, indent=4)


def delete_blogpost_from_database(post_id):
    """
    Delete a blog post from the database by its ID.

    Args:
        post_id (int): The ID of the blog post to be deleted.
    """
    data = get_blogposts_from_database()
    data = [blog_post for blog_post in data if blog_post['id'] != post_id]
    with open("database.json", "w") as fileobj:
        json.dump(data, fileobj, indent=4)


def update_blogpost_in_database(post_id, title, author, content):
    """
    Update an existing blog post in the database.

    Args:
        post_id (int): The ID of the blog post to be updated.
        title (str): The new title of the blog post.
        author (str): The new author of the blog post.
        content (str): The new content of the blog post.
    """
    data = get_blogposts_from_database()
    for blog_post in data:
        if blog_post['id'] == post_id:
            blog_post['title'] = title
            blog_post['author'] = author
            blog_post['content'] = content
    with open("database.json", "w") as fileobj:
        json.dump(data, fileobj, indent=4)


# Initialize the Flask application
app = Flask(__name__)


@app.route('/')
def index():
    """
    Render the homepage with all blog posts.

    Returns:
        str: Rendered HTML template with blog posts.
    """
    blog_posts = get_blogposts_from_database()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handle adding a new blog post.
    If the request method is POST, retrieve form data and add the post to the database.
    Otherwise, render the add post form.

    Returns:
        str: Redirects to index or renders add post form.
    """
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')
        add_blogpost_to_database(title, author, content)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """
    Delete a blog post and redirect to homepage.

    Args:
        post_id (int): ID of the blog post to delete.

    Returns:
        str: Redirects to index.
    """
    delete_blogpost_from_database(post_id)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Update an existing blog post. If method is POST, update post data.
    Otherwise, render update form with current post details.

    Args:
        post_id (int): ID of the blog post to update.

    Returns:
        str: Redirects to index or renders update form.
    """
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')
        update_blogpost_in_database(post_id, title, author, content)
        return redirect(url_for('index'))

    data = get_blogposts_from_database()
    for blog_post in data:
        if blog_post['id'] == post_id:
            return render_template('update_form.html', post=blog_post)

    return render_template('error.html', error_msg="Something went wrong while updating the post")


@app.route('/like/<int:post_id>')
def like(post_id):
    """
    Increment the like count for a blog post.

    Args:
        post_id (int): ID of the blog post to like.

    Returns:
        str: Redirects to index.
    """
    data = get_blogposts_from_database()
    for blog_post in data:
        if blog_post['id'] == post_id:
            blog_post['likes'] += 1
    with open("database.json", "w") as fileobj:
        json.dump(data, fileobj, indent=4)
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Run the Flask application
    app.run(host="0.0.0.0", port=5000, debug=True)
