from django.views import generic
from django import http

from phpserver.lib import base

import os


class ModalBackdropMixin(object):
    """This mixin class is to be used for together with ModalFormView and
    WorkflowView classes to augment them with modal_backdrop context data.

    .. attribute: modal_backdrop (optional)

        The appearance and behavior of backdrop under the modal element.
        Possible options are:
        * 'true' - show backdrop element outside the modal, close the modal
        after clicking on backdrop (the default one);
        * 'false' - do not show backdrop element, do not close the modal after
        clicking outside of it;
        * 'static' - show backdrop element outside the modal, do not close
        the modal after clicking on backdrop.
    """
    modal_backdrop = 'static'

    def __init__(self):
        super(ModalBackdropMixin, self).__init__()
        # config = getattr(settings, 'HORIZON_CONFIG', {})
        # if 'modal_backdrop' in config:
        #     self.modal_backdrop = config['modal_backdrop']

    def get_context_data(self, **kwargs):
        context = super(ModalBackdropMixin, self).get_context_data(**kwargs)
        context['modal_backdrop'] = self.modal_backdrop
        return context

class ModalFormMixin(object):
    def get_template_names(self):
        if self.request.is_ajax():
            if not hasattr(self, "ajax_template_name"):
                # Transform standard template name to ajax name (leading "_")
                bits = list(os.path.split(self.template_name))
                bits[1] = "".join(("_", bits[1]))
                self.ajax_template_name = os.path.join(*bits)
            template = self.ajax_template_name
            print template
        else:
            template = self.template_name
        return template

    def get_context_data(self, **kwargs):
        context = super(ModalFormMixin, self).get_context_data(**kwargs)
        if self.request.is_ajax():
            context['hide'] = True
            """@@@"""
        # if ADD_TO_FIELD_HEADER in self.request.META:
        #     context['add_to_field'] = self.request.META[ADD_TO_FIELD_HEADER] 
        return context

class ModalFormView(ModalBackdropMixin,ModalFormMixin,base.CaasFormView):
    """docstring for ModalFormView"ModalBackdropMixin,ModalFormMixin,django.FormView"""
    # __init__(self, arg):
    #   super(ModalFormView,ModalBackdropMixin,ModalFormMixin,django.FormView.__init__()
    #   self.arg = arg
    modal_id = None
    modal_header = ""
    form_id = None
    submit_url = None
    submit_label = "Submit"
    cancel_label = "Cancel"
    cancel_url = None

    def get_context_data(self, **kwargs):
        context = super(ModalFormView, self).get_context_data(**kwargs)
        context['modal_id'] = self.modal_id
        context['modal_header'] = self.modal_header
        context['form_id'] = self.form_id
        context['submit_url'] = self.submit_url
        context['submit_label'] = self.submit_label
        context['cancel_label'] = self.cancel_label
        context['cancel_url'] = self.get_cancel_url
        return context

    def get_cancel_url(self):
        """ Return success_url if cancel_url do not exist"""
        return self.cancel_url or self.success_url

    def get_form(self, form_class):
        """Returns an instance of the form to be used in this view."""
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        try:
            handled = form.handle(self.request, form.cleaned_data)
        except Exception, e:
            handled = None
            print e
            # exceptions.handle(self.request)

        # if handled:
        #     if ADD_TO_FIELD_HEADER in self.request.META:
        #         field_id = self.request.META[ADD_TO_FIELD_HEADER]
        #         data = [self.get_object_id(handled),
        #                 self.get_object_display(handled)]
        #         response = http.HttpResponse(json.dumps(data))
        #         response["X-Horizon-Add-To-Field"] = field_id
        #     elif isinstance(handled, http.HttpResponse):
        #         return handled
        #     else:
        #         success_url = self.get_success_url()
        #         response = http.HttpResponseRedirect(success_url)
        #         # TODO(gabriel): This is not a long-term solution to how
        #         # AJAX should be handled, but it's an expedient solution
        #         # until the blueprint for AJAX handling is architected
        #         # and implemented.
        #         response['X-Horizon-Location'] = success_url
        #     return response
        # else:
        #     # If handled didn't return, we can assume something went
        #     # wrong, and we should send back the form as-is.
        #     return self.form_invalid(form)

        # return super(ModalFormView, self).form_valid(form)
        if handled:
            return handled
        else:
            return http.HttpResponseRedirect(self.get_success_url())
