from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
from database.mongodb import posts_collection, comments_collection, per_page
from bson.objectid import ObjectId

from controllers.db.user_controller import get_user_data
from controllers.post_controller import *

from logger_settings import setup_logger

logger = setup_logger("post")
logger.info("Запуск страницы постов")


def init_post(app):
    @app.route('/main_post_page')
    def posts_view():
        user_id = session.get("user_id")
        user_data = get_user_data(user_id)
        page = int(request.args.get("page", 1))

        last_posts = list(posts_collection.find().sort("created_at", -1).skip(per_page * (page - 1)).limit(per_page))
        post_ids = {post["_id"]: post for post in last_posts}

        # Получаем комментарии из Mongo
        comments = comments_collection.find({"post_id": {"$in": list(post_ids.keys())}})
        comments_by_post = {post_id: [] for post_id in post_ids}
        for comment in comments:
            comment["can_delete"] = can_edit_comment(post_ids[comment["post_id"]], comment, user_data)
            comments_by_post[comment["post_id"]].append(comment)
        
        # Добавляем количество комментариев к каждому посту
        for post in last_posts:
            post["title"] = f"""{post["author"]}: {post["title"]}"""
            post["content"], post["setup"] = make_content(post)
            post["comments"] = comments_by_post[post["_id"]]
            post["can_delete"] = can_delete_post(post, user_data)
        total_pages = (posts_collection.count_documents({}) + per_page - 1) // per_page

        return render_template("posts.html", posts=last_posts, current_page=page, total_pages=total_pages)


    @app.route('/add_comment', methods=['POST'])
    def add_comment():
        
        data = request.json
        post_id = data.get("post_id")
        logger.debug(data)
        text = data.get("text")

        if not post_id or not text:
            return jsonify({"error": "Недостаточно данных"}), 400

        user_id = session.get("user_id")
        user_data = get_user_data(user_id)
        new_comment = {
            "post_id": ObjectId(post_id),
            "text": text,
            "user": user_data["username"],
            "created_at": datetime.now()
        }

        result = comments_collection.insert_one(new_comment)
        new_comment["_id"] = result.inserted_id

        logger.debug(new_comment)

        return jsonify({
            "success": True,
            "comment_id": str(new_comment["_id"]),
            "user": new_comment["user"],
            "created_at": new_comment["created_at"].strftime('%d.%m.%Y %H:%M'),
            "can_delete": True  # всегда true для автора в момент создания
        })


    @app.route('/delete_post', methods=['POST'])
    def delete_post():
        data = request.json
        post_id = data.get("post_id")

        if not post_id:
            return jsonify({"error": "Нет ID"}), 400

        post = posts_collection.find_one({"_id": ObjectId(post_id)})

        if not post:
            return jsonify({"error": "Пост не найден"}), 404

        user_id = session.get("user_id")
        user_data = get_user_data(user_id)

        if not can_delete_post(post, user_data):
            return jsonify({"error": "Нет доступа"}), 403

        posts_collection.delete_one({"_id": ObjectId(post_id)})
        comments_collection.delete_many({"post_id": ObjectId(post_id)})

        return jsonify({"success": True})

    @app.route('/delete_comment', methods=['POST'])
    def delete_comment():
        data = request.json
        comment_id = data.get("comment_id")

        if not comment_id:
            return jsonify({"error": "Нет ID"}), 400

        comment = comments_collection.find_one({"_id": ObjectId(comment_id)})
        post = posts_collection.find_one({"_id": comment["post_id"]})

        if not comment:
            return jsonify({"error": "Комментарий не найден"}), 404

        user_id = session.get("user_id")
        user_data = get_user_data(user_id)
        
        if not can_edit_comment(post, comment, user_data):
            return jsonify({"error": "Нет доступа"}), 403

        comments_collection.delete_one({"_id": ObjectId(comment_id)})

        return jsonify({"success": True})

