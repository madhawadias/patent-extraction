$(document).ready(function() {

	$('form').on('submit', function(event) {

        $('#searching').text("Searching.....").show();
        $('#errorAlert').hide();
        $('#successAlert').hide();

        function reqListener() {
        var res = this.responseText;
        console.log(res)
        document.getElementById("searching").innerHTML=res
        }

        var get_progress = setInterval(function(){
        var oReq = new XMLHttpRequest();
        oReq.open("GET", "/progress", true);
        oReq.send()
        oReq.addEventListener('load', reqListener);
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


