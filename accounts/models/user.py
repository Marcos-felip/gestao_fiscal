import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from core.models import CompanyBaseModel
from .company import Company


class User(AbstractUser):
    """Usuário customizado para permitir relacionamentos de membership multi-empresa."""
    email = models.EmailField(unique=True)
    username = models.CharField(blank=True, null=True, max_length=100)
    company_active = models.ForeignKey(Company, verbose_name='Empresa ativa', blank=True, null=True, on_delete=models.CASCADE, related_name="company")
    company_list = models.ManyToManyField(Company, verbose_name='Empresas', blank=True, through='Membership')
    email_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Membership(CompanyBaseModel):
    """Associação de usuário a empresa, com permissões."""
    class Role(models.TextChoices):
        OWNER = 'owner', 'Proprietário da Conta'
        ADMIN = 'admin', 'Administrador'
        MEMBER = 'member', 'Membro'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
    key = models.CharField(max_length=50, unique=True, verbose_name='Chave de acesso')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'company')

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} @ {self.company.legal_name} ({self.role})"