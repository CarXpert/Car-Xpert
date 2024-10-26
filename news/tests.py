from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from news.models import NewsArticle
from news.views import news_article_list, create_article, edit_article, delete_article_direct, news_detail, show_json, show_xml
from django.utils import timezone


class NewsArticleModelTest(TestCase):
    def test_article_str(self):
        article = NewsArticle.objects.create(
            title="Test Article",
            content="This is a test content",
            author="Author1",
            published_date=timezone.now(),
            category="Mobil"
        )
        self.assertEqual(str(article), "Test Article")

    def test_article_category(self):
        article = NewsArticle.objects.create(
            title="Another Article",
            content="This is another test content",
            author="Author2",
            published_date=timezone.now(),
            category="Mobil Bekas"
        )
        self.assertEqual(article.category, "Mobil Bekas")


class NewsArticleListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Buat pengguna dan artikel untuk test
        cls.user = User.objects.create_user(username='testuser', password='testpass')
        cls.article1 = NewsArticle.objects.create(
            title="Article 1",
            content="Content of article 1",
            author="Author1",
            published_date=timezone.now(),
            category="Mobil"
        )
        cls.article2 = NewsArticle.objects.create(
            title="Article 2",
            content="Content of article 2",
            author="Author2",
            published_date=timezone.now(),
            category="Tips and Trick Otomotif"
        )

    def setUp(self):
        # Login sebagai pengguna sebelum setiap test dijalankan
        self.client.login(username='testuser', password='testpass')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('news:news_article_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('news:news_article_list'))
        self.assertTemplateUsed(response, 'news_article_list.html')

    def test_author_filter(self):
        response = self.client.get(reverse('news:news_article_list') + '?author=Author1')
        self.assertEqual(len(response.context['articles']), 1)
        self.assertEqual(response.context['articles'][0].author, "Author1")

    def test_category_filter(self):
        response = self.client.get(reverse('news:news_article_list') + '?category=Tips and Trick Otomotif')
        self.assertEqual(len(response.context['articles']), 1)
        self.assertEqual(response.context['articles'][0].category, "Tips and Trick Otomotif")


class ShowJsonXmlViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        NewsArticle.objects.create(
            title="JSON XML Test Article",
            content="This is test content for JSON and XML",
            author="TestAuthor",
            published_date=timezone.now(),
            category="Others"
        )

    def test_show_json(self):
        response = self.client.get(reverse('news:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_show_xml(self):
        response = self.client.get(reverse('news:show_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')


class CreateArticleViewTest(TestCase):
    def setUp(self):
        # Buat admin user dan login
        self.admin_user = User.objects.create_superuser(username='admin', password='password', email='admin@example.com')
        self.client.login(username='admin', password='password')

    def test_create_article_as_admin(self):
        response = self.client.post(reverse('news:create_article'), {
            'title': 'Admin Article',
            'content': 'Content by admin',
            'author': 'Admin Author',
            'category': 'Mobil',
        })
        self.assertEqual(response.status_code, 302)  # Redirect on successful creation
        self.assertTrue(NewsArticle.objects.filter(title="Admin Article").exists())


class NewsURLTest(TestCase):
    def test_news_article_list_url_resolves(self):
        url = reverse('news:news_article_list')
        self.assertEqual(resolve(url).func, news_article_list)

    def test_create_article_url_resolves(self):
        url = reverse('news:create_article')
        self.assertEqual(resolve(url).func, create_article)

    def test_edit_article_url_resolves(self):
        url = reverse('news:edit_article', args=[1])
        self.assertEqual(resolve(url).func, edit_article)

    def test_delete_article_url_resolves(self):
        url = reverse('news:delete_article_direct', args=[1])
        self.assertEqual(resolve(url).func, delete_article_direct)

    def test_news_detail_url_resolves(self):
        url = reverse('news:news_detail', args=[1])
        self.assertEqual(resolve(url).func, news_detail)
