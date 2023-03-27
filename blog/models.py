from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from PIL import Image
from django.urls import reverse


# Create your models here.

def blog_image_dir_path(instance, filename):
    imgageFile = filename.split('.')
    try:
        if (imgageFile[-1] == 'jpeg'):
            image_ext = '.jpeg'
        elif (imgageFile[-1] == 'png'):
            image_ext = '.png'
        elif (imgageFile[-1] == 'jpg'):
            image_ext = '.jpg'
        image_ext_name = 'user_{0}/postImage{1}'.format(instance.author.id,image_ext)
    except Exception as e:
        raise e
    
    return image_ext_name


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)    
    body = models.TextField()
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250,unique_for_date='publish')
    status = models.CharField(max_length=2,choices=Status.choices,default=Status.DRAFT)
    objects = models.Manager()
    published = PublishedManager()
    postImage = models.ImageField(upload_to=blog_image_dir_path,default=None,null=True,blank=True)
        
    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super().save(*args,**kwargs)        
        SIZE = 630,1024
        if self.postImage:
            img = Image.open(self.postImage.path)
            img.thumbnail(size=(SIZE))
            img.save(self.postImage.path,optimize=True,qulaity=90)

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]  

    @property
    def summary(self):
        return self.body[:50] + ' ...'

    @property
    def get_absolute_url(self):
        return reverse("blog:post_detail",args=[self.publish.month,self.publish.day,self.publish.year,self.slug])

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"

    