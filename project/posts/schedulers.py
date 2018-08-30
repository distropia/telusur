
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import generic
from django.views.generic.edit import FormView
from django.shortcuts import redirect

from .forms import GenerateRandomUserForm
from .tasks import create_random_posts

class UserListView(generic.ListView):
	template_name = 'posts/users_list.html'
	model = User

class GenerateRandomUserView(FormView):
    template_name = 'posts/generate_random_users.html'
    form_class = GenerateRandomUserForm

    def form_valid(self, form):
        total = form.cleaned_data.get('total')
        create_random_posts.delay(total)
        messages.success(self.request, 'We are generating your random users! Wait a moment and refresh this page.')
        return redirect('users_list')