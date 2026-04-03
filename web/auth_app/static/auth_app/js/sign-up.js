console.log('sing-up')
$(function () {
  $('#signUpForm').submit(singUp);
});

function singUp(e) {
  let form = $(this);
  e.preventDefault();

  // Скрыть предыдущие сообщения
  $('#signUpMessage').remove();

  // Добавить индикатор загрузки
  const submitBtn = form.find('button[type="submit"]');
  const originalText = submitBtn.text();
  submitBtn.prop('disabled', true).text('Регистрация...');

  $.ajax({
    url: "/api/v1/auth/sign-up/",
    type: "POST",
    data: form.serialize(),

    success: function(data) {
      console.log("Success", data)

      // Создать сообщение об успехе
      const successMsg = $('<div id="signUpMessage" class="alert alert-success" role="alert"></div>');
      successMsg.html(`
        <strong>Успешная регистрация!</strong><br>
        ${data.message || 'Вы успешно зарегистрировались. Проверьте вашу почту для подтверждения.'}
      `);

      // Вставить сообщение перед формой
      form.before(successMsg);
      
      // Очистить форму
      form[0].reset();

      // Перенаправление (если нужно)
      if (data.redirect_url) {
        setTimeout(() => {
          window.location.href = data.redirect_url;
        }, 3000);
      }
    },

    error: function(data) {
      console.log("Error", data)

      let errorMessage = 'Произошла ошибка при регистрации.';
      
      // Парсим ответ от сервера
      if (data.responseJSON) {
        const errors = data.responseJSON;
        
        // Если есть общее сообщение об ошибке
        if (errors.detail) {
          errorMessage = errors.detail;
        }
        // Если есть ошибки полей
        else if (errors.non_field_errors) {
          errorMessage = errors.non_field_errors.join('<br>');
        }
        else {
          // Форматируем ошибки полей
          const fieldErrors = [];
          for (const [field, messages] of Object.entries(errors)) {
            if (Array.isArray(messages)) {
              fieldErrors.push(`<strong>${field}:</strong> ${messages.join(', ')}`);
            }
          }
          if (fieldErrors.length > 0) {
            errorMessage = fieldErrors.join('<br>');
          }
        }
      } else if (data.status === 0) {
        errorMessage = 'Нет соединения с интернетом. Проверьте подключение.';
      } else if (data.status === 500) {
        errorMessage = 'Внутренняя ошибка сервера. Пожалуйста, попробуйте позже.';
      }
      
      // Создать сообщение об ошибке
      const errorMsg = $('<div id="signUpMessage" class="alert alert-danger" role="alert"></div>');
      errorMsg.html(`<strong>Ошибка!</strong><br>${errorMessage}`);
      
      // Вставить сообщение перед формой
      form.before(errorMsg);
      
      // Прокрутить к сообщению об ошибке
      $('html, body').animate({
        scrollTop: errorMsg.offset().top - 100
      }, 500);
    },

    complete: function() {
      // Восстановить кнопку
      submitBtn.prop('disabled', false).text(originalText);
    }
  });
}
