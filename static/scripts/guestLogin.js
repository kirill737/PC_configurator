function guestLogin() {
    // Отправляем запрос на сервер, чтобы выполнить нужную функцию
    fetch('{{ url_for("guest_login") }}', { method: 'POST' })
        .then(response => {
            if (response.ok) {
                // Перенаправляем пользователя после того, как функция выполнена
                window.location.href = '{{ url_for("posts_view") }}';
            } else {
                alert('Произошла ошибка');
            }
        });
}