from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, FormView
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView

from .forms import CustomUserCreationForm

User = get_user_model()


class UserRegisterView(SuccessMessageMixin, FormView):
    template_name = "authentication/register.html"
    form_class = CustomUserCreationForm
    success_message = "Registration successful!"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Редірект після успішної реєстрації
        return reverse_lazy('authentication:login')


class UserLoginView(BaseLoginView):
    template_name = "authentication/login.html"
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))

class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('authentication:login')
