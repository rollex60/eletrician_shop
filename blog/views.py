import calendar

from calendar import HTMLCalendar
from django import views
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.views.generic.edit import FormMixin
from flask.json import tag
from taggit.models import Tag

from blog.models import Blog, Comment
from electric.mixins import CartMixin, NotificationsMixin, TagMixin, TagMixinBlog
from electric.models import Electric
from electric.utils import menu
from blog.forms import CommentsForm

from shop.models import Customer, Notification, Cart


class BlogDetailView(CartMixin, NotificationsMixin, views.generic.DetailView):
    # ----Blog-----------------------------------------------------------------------------------------
    
    model = Electric
    template_name = 'blog/blog.html'
    context_object_name = 'blog'
    paginate_by = 2

    def get(self, request, blog=None, *args, **kwargs):
        tages = Blog.tages.annotate(blog_count=Count('tages'))
        contact_list = Blog.objects.all()
        paginator = Paginator(contact_list, 2)

        page_number = request.GET.get('page')
        blog = paginator.get_page(page_number)
        page_obj = paginator.get_page(page_number)


        return render(request, 'blog/blog.html',
                      {"cart": self.cart,
                       'tages_selected':0,
                       'blog': blog,
                       'page_obj': page_obj,
                       'tages': tages,
                       'menu': menu,
                       'tag': tag,
                       'notifications': self.notifications(request.user)})

    def get_tags(self):
        tages = []

        for tag in self.tages.all():
            tages.append(str(tag))
        return ', '.join(tages)


    def tagg(request, slug):
        tag = get_object_or_404(Tag, slug=slug)
        tages = Blog.tages.annotate(blog_count=Count('tages'))

        context = {
            'tag': tag,
            'tages': tages,
        }
        return render(request, 'blog/blog.html', context)


class TagBlogView(TagMixinBlog, ListView):

    model = Blog
    paginate_by = '3'
    context_object_name = 'blog'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['tag'] = str(context['tages'][0].slug)


        context['tages_selected'] = context['tages'][0].slug
        return context


    def get_queryset(self):
        return Blog.objects.filter(tages__slug=self.kwargs.get('tag_slug'))


class BlogPost(CartMixin, NotificationsMixin, FormMixin, views.generic.DetailView):
    # ----Blog Post--------------------------------------------------------------------------------------
    
    model = Blog
    template_name = 'blog/blogpost.html'
    slug_url_kwarg = 'blogpost_slug'
    context_object_name = 'blogpost'
    form_class = CommentsForm
    success_msg = 'Comment successfully created, please wait for moderation'

    def get_success_url(self, **kwargs):
        return reverse_lazy('blogpost', kwargs={'blogpost_slug': self.get_object().slug})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.article = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = context['blogpost']
        context['menu'] = menu
        context['similar_posts'] = self.object.tages.similar_objects()[:4]
        context['blog_selected'] = 0,
        context['tages_selected'] = 0,
        return context

    def tagg(request, slug):
        tag = get_object_or_404(Tag, slug=slug)
        # Filter posts by tag name
        blog = Blog.objects.filter(tages=tag)
        context = {
            'tag': tag,
            'blog': blog,
        }
        return render(request, 'blog/blogpost.html', context)


class SearchResultsBlogView(ListView):
    # Form Search-----------------------------------------------------------------------
    
    model = Blog
    template_name = "blog/blog.html"
    context_object_name = 'blog'
    paginate_by = 2

    @staticmethod
    def notifications(user):
        if user.is_authenticated:
            return Notification.objects.all(user.customer)
        return Notification.objects.none()

    def get_queryset(self):

        if self.request.GET.get('val'):
            value = self.request.GET.get('val')
            queryset = Blog.objects.filter(Q(name__contains=value) | Q(content__contains=value))
        else:
            queryset = Blog.objects.all()
        return queryset

    def list(request):
        contact_list = Blog.objects.all()
        paginator = Paginator(contact_list, 6)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'blog/blog.html', {'page_obj': page_obj})

    def dispatch(self, request, *args, **kwargs):
        cart = None
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(
                    user=request.user
                )
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        val = self.request.GET.get('val')
        tages = Blog.tages.annotate(blog_count=Count('tages'))

        context['search-blog'] = val
        context['menu'] = menu
        context['notifications'] = self.notifications(self.request.user)
        context['cart'] = self.cart
        context['tages'] = tages
        return context




class BlogCategory(TagMixinBlog, ListView):
    # ----Blog Category----------------------------------------------------------------------------
    
    paginate_by = 9
    model = Blog
    template_name = 'blog/blog.html'
    context_object_name = 'blog'

    @staticmethod
    def notifications(user):
        if user.is_authenticated:
            return Notification.objects.all(user.customer)
        return Notification.objects.none()

    def dispatch(self, request, *args, **kwargs):
        cart = None
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(
                    user=request.user
                )
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = str(context['blog'][0].blog)
        context['notifications'] = self.notifications(self.request.user)
        context['cart'] = self.cart
        context['menu'] = menu
        context['tag'] = tag
        context['blog_selected'] = context['blog'][0].blog_id
        return context

    def get_queryset(self):
        return Blog.objects.filter(blog__slug=self.kwargs['blog_slug'], is_published=True)


def updated_comments_status(request, pk, type):
    # ----Update comments-------------------------------------------------------------------------------
    
    item = Comment.objects.get(pk=pk)

    if type == 'public':
        import operator
        item.status = operator.not_(item.status)
        item.save()
        template = 'blog/comment_blog.html'
        context = {'item': item, 'status_comment': 'Comment published'}
        return render(request, template, context)

    elif type == 'delete':
        item.delete()
        return HttpResponse('''
            <div class="alert alert-success">
            Comment has been deleted
            </div>
            ''')

    return HttpResponse('1')