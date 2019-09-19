var question_no = 1;

function readURL(input) {
	if (input.files && input.files[0]) {
		var reader = new FileReader();

		reader.onload = function (e) {
			$('#file-drag').html(
				`<img src = "${ e.target.result}" style = "width:350px; height:200px;"/>`
			)
		}

		reader.readAsDataURL(input.files[0]);
	}
}
$("#question_area").hide();

var answers;

$("#id_image").change(function () {
	readURL(this);

	var formData = new FormData();
	formData.append('image', $(this)[0].files[0]);
	formData.append('csrfmiddlewaretoken', $("input[type='hidden']").val());

	$.ajax({
		url: "/ajax/upload/image",
		type: 'POST',
		data: formData,
		success: function (response) {
			$("#question_area").show();
			currentImageId = response["image_id"];
			$("#image_id").val(currentImageId);
			$("#question").focus();
			question_no= 1;
		},
		cache: false,
		contentType: false,
		processData: false
	});

});


$("#ask_question").click(function (e) {
	e.preventDefault();
	if ($("#question").val().length === 0) {
		alert("No question asked");
		return false;
	}
	var formData = {
		"question": $("#question").val(),
		"image_id": $("#image_id").val(),
		"question_no": question_no,
	};
	$(this).button('loading');
	$(this).prop("disabled", true);


	$("#question").prop("disabled", true);

	$.ajax({
		url: "/ajax/upload/question",
		type: 'GET',
		data: formData,
		success: function (response) {
			answers = response["answers"]
			$("#question").prop("disabled", false);
			var answers_html = ""
			$.each(answers, function (i, answer) {
				answers_html += `<p><b>${answer["label"]}</b> with confidence of <b>${answer["prediction"]}</b></p>`
			});
			$("#answer_area").html(answers_html);
			$("#ask_question").button('reset');
			$("#ask_question").prop("disabled", false);
			question_no+=1;

		},
		error: function (response) {
			console.log(response["error"]);
			$("#ask_question").button('reset');
			$("#ask_question").prop("disabled", false);

			alert("Something went wrong");
		},
	});


})

$("#question").focus(function () {
	$("#answer_area").html("")
	$("#question").val("");

})
