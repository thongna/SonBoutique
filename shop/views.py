from django.shortcuts import render, get_object_or_404
from .models import Category, Product, ProductImage, Comment, Banner
from .forms import CommentForm
from taggit.models import Tag
from django.db.models import Count, Q
from cart.forms import CartAddProductForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Show product list
def  product_list(request, id=None, tag_slug=None, best_saled=None):
    tag = None
    title = 'HÀNG MỚI VỀ'
    product_list = Product.objects.filter(available=True)

    search = request.GET.get('q')
    if search:
        product_list = product_list.filter(Q(name__contains=search.upper()) | Q(name__contains=search.lower()) | Q(product_code__contains=search))
        title = 'SẢN PHẨM TÌM KIẾM THEO "{}"'.format(search)
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        product_list = product_list.filter(tags__in=[tag])
        title = 'Danh sách sản phẩm với ' + tag.name
    if id:
        categories = Category.objects.filter(parent_id=id)
        product_list = product_list.filter(category__in=categories)
        title = '{}'.format(Category.objects.get(id=id).name)

    # get 2 pages of list of best saled products
    if best_saled:
        product_list = product_list.order_by('-saled')[:24]
        title = 'Sản phẩm bán chạy nhất'

    paginator = Paginator(product_list, 12)  # 12 products in each page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        products = paginator.page(paginator.num_pages)

    return render(request,
                  'shop/product/list.html',
                  {'products': products,
                   'tag': tag,
                   'title': title})

def category(request, category_slug=None):
    category = None
    categories = Category.objects.exclude(parent_id=0)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        product_list = Product.objects.filter(available=True, category=category)

    paginator = Paginator(product_list, 12)  # 12 products in each page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        products = paginator.page(paginator.num_pages)

    # get tags in category and remove duplicate
    tags = []
    for product in products:
        for tag in product.tags.all():
            if tag not in tags:
                tags.append(tag)

    # best saled
    best_saled_products = product_list.order_by('-saled')[:2]

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'tags': tags,
        'best_saled_products': best_saled_products,
    }


    return render(request, 'shop/product/category.html', context)


def home(request):
    banners = Banner.objects.filter(active=True)
    products = Product.objects.filter(available=True)
    best_saled_products = products.order_by('-saled')[:4]
    products = products[:4]

    context = {
        'products': products,
        'best_saled_products': best_saled_products,
        'banners': banners
    }
    return render(request, 'shop/index.html', context)

# Show product detail
def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()

    #List of active comments for this product
    comments = product.comments.filter(active=True)

    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.product = product
            new_comment.save()
    else:
        comment_form = CommentForm()

    product_images = product.images.all()

    # List of related products
    product_tags_ids = product.tags.values_list('id', flat=True)
    related_products = Product.objects.filter(tags__in=product_tags_ids).exclude(id=product.id)
    related_products = related_products.annotate(same_tags=Count('tags')).order_by('-same_tags')[:8]
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'product_images': product_images,
                   'cart_product_form': cart_product_form,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'related_products': related_products})

def collection_list(request):
    collections = Category.objects.filter(parent_id=0)

    context = {
        'collections': collections
    }
    return render(request, 'shop/collection/collection_list.html', context)