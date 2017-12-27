
function makeRequest_re(){

    var Country = $('#id_Country').val();
    var URL_key = $('#id_url').val();
    var start = $('#id_start').val();
    makeRequest(Country, URL_key, start);
}


function makeRequest(Country, URL_key, start=0){

    args = {'Country': Country, 'URL_key': URL_key, 'start': start};
    $.ajax({url: '/', data: args, type: 'POST',


  

        error: function() {
            $('#output_text_id').html('An error has occurred');
        },
        success: function(data) {
            $('#output_text_id').html(data);
         }

     
     });
}