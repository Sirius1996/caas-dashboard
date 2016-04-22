      beforeSend: function() {
        $("#modal_wrapper .modal").last().modal("hide");
        $('.ajax-modal, .dropdown-toggle').attr('disabled', true);
      },
      complete: function () {
        $("#modal_wrapper .modal").last().modal("show");
        $button.prop("disabled", false);
      },
      success: function (data) {
        $form.closest(".modal").modal("hide");
        var modal;
        $('#modal_wrapper').append(data);
        modal = $('.modal:last');
        modal.modal();
        $(modal).trigger("new_modal", modal);
        return modal;
      },