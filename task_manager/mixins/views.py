from http import HTTPStatus

from django.views.generic.base import TemplateResponseMixin, ContextMixin


class RaiseUnprocessableEnittyIfInvalidMixin(TemplateResponseMixin, ContextMixin):
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form),
                                       status=HTTPStatus.UNPROCESSABLE_ENTITY)
