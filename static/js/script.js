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
});
