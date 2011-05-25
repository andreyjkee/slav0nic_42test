$(document).ready(function() { 
    $(document).ajaxStart($.blockUI).ajaxStop($.unblockUI);
    $('#basicform').ajaxForm({ 
        dataType: 'json',
        success: success_callback,
        error: error_callback,
    }); 
});

function success_callback(response, status) {
    if (response.success === true) {
        $("div#ajax_info").removeClass('error');
        $("div#ajax_info").addClass('success').text('Success');
    } else {
        $("div#ajax_info").removeClass('success');
        console.log(response.errors)
        $("div#ajax_info").addClass('error').text(response.errors);
    }
}

function error_callback(xhr, status, error) {
    $("div#ajax_info").removeClass('success');
    $("div#ajax_info").addClass('error').text('Error');
}