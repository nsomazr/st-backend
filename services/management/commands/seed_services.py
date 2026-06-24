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
        'name': 'Safari & Tours',
        'slug': 'safari-and-tours',
        'description': (
            'Unforgettable wildlife safaris and guided tours across Tanzania and East Africa — '
            'Serengeti, Ngorongoro, and beyond.'
        ),
        'icon': 'binoculars',
        'image': 'https://images.unsplash.com/photo-1516426122078-c23e76319801?w=800&q=80',
        'price_from': 250,
    },
    {
        'name': 'Maasai Experience Tour',
        'slug': 'maasai-experience-tour',
        'description': (
            'Authentic Maasai cultural experiences — village visits, traditional ceremonies, '
            'and immersive day tours with local guides.'
        ),
        'icon': 'users',
        'image': 'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=800&q=80',
        'price_from': 120,
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
