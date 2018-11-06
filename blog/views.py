from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, resolve_url
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from rest_framework.renderers import JSONRenderer
from .forms import CommentForm
from .models import Post, Comment
from .serializers import PostSerializer


class PostListView(ListView):
    model = Post
    paginate_by = 5

    def get_template_names(self): #리스트뷰에서 사용하는 함수의 종류중 하나
        if self.request.is_ajax(): #참 or 거짓을 리턴한다.ajax요청시 x-requested-with헤더에 xmlhttprequest값이 전달되는지 확인해줌.
            return ['blog/_post_list.html'] #ajax할떈 이템플릿으로 랜더링.
        return ['blog/index.html']

index = PostListView.as_view()





post_new = CreateView.as_view(model=Post, fields=['title', 'content'])






class PostDetailView(DetailView):
    model = Post

    def render_to_response(self, context):
        if self.request.is_ajax():
            return JsonResponse({
                'title': self.object.title,
                'summary': truncatewords(self.object.content, 100), #truncatewords쓰면 전체글이 아니라 요약된 100단어만 몇글자만..
            })
        # 템플릿 렌더링
        return super().render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm() #comment_form이라는 이름으로 모델폼의 인스턴스를 넘겨줌.
        return context

post_detail = PostDetailView.as_view()







post_edit = UpdateView.as_view(model=Post, fields='__all__')






class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')

post_delete = PostDeleteView.as_view()






class CommentListView(ListView):
    model = Comment

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(post__id=self.kwargs['post_pk'])

        latest_comment_id = self.request.GET.get('latest_comment_id', None)
        if latest_comment_id:
            qs = qs.filter(id__gt=latest_comment_id)
        return qs


comment_list = CommentListView .as_view()






class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        response = super().form_valid(form)

        if self.request.is_ajax(): # render_to_response가 호출되지 않습니다.
            return render(self.request, 'blog/_comment.html', {
                'comment': comment,
            })

        return response


    def get_success_url(self):
        return resolve_url(self.object.post)

    def get_template_names(self):
        if self.request.is_ajax():
            return ['blog/_comment_form.html']
        return ['blog/comment_form.html']

comment_new = CommentCreateView.as_view()





class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.is_ajax(): # render_to_response가 호출되지 않습니다.
            return render(self.request, 'blog/_comment.html', {
                'comment': self.object,
            })

        return response

    def get_success_url(self):
        return resolve_url(self.object.post)

    def get_template_names(self):
        if self.request.is_ajax():
            return ['blog/_comment_form.html']
        return ['blog/comment_form.html']

comment_edit = CommentUpdateView.as_view()






class CommentDeleteView(DeleteView):
    model = Comment

    def get_success_url(self):
        return resolve_url(self.object.post)

comment_delete = CommentDeleteView.as_view()






#cbv
# class CommentLikeView(UpdateView):
#     model = Comment
#     form_class = CommentForm
#
#     def form_valid(self, form):
#         response = super().form_valid(form)
#
#         if self.request.is_ajax(): # render_to_response가 호출되지 않습니다.
#             return render(self.request, 'blog/_comment.html', {
#                 'comment': self.object,
#             })
#
#         return response
#
#     def get_success_url(self):
#         return resolve_url(self.object.post)
#
#     def get_template_names(self):
#         if self.request.is_ajax():
#             return ['blog/_comment_form.html']
#         return ['blog/comment_form.html']
#
# comment_like = CommentLikeView.as_view()

@login_required
#@require_POST
def comment_like(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user in comment.like_users.all():
        comment.like_users.remove(request.user)
        print("있음")
    else:
        comment.like_users.add(request.user)
        print("없음")
    comment.like_count = comment.like_users.count()
    comment.save()
    return JsonResponse({'ok': True, 'comment_count': comment.like_count}, safe=False)


def post_list_json(request):
    qs = Post.objects.all()

    serializer = PostSerializer(qs, many=True) #시리얼라이저 할때 매니트루 꼭해준다,
    json_utf8_string = JSONRenderer().render(serializer.data)

    return HttpResponse(json_utf8_string, content_type='application/json; charset=utf-8') # 커스텀 지정





# 좋아요 취소는 안되는거
# @login_required
# # @require_POST
# def post_like(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.like_users.add(request.user)
#     post.like_count = post.like_users.count()
#     post.save()
#     return JsonResponse({'ok': True, 'like_count': post.like_count}, safe=False)

@login_required
#@require_POST 되는거
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
        print("있음")
    else:
        post.like_users.add(request.user)
        print("없음")
    post.like_count = post.like_users.count()
    post.save()
    return JsonResponse({'ok': True, 'like_count': post.like_count}, safe=False)



#
# @login_required
# #@require_POST
# def post_like(request, pk):
#     if request.method=='POST':
#         user = request.user
#         like_users = request.POST.get('pk', None)
#         memo = Post.objects.get(pk=like_users)
#
#         if memo.like_users.filter(id=user.id).exists():
#             memo.like_users.remove(user)
#             message='you cant'
#         else :
#             memo.like_users.add(user)
#             message= 'connect'
#         memo.like_count = memo.like_users.count()
#         memo.save()
#         return JsonResponse({'ok': True, 'like_count': memo.like_count}, safe=False)
#
#



