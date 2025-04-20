def make_content(post: dict):
    beggining = post.pop("content", "")
    
    setup = ""
    for k in post.keys() - {"created_at", "comments", "_id", "title", "author"}:
        setup += f"{k}: {post[k]}<br>"
    
    return beggining, setup


def can_delete_post(post, user):
    return user["role"] == "admin" or post.get("author") == user["username"]


def can_edit_comment(post, comment, user):
    return user["role"] == "admin" or any(v == user["username"] for v in [comment.get("user"), post.get("author")])
