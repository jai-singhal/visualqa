
function readURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      
      reader.onload = function(e) {
        $('#file-drag').html(
            `<img src = "${ e.target.result}" style = "width:350px; height:200px;"/>`
        )
      }
      
      reader.readAsDataURL(input.files[0]);
    }
  }
  $("#question_area").hide();

var currentImageId = "";

$("#id_image").change(function() {
    readURL(this);

    var formData = new FormData();
    formData.append( 'image', $( this)[0].files[0] );
    formData.append( 'csrfmiddlewaretoken', $("input[type='hidden']").val() );

    $.ajax({
        url: "/ajax/upload/image",
        type: 'POST',
        data: formData,
        success: function (response) {
            console.log(response);
            $("#question_area").show();
            currentImageId = response["image_id"];
            $("#image_id").val(currentImageId);
        },
        cache: false,
        contentType: false,
        processData: false
    });

  });

  $("#questionForm").submit(function(e){
    if( $("#question").val().length === 0 ){
      alert("No question asked");
      return false;
    }
    e.preventDefault()
    $form = $(this)
    var formData = new FormData(this);
    // formData.append('image_id', currentImageId);
    
    console.log(formData)
    $("#question").prop("disabled", true);

    $.ajax({
        url: "/ajax/upload/question",
        type: 'POST',
        data: formData,
        success: function (response) {
            answers = response["answers"]
            $("#question").val("");
            $("#question").prop("disabled", false);
            console.log(answers)
            $("#answer_area").html(`
            <p>${answers[0]["label"]}
             with confidence of ${answers[0]["prediction"]}</p>
             `);
            
        },
        error: function(response){
          alert("Something went wrong");
        },
        cache: false,
        contentType: false,
        processData: false
    });


  })

$("#question").focus(function(){
    $("#answer_area").html("")
})