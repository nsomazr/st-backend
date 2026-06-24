from django.core.management.base import BaseCommand

from services.models import Service


DEFAULT_SERVICES = [
    {
        'name': 'Travel Consultancy & Holiday Planning',
        'slug': 'travel-consultancy',
        'description': (
            'Expert travel advice and end-to-end holiday planning — personalized itineraries, '
            'packages, accommodation, activities, and transfers tailored to your trip.'
        ),
        'icon': 'compass',
        'image': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80',
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
        'name': 'Hotel Reservations',
        'slug': 'hotel-reservations',
        'description': (
            'Handpicked hotels and resorts at competitive rates. From city stays to beach '
            'retreats, we find the right room for your trip.'
        ),
        'icon': 'hotel',
        'image': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80',
        'price_from': 80,
    },
    {
        'name': 'Corporate Travels',
        'slug': 'corporate-travels',
        'description': (
            'Business travel management for companies — flights, hotels, transfers, and '
            'itineraries tailored to your corporate needs.'
        ),
        'icon': 'briefcase',
        'image': 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=800&q=80',
        'price_from': 150,
    },
    {
        'name': 'Airport Pickups & Drop Off',
        'slug': 'airport-pickups-drop-off',
        'description': (
            'Reliable airport transfers with professional drivers. Meet-and-greet pickups and '
            'comfortable drop-offs, on time every time.'
        ),
        'icon': 'car',
        'image': 'https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=800&q=80',
        'price_from': 40,
    },
    {
        'name': 'Safari, Tours & Maasai Experiences',
        'slug': 'safari-and-tours',
        'description': (
            'Wildlife safaris, guided tours, and authentic Maasai cultural experiences across '
            'Tanzania and East Africa — from Serengeti game drives to village visits.'
        ),
        'icon': 'binoculars',
        'image': 'https://images.unsplash.com/photo-1516426122078-c23e76319801?w=800&q=80',
        'price_from': 250,
    },
    {
        'name': 'Travel Insurance',
        'slug': 'travel-insurance',
        'description': (
            'Comprehensive travel insurance cover for medical emergencies, trip cancellation, '
            'lost baggage, and peace of mind abroad.'
        ),
        'icon': 'shield',
        'image': 'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=800&q=80',
        'price_from': 30,
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

        retired = Service.objects.filter(slug='holiday-planning').update(is_active=False)
        if retired:
            self.stdout.write(self.style.WARNING('Deactivated legacy service: Holiday Planning'))

        retired_maasai = Service.objects.filter(slug='maasai-experience-tour').update(is_active=False)
        if retired_maasai:
            self.stdout.write(self.style.WARNING('Deactivated legacy service: Maasai Experience Tour'))
