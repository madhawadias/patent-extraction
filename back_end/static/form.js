$(document).ready(function() {

	$('form').on('submit', function(event) {

        $('#searching').text("Searching.....").show();
        $('#errorAlert').hide();
        $('#successAlert').hide();
		$.ajax({
			data : {
				name : $('#nameInput').val(),
			},
			type : 'POST',
			url : '/process'
		})
		.done(function(data) {

			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
				$('#searching').text(data.error).hide();
			}
			else {
				$('#successAlert').text(data.name).show();
				$('#errorAlert').hide();
				$('#searching').text(data.error).hide();
			}
		});

		event.preventDefault();

	});

});

