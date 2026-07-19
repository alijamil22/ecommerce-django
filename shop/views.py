from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category


def home(request):
    products = Product.objects.filter(available=True)[:8]
    mobile_products = Product.objects.filter(category__name='Mobile Phone', available=True)
    tablet_products = Product.objects.filter(category__name='Tablet', available=True)
    return render(request, 'shop/index.html', {
        'products': products,
        'mobile_products': mobile_products,
        'tablet_products': tablet_products,
    })


def product_list(request):
    queryset = Product.objects.filter(available=True).order_by('name')
    paginator = Paginator(queryset, 8)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'shop/product.html', {
        'page_obj': page_obj,
        'products': page_obj.object_list,
    })


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    queryset = Product.objects.filter(category=category, available=True).order_by('name')
    paginator = Paginator(queryset, 8)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'shop/product.html', {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'current_category': category,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'shop/product_detail.html', {
        'product': product,
    })


def search(request):
    query = request.GET.get('q', '')
    queryset = Product.objects.filter(available=True).order_by('name')
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    paginator = Paginator(queryset, 8)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'shop/search_results.html', {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'query': query,
    })
