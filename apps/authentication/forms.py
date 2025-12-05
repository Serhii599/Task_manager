from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # кастомні лейбли/атрибути для полів
        self.fields['email'].label = "Email"
        self.fields['first_name'].label = "Name"
        self.fields['last_name'].label = "Surname"