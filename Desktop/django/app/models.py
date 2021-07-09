from django.core.checks import messages
from django.db import models
from django.db.models.fields.related import ForeignKey
from account.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from ckeditor.fields import RichTextField

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=200)
    
    
    def __str__(self):
        return self.name
    
    #slugfily
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    

class BlogPost(models.Model):
    title=models.CharField(max_length=200,unique=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    image=models.ImageField(upload_to='post_image')
    body=RichTextField()
    slug=models.SlugField(max_length=200)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    category=models.ForeignKey(Category,related_name='category',on_delete=models.CASCADE)
    views=models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    
    
    def __str__(self):
        return self.title
    #slugfily
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)

class Comment(models.Model):
    post=models.ForeignKey(BlogPost,on_delete=models.CASCADE,related_name='comment')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    comment = models.TextField(max_length=500, blank=True)
    
    def __str__(self):
        return self.post.title

    def user_comment_post(instance,sender,*args, **kwargs):
        comment=instance
        post=comment.post
        sender=comment.user
        notify=Notifications(post=post,sender=sender,user=post.user,notification_type=2)
        notify.save()
#Comment
post_save.connect(Comment.user_comment_post,sender=Comment)

class Likes(models.Model):
    post=models.ForeignKey(BlogPost,on_delete=models.CASCADE,related_name='likes')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)

    def user_liked_post(sender,instance,*args, **kwargs):
        like=instance
        post=like.post
        sender=like.user
        notify=Notifications(post=post,sender=sender,user=post.user,notification_type=1)
        notify.save()

    

class Notifications(models.Model):
    NOTIFICATIONS=(
        ( 1 ,'Like'),
        ( 2 ,'Comment'),
        ( 3 ,'Register')
    )

    post=models.ForeignKey(BlogPost,related_name='notification',on_delete=models.CASCADE,blank=True,null=True)
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name='notifi_from_user')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='notifi_to_user')
    notification_type=models.IntegerField(choices=NOTIFICATIONS)
    text_prewiev=models.CharField(max_length=250,blank=True)
    date=models.DateTimeField(auto_now_add=True)
    is_seen=models.BooleanField(default=False)

    def __str__(self):
        return str(self.notification_type)

    
#Likes
post_save.connect(Likes.user_liked_post,sender=Likes)



admin=User.objects.get(email='firat.cavit@hotmail.com')
class Contact(models.Model):
    
    email=models.EmailField(max_length=250)
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    number=models.CharField(max_length=12)
    message=models.TextField()
    send_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    