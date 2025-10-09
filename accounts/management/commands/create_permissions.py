from django.core.management.base import BaseCommand
from django.db import transaction
from accounts.models.user import Permission

class Command(BaseCommand):
    help = 'Cria as permissões iniciais simplificadas para o sistema'

    DEFAULT_PERMISSIONS = [
        {'name': 'Gerenciar usuários', 'codename': 'users_manage'},
        {'name': 'Gerenciar empresas', 'codename': 'companies_manage'},   
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Remove todas as permissões existentes antes de criar as novas',
        )

    def handle(self, *args, **options):
        reset = options.get('reset', False)
        
        self.stdout.write('🚀 Iniciando criação de permissões...')
        
        created_count = 0
        existing_count = 0
        
        with transaction.atomic():
            if reset:
                deleted_count, _ = Permission.objects.all().delete()
                self.stdout.write(self.style.WARNING(f'🗑️  {deleted_count} permissões removidas'))
            
            for perm_data in self.DEFAULT_PERMISSIONS:
                permission, created = Permission.objects.get_or_create(
                    codename=perm_data['codename'],
                    defaults={'name': perm_data['name']}
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(f'✅ CRIADA: {perm_data["name"]}')
                else:
                    existing_count += 1
                    self.stdout.write(f'🔵 EXISTIA: {perm_data["name"]}')
        
        self.stdout.write(self.style.SUCCESS(f'\n🎉 Concluído! {created_count} novas, {existing_count} existentes'))