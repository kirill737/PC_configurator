document.querySelectorAll('.post').forEach(post => {
    const content = post.querySelector('.content');
    const commentsBlock = post.querySelector('.comments');
    const addCommentBlock = post.querySelector('.add-comment');
    const input = post.querySelector('input');
    const commentCount = post.querySelector('.comment-count');
    const sendButton = addCommentBlock.querySelector('button');

    const post_title = post.querySelector('.post-title');
    const post_data = post.querySelector('.post-data');
    const post_comments_container = post.querySelector('.post-comments-container');

    post.addEventListener('click', function () {
        content.style.display = 'block';
        commentsBlock.style.display = 'block';
        addCommentBlock.style.display = 'block';
    });
    post_title.addEventListener('click', function () {
        post_data.classList.toggle("hidden");
        post_comments_container.classList.toggle("hidden");
    });

    sendButton.addEventListener('click', async function (e) {
        e.stopPropagation();
        const text = input.value.trim();
        const postId = post.dataset.id;
        if (!text) return;

        const response = await fetch('/add_comment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ post_id: postId, text })
        });

        if (response.ok) {
            const result = await response.json();

            const newCommentBox = document.createElement('div');
            newCommentBox.classList.add('comment-box');
            newCommentBox.dataset.id = result.comment_id;

            const header = document.createElement('div');
            header.classList.add('comment-header');

            const userSpan = document.createElement('span');
            userSpan.classList.add('comment-user');
            userSpan.textContent = result.user;

            const dateSpan = document.createElement('span');
            dateSpan.classList.add('comment-date');
            dateSpan.textContent = result.created_at;

            header.appendChild(userSpan);
            header.appendChild(dateSpan);

            const textDiv = document.createElement('div');
            textDiv.classList.add('comment-text');
            textDiv.textContent = text;

            newCommentBox.appendChild(header);
            newCommentBox.appendChild(textDiv);

            // Добавляем кнопку удаления, если разрешено
            if (result.can_delete) {
                const deleteButton = document.createElement('button');
                deleteButton.classList.add('delete-comment');
                deleteButton.textContent = '🗑️';

                // обработчик удаления
                deleteButton.addEventListener('click', async function (e) {
                    e.stopPropagation();
                    const confirmed = confirm("Удалить комментарий?");
                    if (!confirmed) return;

                    const resp = await fetch('/delete_comment', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ comment_id: result.comment_id })
                    });

                    if (resp.ok) {
                        newCommentBox.remove();
                    } else {
                        alert("Ошибка при удалении комментария");
                    }
                });

                newCommentBox.appendChild(deleteButton);
            }

            commentsBlock.appendChild(newCommentBox);

            // Обновляем счётчик
            const currentCount = parseInt(commentCount.textContent) || 0;
            commentCount.textContent = `${currentCount + 1} комментариев`;

            input.value = '';
        }
    });
});


document.querySelectorAll('.delete-post').forEach(button => {
    button.addEventListener('click', async function (e) {
        e.stopPropagation();

        const postEl = this.closest('.post');
        const postId = postEl.dataset.id;

        const confirmed = confirm("Точно удалить пост?");
        if (!confirmed) return;

        const response = await fetch('/delete_post', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ post_id: postId })
        });

        if (response.ok) {
            postEl.remove(); // Удаляем из DOM
        } else {
            alert("Ошибка при удалении поста");
        }
    });
});

document.querySelectorAll('.delete-comment').forEach(button => {
    button.addEventListener('click', async function (e) {
        e.stopPropagation();
        const commentBox = this.closest('.comment-box');
        const commentId = commentBox.dataset.id;

        const confirmed = confirm("Удалить комментарий?");
        if (!confirmed) return;

        const response = await fetch('/delete_comment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ comment_id: commentId })
        });

        if (response.ok) {
            commentBox.remove();
        } else {
            alert("Ошибка при удалении комментария");
        }
    });
});