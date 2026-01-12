from django.shortcuts import render
from django.views.generic import TemplateView, View

from accounts.forms import CustomChangePasswordForm, ProfileForm

class BaseProfileView(TemplateView):
    template_name = 'account/layouts/base_profile.html'


class ProfileView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        profile_form = ProfileForm(instance=request.user)
        change_password_form = CustomChangePasswordForm(user=request.user)
        context['profile_form'] = profile_form
        context['change_password_form'] = change_password_form

        return render(request, 'account/profile.html', context)

    def post(self, request, *args, **kwargs):
        profile_form = ProfileForm(request.POST, instance=request.user)
        change_password_form = CustomChangePasswordForm(request.POST, user=request.user)
        if profile_form.is_valid() and change_password_form.is_valid():
            profile_form.save()
            change_password_form.save()
            ## Adicionar mensagem de sucesso ou redirecionamento
        context = {'profile_form': profile_form, 'change_password_form': change_password_form}
        return render(request, 'account/profile.html', context)
