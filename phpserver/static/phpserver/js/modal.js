$(function(){
  $(document).on('click','.ajax-modal',function (evt){
    evt.preventDefault();
    var $this = $(this);
    $.ajax($this.attr('href'),{
      success:function(data){
        $('#modal_wrapper').append(data);
        var modal = $('.modal:last');
        modal.modal();
      }
    });
  });

  $(document).on('submit','.modal form',function (evt) {
    evt.preventDefault();
    var $form = $(this),
    form = this,
    ajaxOpts,formData;

    formData = $form.serialize();

    console.log(formData);

    ajaxOpts = {
      type: "POST",
      url: $form.attr('action'),
      data: formData,
      beforeSend: function () {
        $form.closest(".modal").modal("hide");
      },
      error: function(){
        alert("ajax-Error");
      }
    };
    $.ajax(ajaxOpts);
  });

  $(document).on('click', '.modal .cancel', function (evt) {
    evt.preventDefault();
    $(this).closest('.modal').modal('hide');
  });

  $(document).on('click', '#search', function (evt) {
    evt.preventDefault();
    var $form = $("#search_image"),
    ajaxOpts,formData;

    formData = $form.serialize();
    ajaxOpts = {
      type: "POST",
      url: $form.attr('action'),
      data: formData,
      beforeSend: function() {
        $(".image-table").remove();
        $('<b class="ajax-temp">Loading...</b>').insertAfter($("#search_image .modal-body"));
      },
      complete: function() {
      },
      success: function(data) {
        $(".ajax-temp").remove();
        $(data).insertAfter($("#search_image .modal-body"));
      },
      error: function(){
        alert("ajax-Error");
      }
    };
    $.ajax(ajaxOpts);
  });

  $(document).on('hidden.bs.modal', '.modal', function () {
    var $this = $(this),
      modal_stack = $("#modal_wrapper .modal");
    if ($this[0] === modal_stack.last()[0]) {
      $this.remove();
    }
  });

});