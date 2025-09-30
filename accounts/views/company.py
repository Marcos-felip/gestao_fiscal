from django.views.generic import CreateView

from accounts.models.company import Company
from accounts.forms import CompanySetupForm
from accounts.models.user import Membership

class CompanyCreateView(CreateView):
    form_class = CompanySetupForm
    ##template_name
    ##success_url

    def form_valid(self, form):
        user = self.request.user
        ## Cria a empresa
        company = Company.objects.create(
            legal_name=form.cleaned_data['legal_name'],
            slug=form.cleaned_data['slug'],
        )
        ## Atrela o usuário à empresa (Membership)
        member = Membership.objects.create(
            user=user,
            company=company,
            role=Membership.Role.OWNER,
            is_active=True
        )
        user.company_active = company
        user.save(update_fields=['company_active'])
        return super().form_valid(form)
