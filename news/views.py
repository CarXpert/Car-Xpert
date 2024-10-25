from django.shortcuts import render, get_object_or_404, redirect
from .models import NewsArticle
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import NewsArticleForm

# Cek apakah user adalah admin
def is_admin(user):
    return user.is_staff

# View untuk menampilkan semua artikel berita
def news_article_list(request):
    articles = NewsArticle.objects.all().order_by('-published_date')  # Urutkan artikel dari yang terbaru
    featured_article = articles.first()  # Artikel yang di-highlight
    other_articles = articles[1:8]  # Ambil 7 artikel selanjutnya
    return render(request, 'news_article_list.html', {
        'featured_article': featured_article,
        'other_articles': other_articles,
    })
# View untuk membuat artikel (hanya admin)
@user_passes_test(is_admin)
def create_article(request):
    if request.method == "POST":
        form = NewsArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('news:news_article_list')  # Use namespaced URL
    else:
        form = NewsArticleForm()
    return render(request, 'create_article.html', {'form': form})

# View untuk mengedit artikel (hanya admin)
@user_passes_test(is_admin)
def edit_article(request, id):
    article = get_object_or_404(NewsArticle, id=id)
    if request.method == "POST":
        form = NewsArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('news:news_article_list')  # Use namespaced URL
    else:
        form = NewsArticleForm(instance=article)
    return render(request, 'edit_article.html', {'form': form})

# View untuk menghapus artikel (hanya admin)
@user_passes_test(is_admin)
def delete_article_direct(request, id):
    # Get the article based on the id
    article = get_object_or_404(NewsArticle, id=id)
    
    # If this is a POST request, delete the article
    if request.method == "POST":
        article.delete()
        return redirect('news:news_article_list')  # Redirect back to the news list

