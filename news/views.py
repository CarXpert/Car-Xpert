from django.shortcuts import render, get_object_or_404, redirect
from .models import NewsArticle
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import NewsArticleForm
from django.http import HttpResponse
from django.core import serializers
from django.utils.html import strip_tags

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
    return render(request, 'news_article_list.html', {'articles': articles})

# View untuk membuat artikel (hanya admin)
@user_passes_test(is_admin)
def create_article(request):
    if request.method == "POST":
        form = NewsArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('news:news_article_list')
    else:
        form = NewsArticleForm()
    return render(request, 'create_article.html', {'form': form})

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

