from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def home(request):
    products = Product.objects.filter(available=True)[:8]
    categories = Category.objects.all()
    mobile_products = Product.objects.filter(category__name='Mobile Phone', available=True)
    tablet_products = Product.objects.filter(category__name='Tablet', available=True)
    return render(request, 'shop/index.html', {
        'products': products,
        'categories': categories,
        'mobile_products': mobile_products,
        'tablet_products': tablet_products,
    })


def product_list(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    return render(request, 'shop/product.html', {
        'products': products,
        'categories': categories,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'shop/product_detail.html', {
        'product': product,
    })
