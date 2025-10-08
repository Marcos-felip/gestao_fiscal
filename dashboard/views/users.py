from django.views.generic import ListView, CreateView, UpdateView
from accounts.models.user import User, Membership, Company
from django.urls import reverse_lazy

from dashboard.forms.users import UserMembershipForm


class UserListView(ListView):
    """
        View para listar os usuários do sistema.
    """
    model = Membership
    template_name = 'users/list_view.html'

    def context_data(self, **kwargs):
        context = super().context_data(**kwargs)
        return context
    
    def get_queryset(self):
        company = self.request.user.company_active
        print(' company', company)
        queryset = Membership.objects.filter(company=company)
        print(' queryset', queryset)
        return queryset


class UserCreateView(CreateView):
    """
        View para criar um novo usuário.
    """
    template_name = 'users/create_view.html'
    model = Membership
    form_class = UserMembershipForm
    success_url = reverse_lazy('dashboard:user_list')

    def get_form_kwargs(self):
        kwargs = super(UserCreateView, self).get_form_kwargs()
        company_obj = self.request.user.company_active
        kwargs['company_obj'] = company_obj
        return kwargs
    

class UserUpdateView(UpdateView):
    """
        View para atualizar um usuário existente.
    """
    template_name = 'users/create_view.html'
    model = Membership
    form_class = UserMembershipForm
    success_url = reverse_lazy('dashboard:user_list')

    def get_form_kwargs(self):
        kwargs = super(UserUpdateView, self).get_form_kwargs()
        company_obj = self.request.user.company_active
        if self.object.is_active:
            kwargs['company_obj'] = company_obj
        return kwargs


class UserDeleteView(UpdateView):
    """
        View para desativar um usuário existente.
    """
    template_name = 'users/delete_view.html'
    model = Membership
    success_url = reverse_lazy('dashboard:user_list')

    def form_valid(self, form):
        membership = self.get_object()
        membership.is_active = False
        membership.save()
        return super().form_valid(form)