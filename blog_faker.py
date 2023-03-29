import django
django.setup()
from django.contrib.auth.models import User
from blog.models import Post
import os
from faker import Faker
from django.conf import settings
#import shutil
from django.utils.crypto import get_random_string
from image_resize import image_resize
import cv2
from taggit.models import Tag

fake = Faker()
def add_fst_lst_name():
    user = User.objects.get(id=1)
    return user

#filePth = '/Users/mac/Downloads/standardized/'
#imgPath = list(filePth + str(x) for x in os.listdir(filePth))

#imglist = os.path.join(settings.BASE_DIR, "blogSite/media/user_1/")
#imgPath = list(x for x in os.listdir(imglist))

#for img in imgPath:    
    #ext = img.split('.')
    #imgSize = cv2.imread(img,cv2.IMREAD_UNCHANGED)
    #directory = os.path.join(settings.BASE_DIR, "blogSite/media/user_1/") 
    #imgFile = f"postImage{get_random_string(5)}.{ext[-1]}"
    #resized = image_resize(imgSize,height=630)
    #os.chdir(directory)
    #cv2.imwrite(imgFile,imgSize)
    #shutil.copyfile(img,newPth)   
    #post = Post(author=add_fst_lst_name(),title=fake.sentence()[:250],
    #            body=fake.text()[:2000],status='PB')        
    #post.postImage = f"user_1/{img}"    
    #post.save()
import random
tags = Tag.objects.all().values_list('name',flat=True)
for _ in range(41):
    post = Post.objects.all()[_]
    post.tags.add(random.choice(tags),random.choice(tags))
    post.save()
