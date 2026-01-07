from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from accounts.models.user import Membership
from django.urls import reverse_lazy
from django.shortcuts import redirect
from configuration.forms.users import UserMembershipForm


class UserListView(ListView):
    """
        View para listar os usuários do sistema.
    """
    model = Membership
    template_name = 'users/list_view.html'
    partial_template_name = 'users/includes/list_view.html'
    
    def get_queryset(self):
        company = self.request.user.company_active
        queryset = Membership.objects.filter(company=company).select_related('user')
        
        # Aplicar filtros
        status = self.request.GET.get('status', 'all')
        search = self.request.GET.get('search', '')
        
        # Filtrar por status (ativo/inativo)
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)
            
        # Busca por nome ou email
        if search:
            queryset = queryset.filter(
                user__email__icontains=search
            ) | queryset.filter(
                user__first_name__icontains=search
            ) | queryset.filter(
                user__last_name__icontains=search
            )
            
        return queryset
    
    def get_table_config(self):
        """
            Configuração da tabela de usuários.
        """
        return {
            'card_title': 'Usuários',
            'card_actions': [
                {
                    'label': 'Novo Usuário',
                    'url': reverse_lazy('configuration:user_create'),
                    'icon': '<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-plus" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M12 5l0 14" /><path d="M5 12l14 0" /></svg>',
                    'variant': 'primary'
                }
            ],
            'table_id': 'users-table',
            'headers': [
                {
                    'label': 'Nome',
                    'field': 'user.first_name',
                    'template': 'users/components/user_table_cells.html',
                    'cell_type': 'name'
                },
                {
                    'label': 'Email',
                    'field': 'user.email',
                    'template': 'users/components/user_table_cells.html',
                    'cell_type': 'email'
                },
                {
                    'label': 'Perfil',
                    'field': 'role',
                    'template': 'users/components/user_table_cells.html',
                    'cell_type': 'role'
                },
                {
                    'label': 'Status',
                    'field': 'is_active',
                    'template': 'users/components/user_table_cells.html',
                    'cell_type': 'status'
                },
            ],
            'actions_template': 'users/components/user_table_cells.html',
            'actions_cell_type': 'actions',
            'empty_message': 'Nenhum usuário encontrado.',
        }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', 'all')
        context['current_search'] = self.request.GET.get('search', '')
        context['table_config'] = self.get_table_config()
        return context
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('Hx-Request'):
            self.template_name = self.partial_template_name
        return super().render_to_response(context, **response_kwargs)


class UserCreateView(CreateView):
    """
        View para criar um novo usuário.
    """
    template_name = 'users/create_view.html'
    model = Membership
    form_class = UserMembershipForm
    success_url = reverse_lazy('configuration:user_list')

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
    success_url = reverse_lazy('configuration:user_list')

    def get_form_kwargs(self):
        kwargs = super(UserUpdateView, self).get_form_kwargs()
        company_obj = self.request.user.company_active
        if self.object.is_active:
            kwargs['company_obj'] = company_obj
        return kwargs


class UserDeleteView(DeleteView):
    """
        View para desativar um usuário existente.
    """

    template_name = 'users/includes/delete_view.html'
    model = Membership
    success_url = reverse_lazy('configuration:user_list')

    def post(self, request, *args, **kwargs):
        membership = self.get_object()
        if self.request.user.company_active == membership.user.company_active:
            membership.user.company_active = None
            membership.user.save()
        membership.is_active = False
        membership.save()
            
        return redirect(self.success_url)


class UserReactivateView(UpdateView):
    """
        View para reativar um usuário existente.
    """
    template_name = 'users/includes/reactivate_view.html'
    model = Membership
    fields = []
    success_url = reverse_lazy('configuration:user_list')

    def post(self, request, *args, **kwargs):
        membership = self.get_object()
        if self.request.user.company_active == membership.user.company_active:
            membership.user.company_active = membership.company
            membership.user.save()
        membership.is_active = True
        membership.save()
            
        return redirect(self.success_url)