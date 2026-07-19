"""
Run: python create_sample_data.py

Creates sample categories and products for the store.
Uses images from static/img/ copied into media/products/.
"""
import os
import sys
import shutil
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from shop.models import Category, Product

# Clear existing data
Product.objects.all().delete()
Category.objects.all().delete()

MEDIA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'products')
STATIC_IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'img')
os.makedirs(MEDIA_DIR, exist_ok=True)

# Create categories
categories_data = ['Mobile Phone', 'Tablet', 'Laptop']
categories = {}
for name in categories_data:
    slug = name.lower().replace(' ', '-')
    cat = Category.objects.create(name=name, slug=slug)
    categories[name] = cat
    print(f'  Created category: {name}')

# Products: (name, slug, category, price, compare_price, stock, image_static_name, description)
products_data = [
    ('iPhone 6s Plus 16GB', 'iphone-6s-plus-16gb', 'Mobile Phone', 649.00, 739.00, 50,
     'iphone.png', '3D Touch. 12MP photos. 4K video. The most advanced iPhone ever.'),
    ('iPhone SE 32/64GB', 'iphone-se-32-64gb', 'Mobile Phone', 499.00, 599.00, 30,
     'iphone-se.png', 'A big step for small. A beloved design. Now with more to love.'),
    ('Samsung Galaxy Note 5', 'samsung-galaxy-note-5', 'Mobile Phone', 599.00, 799.00, 25,
     'samsung-note5.png', 'Super. Computer. Now in two sizes.'),
    ('Samsung Galaxy S7 Edge', 'samsung-galaxy-s7-edge', 'Mobile Phone', 799.00, 999.00, 20,
     'samsung-s7-edge.jpg', 'Redefine what a phone can do with the Galaxy S7 edge.'),
    ('9.7-inch iPad Pro 32GB', '9-7-inch-ipad-pro-32gb', 'Tablet', 649.00, 739.00, 35,
     'ipad-pro.png', 'Super. Computer. Now in two sizes. Stunning Retina display.'),
    ('iPad Air 2 32/64GB', 'ipad-air-2-32-64gb', 'Tablet', 399.00, 459.00, 40,
     'ipad-air.png', 'Light. Heavyweight. The thinnest, most powerful iPad ever.'),
    ('MacBook Pro with Retina Display', 'macbook-pro-retina', 'Laptop', 1299.00, 1499.00, 15,
     'macbook-pro.png', 'Stunning Retina Display. The best Mac notebook ever.'),
]

print()
for name, slug, cat_name, price, compare_price, stock, img_name, desc in products_data:
    # Copy image from static/img to media/products
    src = os.path.join(STATIC_IMG, img_name)
    dst = os.path.join(MEDIA_DIR, img_name)
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.copy2(src, dst)
        print(f'  Copied image: {img_name}')
    elif os.path.exists(dst):
        print(f'  Image already exists: {img_name}')
    else:
        print(f'  WARNING: Source image not found: {src}')

    product = Product.objects.create(
        name=name,
        slug=slug,
        category=categories[cat_name],
        description=desc,
        price=price,
        compare_price=compare_price,
        image=f'products/{img_name}',
        stock=stock,
        available=True,
    )
    print(f'  Created product: {name} (${price})')

print()
print(f'Done! Created {Category.objects.count()} categories and {Product.objects.count()} products.')
