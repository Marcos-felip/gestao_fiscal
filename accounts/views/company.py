from django.urls import reverse_lazy
from django.views.generic import FormView

from accounts.models.company import Company, Establishment
from accounts.forms import CompanySetupForm
from accounts.models.user import Membership

class CompanyCreateView(FormView):
    """
        View para criação de empresa e estabelecimento matriz após o cadastro do usuário
    """
    form_class = CompanySetupForm
    template_name = 'account/company_create.html'
    #success_url = reverse_lazy('dashboard:home')

    def form_valid(self, form):
        user = self.request.user

        company = Company.objects.create(
            legal_name=form.cleaned_data['legal_name'],
        )

        Establishment.objects.create(
            company=company,
            phone=form.cleaned_data.get('phone'),
            is_matrix=True,
        )

        user.company_active = company
        user.save(update_fields=['company_active'])

        member = Membership.objects.create(
            user=user,
            company=company,
            role=Membership.Role.OWNER,
            is_active=True
        )

        member.save()
        
        return super().form_valid(form)
