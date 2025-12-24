import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommarce.settings')
django.setup()

from myapp.models import Product

print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"MEDIA_URL: {settings.MEDIA_URL}")

for p in Product.objects.all():
    print(f"Product: {p.name} (ID: {p.id})")
    if p.image:
        print(f"  Field Value: {p.image}")
        print(f"  URL: {p.image.url}")
        full_path = os.path.join(settings.MEDIA_ROOT, str(p.image))
        exists = os.path.exists(full_path)
        print(f"  Full Path: {full_path}")
        print(f"  Exists: {exists}")
    else:
        print("  No Image")
    print("-" * 20)
