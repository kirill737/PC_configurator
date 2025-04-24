from datetime import datetime, timedelta
from database.mongodb import db, posts_collection, comments_collection
from controllers.db.build_controller import get_build_info
from logger_settings import setup_logger
from flask import session
import json

logger = setup_logger("posts_controller")

def make_content(post: dict):
    beggining = post.pop("content", "")
    
    setup = ""
    for k in post.keys() - {"created_at", "comments", "_id", "title", "author_id"}:
        
        if post[k]:
            setup += f"{k}: {post[k]}<br>"
    
    return beggining, setup


def can_delete_post(post, user_data):
    return user_data["role"] == "admin" or post.get("author_id") == user_data['user_id']


def can_edit_comment(post, comment, user_data):
    logger.debug(user_data)
    if user_data["role"] == 'guest':
        return False
    return user_data["role"] == "admin" or any(v == user_data["username"] for v in [comment.get("user"), post.get("author_id")])

def create_post(post: dict, author_id: str, build_id: int):
    new_post = post.copy()
    logger.debug(post)
    new_post["created_at"] = datetime.now()
    new_post["author_id"] = author_id

    build_info = get_build_info(build_id)
    logger.debug(build_info)
    for ct in build_info:
        new_post[ct['ct_rus']] = ct['name']


    posts_collection.insert_one(new_post)
    
    return