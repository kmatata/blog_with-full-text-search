from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.http import Http404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
# Create your views here.
class PostListView(ListView):
    """alternate list view"""
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'post/list.html'

def post_share(request, post_id):
    post = get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url)
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject,message,settings.EMAIL_HOST_USER,[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    context = {
        "post":post,
        "form":form,
        "sent":sent,
    }
    return render(request,"post/share.html", context)

def post_lists(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list,5)
    page_nos = request.GET.get('page',1)
    try:        
        posts = paginator.page(page_nos)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        # if page_nos is out of range deliver last of page results
        posts = paginator.page(paginator.num_pages)
    return render(request,'post/list.html',{"posts":posts})

def post_detail(request, month,day,year,post):
    post = get_object_or_404(Post,slug=post,publish__month=month,publish__day=day,publish__year=year,status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(request,"post/detail.html",{"post":post,"comments":comments,"form":form})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        'post':post,
        'form':form,
        'comment':comment
    }
    return render(request, 'post/comment.html',context)




