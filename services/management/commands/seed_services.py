from django.core.management.base import BaseCommand

from services.models import Service


DEFAULT_SERVICES = [
    {
        'name': 'Travel Consultancy',
        'slug': 'travel-consultancy',
        'description': (
            'Expert travel advice tailored to your needs. We help you plan the perfect '
            'itinerary, choose destinations, and make informed travel decisions.'
        ),
        'icon': 'compass',
        'image': 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&q=80',
        'price_from': 50,
    },
    {
        'name': 'Air Ticketing',
        'slug': 'air-ticketing',
        'description': (
            'Competitive airfares on domestic and international flights. We search multiple '
            'airlines to find the best routes and prices for your journey.'
        ),
        'icon': 'plane',
        'image': 'https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=800&q=80',
        'price_from': 100,
    },
    {
        'name': 'Visa Documentation Assistance',
        'slug': 'visa-documentation-assistance',
        'description': (
            'Complete visa application support including document preparation, form filling, '
            'and submission guidance for destinations worldwide.'
        ),
        'icon': 'file-text',
        'image': 'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=800&q=80',
        'price_from': 75,
    },
    {
        'name': 'Holiday Planning',
        'slug': 'holiday-planning',
        'description': (
            'End-to-end holiday packages including accommodation, activities, and transfers. '
            'Let us craft your dream vacation from start to finish.'
        ),
        'icon': 'palmtree',
        'image': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80',
        'price_from': 200,
    },
]


class Command(BaseCommand):
    help = 'Seed default travel services'

    def handle(self, *args, **options):
        created_count = 0
        for data in DEFAULT_SERVICES:
            _, created = Service.objects.update_or_create(
                slug=data['slug'],
                defaults=data,
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created: {data["name"]}'))
            else:
                self.stdout.write(f'Updated: {data["name"]}')

        self.stdout.write(self.style.SUCCESS(f'Done. {created_count} new services created.'))
