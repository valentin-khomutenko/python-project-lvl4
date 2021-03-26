from django.contrib.auth.mixins import UserPassesTestMixin


class CheckSelfUser(UserPassesTestMixin):
    def test_func(self):
        user = self.get_object()
        return user == self.request.user
