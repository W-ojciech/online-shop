from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic
from app_shop.models import Basket


def create_basked(self):
    basket = Basket()
    basket.customers = self
    basket.save()

def save(self, *args, **kwargs):
    creaded = not self.id
    super(User, self).save(*args, **kwargs)
    if creaded:
        self.create_basked()

User.save = save
setattr(User, 'create_basked', create_basked)



class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

