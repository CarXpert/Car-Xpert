from django.shortcuts import render, get_object_or_404, redirect
from .models import NewsArticle
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import NewsArticleForm
from django.http import HttpResponse
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

# Cek apakah user adalah admin
def is_admin(user):
    return user.is_staff

# Fungsi untuk mengembalikan semua artikel dalam format XML
def show_xml(request):
    articles = NewsArticle.objects.all()
    return HttpResponse(serializers.serialize("xml", articles), content_type="application/xml")

# Fungsi untuk mengembalikan semua artikel dalam format JSON
def show_json(request):
    articles = NewsArticle.objects.all()
    return HttpResponse(serializers.serialize("json", articles), content_type="application/json")

# Fungsi untuk mengembalikan artikel berdasarkan id dalam format XML
def show_xml_by_id(request, id):
    article = NewsArticle.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", article), content_type="application/xml")

# Fungsi untuk mengembalikan artikel berdasarkan id dalam format JSON
def show_json_by_id(request, id):
    article = NewsArticle.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", article), content_type="application/json")

# View untuk menampilkan semua artikel berita dalam HTML
@login_required(login_url='/auth/login/')
def news_article_list(request):
    articles = NewsArticle.objects.all()
    author = request.GET.get('author')
    category = request.GET.get('category')
    
    if author:
        articles = articles.filter(author=author)
    if category and category != 'Semua':
        articles = articles.filter(category=category)

    authors = NewsArticle.objects.values_list('author', flat=True).distinct()
    categories = [choice[0] for choice in NewsArticle.CATEGORY_CHOICES]

    context = {
        'articles': articles,
        'authors': authors,
        'categories': categories,
    }
    return render(request, 'news_article_list.html', context)

# View untuk membuat artikel (hanya admin) 
@csrf_exempt
@user_passes_test(is_admin)
def create_article(request):
    if request.method == "POST":
        form = NewsArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": True})
            else:
                return redirect("news:news_article_list")
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": False, "error": form.errors})
            else:
                return render(request, "create_article.html", {"form": form})
    else:
        form = NewsArticleForm()
    return render(request, "create_article.html", {"form": form})


# View untuk mengedit artikel (hanya admin)
@user_passes_test(is_admin)
def edit_article(request, id):
    article = get_object_or_404(NewsArticle, id=id)
    form = NewsArticleForm(request.POST or None, request.FILES or None, instance=article)
    if form.is_valid():
        form.save()
        return redirect('news:news_article_list')
    return render(request, 'edit_article.html', {'form': form})

# View untuk menghapus artikel (hanya admin)
@user_passes_test(is_admin)
def delete_article_direct(request, id):
    article = get_object_or_404(NewsArticle, id=id)
    if request.method == "POST":
        article.delete()
        return redirect('news:news_article_list')

# Detail artikel dalam format HTML
def news_detail(request, id):
    article = get_object_or_404(NewsArticle, id=id)
    return render(request, 'news_detail.html', {'article': article})

@csrf_exempt
def add_article_api(request):
    if request.method == "POST":
        if 'image' in request.FILES:
            image = request.FILES['image']
            if not image.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                return JsonResponse({
                    "success": False,
                    "errors": {
                        "image": ["Invalid image format. Please use PNG, JPG, JPEG, or GIF."]
                    }
                }, status=400)
       
        form = NewsArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            image_url = None
            if article.image:
                image_url = f"http://127.0.0.1:8000/{article.image.url}"
           
            return JsonResponse({
                "success": True,
                "id": article.id,
                "image_url": image_url,  # Changed from image_name to image_url
                "message": "Article successfully created"
            })
        else:
            return JsonResponse({
                "success": False,
                "errors": dict(form.errors)
            }, status=400)
    return JsonResponse({"message": "Invalid request method"}, status=405)


@csrf_exempt
def edit_article_api(request, id):
    article = get_object_or_404(NewsArticle, id=id)
    if request.method == "PUT":
        data = json.loads(request.body.decode('utf-8'))
        form = NewsArticleForm(data, instance=article)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": form.errors}, status=400)
    return JsonResponse({"message": "Invalid request method"}, status=405)

@csrf_exempt
def delete_article_api(request, id):
    article = get_object_or_404(NewsArticle, id=id)
    if request.method == "DELETE":
        article.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"message": "Invalid request method"}, status=405)
