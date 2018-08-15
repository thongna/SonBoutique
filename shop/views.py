from django.shortcuts import render, get_object_or_404
from .models import Category, Product, ProductImage, Comment, Banner
from .forms import CommentForm
from taggit.models import Tag
from django.db.models import Count
from cart.forms import CartAddProductForm

# Show product list

def  product_list(request, category_slug=None, tag_slug=None):
    category = None
    tag = None
    title_id = 0

    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        title_id = 1

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
        title_id = 2

    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'tag': tag,
                   'title_id': title_id})


def home(request):
    banners = Banner.objects.filter(active=True)
    products = Product.objects.filter(available=True)[:4]
    return render(request, 'shop/index.html',
                  {'products': products,
                   'banners': banners})

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