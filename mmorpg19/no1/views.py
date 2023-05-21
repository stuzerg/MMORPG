from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from no1.models import post, review, newslist
from no1.forms import PostListForm, PostviewForm, ReviewForm
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django_filters import FilterSet



class SubsView(LoginRequiredMixin, TemplateView): # представление страницы подписки

    context = {}

    def get(self, request):
        print(self.get_context_data())
        return render(request, "subscribe.html",self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = newslist.objects.filter(subscriber=self.request.user).exists()
        context['status'] = status   # передача в контекст, есть ли у текущего пользователя подписка

        return context

    def post(self, request):
        if self.request.POST["wish"] == 'yes' and not newslist.objects.filter(subscriber=self.request.user).exists():
            newslist.objects.create(subscriber=self.request.user)

        if self.request.POST["wish"] == 'unsubscribe' and newslist.objects.filter(subscriber=self.request.user).exists():
            newslist.objects.get(subscriber=self.request.user).delete()

        return HttpResponseRedirect(reverse('all'))


def mail_to_send(sub, to, bod):
    send_mail(
        subject=sub,
        message=bod,
        from_email='stutzerg@yandex.ru',
        recipient_list=[to]
    )
    return


def review_action(request, pk):
    commented_post = review.objects.get(pk=pk)
    context = {'rvw': commented_post}

    if commented_post.reviewpost.user != request.user:
        print('user have not a permission to review')
        return HttpResponse('access denied')

    to_do = request.GET.get('choice')

    if to_do == 'acc':
        r = review.objects.get(pk=pk)
        r.acceptance = True
        r.save()

        print('ваш отклик принят',
              commented_post.reviewuser.email,
              f'отклик на пост {commented_post.reviewpost.header} принят пользователем {request.user}')
        mail_to_send('ваш отклик принят',
                     commented_post.reviewuser.email,
                     f'отклик на пост {commented_post.reviewpost.header} принят пользователем {request.user}')
        return HttpResponseRedirect(reverse('all'))

    if to_do == 'dny':
        r = review.objects.get(pk=pk)
        r.delete()

        print('ваш отклик удалён',
                     commented_post.reviewuser.email,
                     f'отклик на пост {commented_post.reviewpost.header} удалён пользователем {request.user}')
        mail_to_send('ваш отклик удалён',
                     commented_post.reviewuser.email,
                     f'отклик на пост {commented_post.reviewpost.header} удалён пользователем {request.user}')


    return HttpResponseRedirect(reverse('all'))


class ReviewFilter(FilterSet):
    class Meta:
        model = review

        fields = {
            'reviewuser': ['exact'],
            'reviewbody': ['icontains'],
            'acceptance': ['exact'],
            'reviewpost__staff': ['exact'],
        }


class ReviewList(ListView):
    form_class = review
    queryset = review.objects.all().order_by('-date_creation')
    template_name = 'reviews.html'
    context_object_name = 'rvws'

    # form = PostListForm()

    def get_queryset(self):
        queryset = review.objects.filter(reviewpost__user=self.request.user)

        self.filterset = ReviewFilter(self.request.GET, queryset)

        return self.filterset.qs

    #     return review.objects.filter(reviewuser=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ReviewKreator(LoginRequiredMixin, CreateView): #  создание отклика
    form_class = ReviewForm
    template_name = 'review.html'
    success_url = '/all'

    def form_valid(self, form):
        check_user = form
        check_user.instance.reviewuser = self.request.user
        check_user.instance.reviewpost = post.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


class Kreator(LoginRequiredMixin, CreateView): #  создание поста
    model = post
    template_name = 'create.html'
    fields = ['header', 'body', 'staff']
    success_url = '/all'

    def form_valid(self, form):
        check_user = form
        check_user.instance.user = self.request.user
        return super().form_valid(form)


class PostEdit(LoginRequiredMixin, UpdateView):
    model = post
    fields = ['header', 'body', 'staff']
    permission_required = ('no1.change_post',)
    template_name = 'create.html'
    success_url = '/all'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_log_user = self.request.user.pk
        print('logged user = ', User.objects.get(pk=pk_log_user).username)
        pk = self.kwargs['pk']
        print('post pk = ', self.kwargs['pk'])
        print('post belongs to', post.objects.get(pk=pk).user)
        pk_del_user = post.objects.get(pk=pk).user.pk
        if pk_del_user != pk_log_user:
            context['warning'] = '....вы не автор этого поста, вам отказано в доступе....'
            print(context)
        return context


class PostDelete(LoginRequiredMixin, DeleteView):
    model = post
    queryset = post.objects.all()
    template_name = 'kill.html'
    context_object_name = 'pst'
    success_url = '/all'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_log_user = self.request.user.pk
        print('logged user = ', User.objects.get(pk=pk_log_user).username)
        pk = self.kwargs['pk']
        print('post pk = ', self.kwargs['pk'])
        print('post belongs to', post.objects.get(pk=pk).user)
        pk_del_user = post.objects.get(pk=pk).user.pk
        if pk_del_user != pk_log_user:
            context['warning'] = '....вы не автор этого поста, вам отказано в доступе....'
            print(context)
        return context


class PostList(ListView):   # представление списка постов
    form_class = PostListForm
    queryset = post.objects.all()
    template_name = 'posts.html'
    context_object_name = 'posts'
    form = PostListForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        context['header_name'] = 'Все посты'

        if not newslist.objects.filter(subscriber=self.request.user).exists():
            context['sub_message'] = 'подписаться на рассылку новостей'
        else:
            context['sub_message'] = 'отписаться от замечательной рассылки новостей'


        return context


class Postview(DetailView):
    form_class = PostviewForm
    template_name = 'post.html'
    context_object_name = 'pst'
    form = PostviewForm()
    queryset = post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        pk= SingleObjectMixin.get_context_data(self)['object'].pk
        #
        context['revs'] = review.objects.filter(reviewpost = post.objects.get(pk=pk),acceptance = True)
        return context


class ListUserPosts(ListView): # представление списка постов одного автора
    form_class = PostListForm
    queryset = post.objects.all()
    template_name = 'posts.html'
    context_object_name = 'posts'
    form = PostListForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        context['header_name'] = 'Посты пользователя ' + User.objects.get(id=self.kwargs['pk']).username
        return context

    def get_queryset(self):
        return post.objects.filter(user_id=self.kwargs['pk'])
