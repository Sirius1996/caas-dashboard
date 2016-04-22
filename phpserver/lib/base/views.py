from django import template
from django.utils import encoding
from django.views.generic.base import TemplateView
from django.views import generic


class PageTitleMixin(object):
    """A mixin that renders out a page title into a view.

    Many views in horizon have a page title that would ordinarily be
    defined and passed through in get_context_data function, this often
    leads to a lot of duplicated work in each view.

    This mixin standardises the process of defining a page title, letting
    views simply define a variable that is rendered into the context for
    them.

    There are cases when page title in a view may also display some context
    data, for that purpose the page_title variable supports the django
    templating language and will be rendered using the context defined by the
    views get_context_data.
    """

    page_title = ""

    def render_context_with_title(self, context):
        """This function takes in a context dict and uses it to render the
        page_title variable, it then appends this title to the context using
        the 'page_title' key. If there is already a page_title key defined in
        context received then this function will do nothing.
        """

        if "page_title" not in context:
            con = template.Context(context)
            # NOTE(sambetts): Use force_text to ensure lazy translations
            # are handled correctly.
            temp = template.Template(encoding.force_text(self.page_title))
            context["page_title"] = temp.render(con)
        return context

    def render_to_response(self, context):
        """This is an override of the default render_to_response function that
        exists in the django generic views, this is here to inject the
        page title into the context before the main template is rendered.
        """

        context = self.render_context_with_title(context)
        return super(PageTitleMixin, self).render_to_response(context)

class CaasTemplateView (PageTitleMixin,TemplateView):
    pass

class CaasFormView (PageTitleMixin,generic.FormView):
    pass