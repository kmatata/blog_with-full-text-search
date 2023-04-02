from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.http import Http404,JsonResponse
from django.db.models import Count
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector,SearchQuery, SearchRank, TrigramSimilarity
import json
from collections import defaultdict
from django.views.decorators.csrf import csrf_exempt
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

def post_lists(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None    
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list,5)
    page_nos = request.GET.get('page',1)
    try:        
        posts = paginator.page(page_nos)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        # if page_nos is out of range deliver last of page results
        posts = paginator.page(paginator.num_pages)
    return render(request,'post/list.html',{"posts":posts,"tag":tag})

def post_detail(request, month,day,year,post):
    post = get_object_or_404(Post,slug=post,publish__month=month,publish__day=day,publish__year=year,status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)
    form = CommentForm()

    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:5]

    return render(request,"post/detail.html",{"post":post,"comments":comments,"form":form,'similar_posts':similar_posts})

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
@csrf_exempt
def post_search(request):
    data = json.loads(request.body)
    searchRslts = defaultdict(list) 
    query = data['postsSearch']   
    #search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
    #search_query = SearchQuery(query)
    #postSearches = Post.published.annotate(search=search_vector,rank=SearchRank(search_vector,search_query)).filter(rank__gte=0.2).order_by('-rank')
    postSearches = Post.published.annotate(similarity=TrigramSimilarity('title', query),).filter(similarity__gte=0.1).order_by('-similarity')
    #psts = postSearches.values_list('title',flat=True)
    #pstids = list(postSearches.values_list('id',flat=True))
    for pst in postSearches:
        #actpst = Post.objects.get(id=pst).get_absolute_url()
        actpst = pst.get_absolute_url()
        url = request.build_absolute_uri(actpst)
        searchRslts['results'].append({'url':url})
        searchRslts['results'].append({'title':pst.title})            
        #for ps in psts:
        #    searchRslts['results'].append({'title':ps})            
    
     
    #aftQuery = json.dumps(listRslts,allow_nan=True)
    return JsonResponse(searchRslts,safe=False)

