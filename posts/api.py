import json

from flask import request, Response, url_for
from jsonschema import validate, ValidationError

from . import models
from . import decorators
from posts import app
from .database import session

@app.route("/api/posts", methods=["GET"])
@decorators.accept("application/json")
def posts_get():
    """ Get a list of posts """

    # Get the posts from the database
    posts = session.query(models.Post).order_by(models.Post.id)

    # Convert the posts to JSON and return a response
    data = json.dumps([post.as_dictionary() for post in posts])
    return Response(data, 200, mimetype="application/json")

@app.route("/api/posts/<int:id>", methods=["GET"])
@decorators.accept("application/json")
def post_get(id):
    """ Single post endpoint """
    # Get the post from the database
    post = session.query(models.Post).get(id)

    # Check whether the post existsm if not return 404 with a message
    if not post:
        message = "Could not find post with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    # Return the post as JSON
    data = json.dumps(post.as_dictionary())
    return Response(data, 200, mimetype="application/json")

@app.route("/api/posts/<int:id>", methods=["DELETE"])
@decorators.accept("application/json")
def delete_post(id):
    # delete a single entry
    # get post from database
    post = session.query(models.Post).get(id)
    
    # make sure the post exists
    if not post:
        message = "Could not find post with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")
    
    # delete post
    session.delete(post)
    session.commit()
    message = "Post with id {} has been deleted".format(id)
    data = json.dumps({"message": message})
    return Response(data, 200, mimetype="application/json")