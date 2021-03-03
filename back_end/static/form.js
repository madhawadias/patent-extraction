$(document).ready(function() {

	$('form').on('submit', function(event) {

        $('#searching').text("Searching.....").show();
        $('#errorAlert').hide();
        $('#successAlert').hide();

        var get_progress = setInterval(function(){
        document.getElementById("searching").innerHTML="res"
        }, 2000);

		$.ajax({
			data : {
				name : $('#nameInput').val(),
				count : $('#countInput').val()
			},
			type : 'POST',
			url : '/process'
		})
		.done(function(data) {
            clearInterval(get_progress);
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


