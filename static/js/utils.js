'use strict';

function formAjaxSubmit(modal, action) {
    var form = modal.find('.modal-body form');
    var footer = $(modal).find('.modal-footer');

    // bind to the form’s submit event
    $(form).on('submit', function(event) {

        // prevent the form from performing its default submit action
        event.preventDefault();
        footer.addClass('loading');

        // either use the action supplied by the form, or the original rendering url
        var url = $(this).attr('action') || action;

        // serialize the form’s content and sent via an AJAX call
        // using the form’s defined method
        $.ajax({
            type: $(this).attr('method'),
            url: url,
            data: $(this).serialize(),
            success: function(xhr, ajaxOptions, thrownError) {

                // If the server sends back a successful response,
                // we need to further check the HTML received

                // If xhr contains any field errors, the form did not
                // validate successfully, so we update the modal body
                // with the new form and its error
                if ($(xhr).find('.has-error').length > 0) {
                    $(modal).find('.modal-body').html(xhr);
                    formAjaxSubmit(modal, url);
                } else {
                    // otherwise, we've done and can close the modal
                    $(modal).modal('hide');
                }
            },
            error: function(xhr, ajaxOptions, thrownError) {
            },
            complete: function() {
                footer.removeClass('loading');
            }
        });
    });
}


/*
    Add spinner while new image gets loaded completely:
      https://stackoverflow.com/questions/21258195/add-spinner-while-new-image-gets-loaded-completely#21262404

    Set the CSS background-image property of the images to a loading spinner graphic;
    once the actual image is downloaded, it covers up the "loading" animated GIF background image.
*/

// .loading {
//     background: transparent url(/static/frontend/images/spinner.gif) no-repeat scroll center center;
// }