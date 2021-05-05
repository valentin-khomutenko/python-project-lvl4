from http import HTTPStatus

from django.contrib import messages
from django.views.generic.base import TemplateResponseMixin, ContextMixin


class RaiseUnprocessableEnittyIfInvalidMixin(TemplateResponseMixin, ContextMixin):
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form),
                                       status=HTTPStatus.UNPROCESSABLE_ENTITY)


class SuccessMessageDeleteMixin:
    success_message = ''

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, self.success_message)
        return response
