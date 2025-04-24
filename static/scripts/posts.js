import { getCurrentBuildId, setCurrentBuildId } from "./help.js"

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
                        // commentCount.textContent = `Комментариев: ${currentCount}`;
                    } else {
                        alert("Ошибка при удалении комментария");
                    }
                });

                newCommentBox.appendChild(deleteButton);
            }

            commentsBlock.appendChild(newCommentBox);

            // Обновляем счётчик
            const currentCount = parseInt(commentCount.textContent) || 0;
            commentCount.textContent = `Комментариев: ${currentCount + 1}`;
            
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


document.getElementById("create-post-button").addEventListener("click", async function () {
    const create_post_menu = document.getElementById("create-post-menu");
    create_post_menu.classList.remove("hidden");
    await setCurrentBuildId(0);
    
    let selected_build_id = 0;
    document.getElementById("post-select-build-button").addEventListener("click", async () => {

        // Передача id выбранной сборки в python (далее в redis)
        // async function selectBuild(buildId) {
        //     await setCurrentBuildId(buildId);
        // }
        const post_select_build_button = document.getElementById("post-select-build-button");
        const menu = document.getElementById("builds-menu");
        menu.classList.remove("hidden");
        
    
        const response = await fetch("/all/builds");
        const builds = await response.json();
    
        const list = document.getElementById("builds-list");
        list.innerHTML = "";
        list.classList.remove("hidden");
        
        builds.forEach(build => {
            const li = document.createElement("li");
            li.textContent = build.name;
            li.addEventListener("click", async () => {
                await setCurrentBuildId(build.id);
                post_select_build_button.textContent = build.name;
                console.log("Выбрали сборку " + selected_build_id);
                list.classList.add("hidden");
            });
            list.appendChild(li);
        });
    });

    const publishBtn = document.getElementById("publish-post");
    if (!publishBtn.dataset.listenerAdded) {
        publishBtn.addEventListener("click", async () => {
            const buildId_dict = await getCurrentBuildId();
            const buildId = buildId_dict['build_id'];
            const titleInput = document.getElementById("post-title-input");
            const contentInput = document.getElementById("post-text-area");
            console.log("buildId->>>>>" + buildId);
            const title = titleInput.value.trim();
            const content = contentInput.value.trim();

            if (!title) {
                alert("Пожалуйста, заполните все поля поста");
                return;
            }

            const response = await fetch("/create/post", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    title: title,
                    content: content,
                    build_id: buildId
                })
            });

            if (response.ok) {
                alert("Пост успешно создан!");
                // можно очистить поля или скрыть форму
            } else {
                alert("Ошибка при создании поста");
            }
        });

        publishBtn.dataset.listenerAdded = "true";
    }

})


document.addEventListener("click", function(event) {
    let menu = document.getElementById("builds-list");
    let select_build_button = document.getElementById("post-select-build-button");
    if (!menu.contains(event.target) && !select_build_button.contains(event.target)) {
        menu.classList.add("hidden");
    }

    let create_post_button = document.getElementById("create-post-button");
    let post_menu = document.getElementById("create-post-menu");
    if (!post_menu.contains(event.target) && !create_post_button.contains(event.target)) {
        post_menu.classList.add("hidden");
    }
});





// Скрытие меню выбора сборки при нажатии вне него
// document.addEventListener("click", function(event) {
//     let menu = document.getElementById("builds-menu");
//     let select_build_button = document.getElementById("select-build-button");
//     if (!menu.contains(event.target) && !select_build_button.contains(event.target)) {
//         menu.classList.add("hidden");
//     }
// });