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
});
