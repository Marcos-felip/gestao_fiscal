from django.core.management.base import BaseCommand
from django.db import transaction
from inventory.models.units import Unit
from accounts.models.company import Company


class Command(BaseCommand):
    help = 'Cria as unidades de medida iniciais para o sistema'

    DEFAULT_UNITS = [
        {'name': 'Quilograma', 'abbreviation': 'kg'},
        {'name': 'Grama', 'abbreviation': 'g'},
        {'name': 'Litro', 'abbreviation': 'L'},
        {'name': 'Mililitro', 'abbreviation': 'ml'},
        {'name': 'Unidade', 'abbreviation': 'un'},
        {'name': 'Peça', 'abbreviation': 'pc'},
        {'name': 'Caixa', 'abbreviation': 'cx'},
        {'name': 'Pacote', 'abbreviation': 'pct'},
        {'name': 'Metro', 'abbreviation': 'm'},
        {'name': 'Centímetro', 'abbreviation': 'cm'},
        {'name': 'Milímetro', 'abbreviation': 'mm'},
        {'name': 'Tonelada', 'abbreviation': 't'},
        {'name': 'Hectolitro', 'abbreviation': 'hl'},
        {'name': 'Decilitro', 'abbreviation': 'dl'},
        {'name': 'Centilitro', 'abbreviation': 'cl'},
        {'name': 'Par', 'abbreviation': 'par'},
        {'name': 'Dúzia', 'abbreviation': 'dz'},
        {'name': 'Saco', 'abbreviation': 'sc'},
        {'name': 'Barril', 'abbreviation': 'barril'},
        {'name': 'Rolo', 'abbreviation': 'rolo'},
        {'name': 'Fardo', 'abbreviation': 'fardo'},
        {'name': 'Pallet', 'abbreviation': 'pallet'},
        {'name': 'Conjunto', 'abbreviation': 'conj'},
        {'name': 'Kit', 'abbreviation': 'kit'},
        {'name': 'Hora', 'abbreviation': 'h'},
        {'name': 'Minuto', 'abbreviation': 'min'},
        {'name': 'Segundo', 'abbreviation': 's'},
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Remove todas as unidades existentes antes de criar as novas',
        )

    def handle(self, *args, **options):
        reset = options.get('reset', False)
        
        self.stdout.write('🚀 Iniciando criação de unidades...')
        
        companies = Company.objects.all()
        if not companies:
            self.stdout.write(self.style.ERROR('❌ Nenhuma empresa encontrada. Crie empresas primeiro.'))
            return
        
        created_count = 0
        existing_count = 0
        
        with transaction.atomic():
            if reset:
                deleted_count, _ = Unit.objects.all().delete()
                self.stdout.write(self.style.WARNING(f'🗑️  {deleted_count} unidades removidas'))
            
            for company in companies:
                for unit_data in self.DEFAULT_UNITS:
                    unit, created = Unit.objects.get_or_create(
                        company=company,
                        abbreviation=unit_data['abbreviation'],
                        defaults={'name': unit_data['name']}
                    )
                    
                    if created:
                        created_count += 1
                        self.stdout.write(f'✅ CRIADA: {unit_data["name"]} ({unit_data["abbreviation"]}) para {company.legal_name}')
                    else:
                        existing_count += 1
                        self.stdout.write(f'🔵 EXISTIA: {unit_data["name"]} ({unit_data["abbreviation"]}) para {company.legal_name}')
        
        self.stdout.write(self.style.SUCCESS(f'\n🎉 Concluído! {created_count} novas, {existing_count} existentes'))