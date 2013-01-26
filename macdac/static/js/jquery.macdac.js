$(function(){
	// Ctrl + arrows navigation.
	$(document).keydown(function(e) {
		var link = '';

		if (e.keyCode == 0x27 && e.ctrlKey) {
			link = $('#next-link').attr('href');
		}
		if (e.keyCode == 0x25 && e.ctrlKey) {
			link = $('#previous-link').attr('href');
		}
		if (link) {
			document.location = link;
		}
	});
});


function csrfSafeMethod(method) {
    // These HTTP methods do not require CSRF protection

    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
	crossDomain: false,
	beforeSend: function(xhr, settings) {
		if (!csrfSafeMethod(settings.type)) {
			xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
		}
	}
});