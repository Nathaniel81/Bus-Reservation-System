document.addEventListener('DOMContentLoaded', function () {
	var date = document.getElementById('date');
	if (date){
		var today = new Date().toISOString().split('T')[0];
		date.min = today;
	}

	function highlightActiveLink() {
		var path = window.location.pathname;
		document.querySelectorAll('.navbar-nav .nav-item .nav-link').forEach(function (link) {
		  var href = link.getAttribute('href');
		  if (path === href) {
			link.classList.add('active');
		  } else {
			link.classList.remove('active');
		  }
		});
	  }

	  window.onload = highlightActiveLink;
	  window.addEventListener('hashchange', highlightActiveLink);
	  window.addEventListener('popstate', highlightActiveLink);

	  function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + '=') {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

	  const submitBtn = document.querySelector('#submit');
      const usernameField = document.querySelector('#id_username');
      const passwordField = document.querySelector('#id_password');
	  const errMsg = document.querySelector('#err-msg');
	  const spinner = document.getElementById('spinner');
	  
      submitBtn.addEventListener('click', function (e) {
          e.preventDefault();
	  
          const username = usernameField.value;
          const password = passwordField.value;
		  console.log(username, password)
		  const csrftoken = getCookie('csrftoken');
		  spinner.style.display = 'inline-block';
          $.ajax({
              type: "POST",
              headers: { "X-CSRFToken": csrftoken },
              url: "/auth/login/",
              data: {
                  username: username,
                  password: password
              },
              dataType: 'json',
              success: function (response) {
				  if (response.redirect) {
					setTimeout(function () {
					  window.location.href = response.redirect;
					}, 1000);
				  }
				if (response.message) {
					errMsg.textContent = response.message
					spinner.style.display = 'none';
				}
              },
              error: function (xhr, errmsg, err) {
                  console.log(xhr.status + ": " + xhr.responseText);
              }
          });
    });	

	const nameField = document.querySelector('#id_name');
	const userNameField= document.querySelector('#signup_id_username');
	const phoneNumberField = document.querySelector('#id_phone_number');
	const password1Field = document.querySelector('#id_password1');
	const password2Field = document.querySelector('#id_password2');
	const emailField = document.querySelector('#id_email');
	const signupBtn = document.querySelector('#signupBtn');


		  signupBtn.addEventListener('click', function(e) {
			e.preventDefault();
			const name = nameField.value;
			const username = userNameField.value;
			const phoneNumber = phoneNumberField.value;
			const password1 = password1Field.value;
			const password2 = password2Field.value;
			const email = emailField.value;
			console.log(name, username, phoneNumber, password1, password2);

		const csrftoken = getCookie('csrftoken');
		// spinner.style.display = 'inline-block';
          $.ajax({
              type: "POST",
              headers: { "X-CSRFToken": csrftoken },
              url: "/auth/signup/",
              data: {
				  name: name,
                  username: username,
				  email: email,
				  phone_number: phoneNumber,
                  password1: password1,
				  password2: password2,
				  
              },
              dataType: 'json',
              success: function (response) {
				  if (response.redirect) {
					setTimeout(function () {
					  window.location.href = response.redirect;
					}, 1000);
				  }
				if (response.message) {
					errMsg.textContent = response.message
					// spinner.style.display = 'none';
				}
              },
              error: function (xhr, errmsg, err) {
                  console.log(xhr.status + ": " + xhr.responseText);
              }
          });

		  })


});
