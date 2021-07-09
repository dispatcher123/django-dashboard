
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404 , redirect
from .models import *
from app.decorators import only_admin
from django.db.models import Count
from account.models import *
from datetime import datetime
from datetime import datetime, timedelta
from django.db.models.functions import TruncDay
from django.conf import settings
from django.db.models.functions import ExtractMonth,ExtractDay
from django.utils import timezone
from account.forms import RegistrationForm
from django.contrib import messages, auth
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import ContactForm, PostForm,CommentForm
# Create your views here.

#Verification Email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import stripe

stripe.api_key='sk_test_51JAExNCbKiyyexfdkXljLo7D1ujo55kqJngYWQkIbybPoqkM8O4Eo3F7ktiC67qrsnI5YStCWAokPfbN7YXlOPZa00T0UOKmav'



    
    

def notifications(request):
    user=request.user
    notifications=Notifications.objects.filter(user=user).order_by('-date')
    Notifications.objects.filter(user=user,is_seen=False).update(is_seen=True)
    return render(request, 'noti.html',context={
        'notifications': notifications
    })
def count_notification(request):
    count_notification=0
    if request.user.is_authenticated:
        count_notification=Notifications.objects.filter(user=request.user,is_seen=False).count()
    return {'count_notification' : count_notification}


    
############## REGISTER , LOGIN , LOGOUT ####################
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password=form.cleaned_data['confirm_password']
            username = email.split("@")[0]
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.save()
            print(user)
            
            #USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('verification.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            #messages.success(request, "Thank You! We have sent a verification email to your email.Please verify it.")
            return redirect("/login/?command=verification&email="+email)
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)

def login(request):
    
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        print(email, password)
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("homepage")
        else:
            messages.error(request, "Login Invalid")
            return render(request, "login.html", 
                {"message":"User does not exist."})

    return render(request, "login.html")
@login_required(login_url='userpage/')
def logout(request):
    auth.logout(request)
    messages.success(request,'You Logged Out Succesful')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')

def forgetpassword(request):
    if request.method=='POST':
        email=request.POST['email']
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email__exact=email)
            #reset password
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('reset_password.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, "Password reset email has been sent to your email!")
            return redirect("/login/?command=verification&email="+email)

        else:
            messages.error(request,'Email Does Not Exist!')
            return redirect('forgetpassword')
    return render(request, 'forgetpassword.html', context={})
    
def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid']= uid
        messages.success(request,'Please Reset Your Password')
        return redirect('resetpassword')
    else:
        messages.error(request,'This link has been expired!')
        return redirect('login')

def resetpassword(request):
    if request.method=="POST":
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password == confirm_password:
            uid= request.session.get('uid')
            user= User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            return redirect('login')
        else:
            messages.errror(request,'Password Does Not Match!')
    else:
        return render(request, 'resetpassword.html',context={})
    


################# DATA START #####################
last_month = datetime.now() - timedelta(days=1)
@only_admin
def admin_dashboard(request):
    posts=BlogPost.objects.all()
    users=User.objects.all()
    comments=Comment.objects.all()
    comment_count=comments.count()
    users_count=users.count()
    posts_count=posts.count()
    posts_views_counts=BlogPost.objects.annotate(Count('comment')).order_by('-comment__count')[:5]
    joined_details = User.objects.filter(joined_date__gte=last_month).values('joined_date').count()
    offline_users=User.objects.filter(is_active=False).count()
    online_users=User.objects.filter(is_active=True).count()
    return render(request, 'dashboard.html',context={
        'posts':posts,
        'users' : users,
        'comments' : comments,
        'users_count':users_count,
        'posts_count' : posts_count,
        'posts_views_counts' : posts_views_counts,
        'comment_count' : comment_count,
        'posts_views_counts' : posts_views_counts,
        'joined_details' : joined_details,
        'offline_users' : offline_users,
        'online_users' : online_users,
    })
@only_admin
def post_detail(request,slug,postslug):
    category=get_object_or_404(Category,slug=slug)
    posts=BlogPost.objects.get(category=category,slug=postslug)
    return render(request, 'post_details.html',context={
        'posts':posts
    })
@only_admin
def user_detail(request,id):
    users=User.objects.get(id=id)
    return render(request,'users_detail.html',context={
        'users' : users,
    })
import time
from django.db import connection
@only_admin
def pie_chart(request):
    labels = []
    data = []
    g=[]
    total=[]
    sex=[]
    all_total=[]
    statuses=[]
    status_total=[]
    month=[]
    days=[]
    total_login=[]
    this_year = time.strftime("%Y", time.localtime(time.time()))
    this_month = time.strftime("%m", time.localtime(time.time()))
    select = {'day': connection.ops.date_trunc_sql('day', 'joined_date')}
    count_data =User.objects.filter(joined_date__year=this_year, joined_date__month=this_month).extra(
        select=select).values('day').annotate(number=Count('id'))
    print(count_data)
    x_list = []
    y_list = []
    for i in count_data:
        x_list.append(i['day'])
        y_list.append(i['number'])
        
    chart_data = (
            User.objects.annotate(date=TruncDay("joined_date"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )
    print(chart_data)
    
    
    
    # check to be sure
    months=User.objects.annotate(month=ExtractDay('joined_date')).values('month').annotate(experiments=Count('is_active')).values('month')
    
    dayss=User.objects.annotate(day=ExtractMonth('joined_date')).values('day').annotate(experiments=Count('is_active')).values('day')
    for i in dayss:
        days.append(i['day'])
    #######
    total_users=User.objects.annotate(month=ExtractDay('joined_date')).values('month').annotate(experiments=Count('is_active')).values('experiments')
    for i in total_users:
        total_login.append(i['experiments'])
    systems=Comment.objects.values('post__title').annotate(count=Count('comment'))
    for i in systems:
        g.append(i['post__title'])
        total.append(i['count'])
    
    
    queryset = BlogPost.objects.order_by('-views')[:5]
    for a in queryset:
        labels.append(a.title)
        data.append(a.views)

    genders=User.objects.values('gender').annotate(count=(Count('gender')))
    for i in genders:
        sex.append(i['gender'])
        all_total.append(i['count'])
        
    status=User.objects.values('status').annotate(count=(Count('status')))
    for i in status:
        statuses.append(i['status'])
        status_total.append(i['count'])
        
        
    print('month', month)
    print('days' , days)
    print('total_login', total_login)
            
    
    return render(request, 'pie_chart.html', {
        'labels': labels,
        'data': data,
        'g' : g,
        'total' : total,
        'sex' : sex,
        'all_total' : all_total,
        'statuses' : statuses,
        'status_total' : status_total,
        'y_list' : y_list,
        'x_list' : x_list,
        'months' : months,
        'chart_data' : chart_data
       
    })
@only_admin
def post_grap(request,slug):
    posts=BlogPost.objects.filter(slug=slug)
    return render(request, 'grap_post.html',context={
        'posts': posts

    })

@only_admin
def delete(request,slug):
    post=BlogPost.objects.get(slug=slug)
    if request.method=='POST':
        post.delete()
        return redirect('admin_dashboard')
    return render(request,'deletepost.html',context={
        'post' : post
    })


##################### DATA END #######################

@login_required(login_url='usepage/')
def donate(request):
    if request.method=="POST":
        amount=int(request.POST['amount'])
        customer=stripe.Customer.create(
            email=request.POST['email'],
            name=request.POST['name'],
            source=request.POST['stripeToken']
        )
        charge=stripe.Charge.create(
            customer=customer,
            amount=amount*100,
            currency='usd',
            description='Donation'
        )
        return redirect(reverse('success',args=[amount]))
    return render(request, 'donate.html',context={})
    
@login_required(login_url='usepage/')
def successMsg(request,args):
    amount = args
    return render(request, 'success.html', {"amount" : amount})
    
############## POST UPDATE,CREATE, REMOVE #####################

@only_admin
def create(request):
    form=PostForm(request.POST or None , files=request.FILES or None)
    if form.is_valid():
        post=form.save(commit=False)
        post.user=request.user
        post.save()
        #messages.success(request,'Created Your Post Successful!')
        return redirect('homepage')
    else:
        form=PostForm()
    return render(request, 'create.html',context={
        'form' : form
    })
@only_admin
def update_post(request,slug):
    post=get_object_or_404(BlogPost,slug=slug)
    form=PostForm(request.POST or None , files=request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('admin_dashboard')
    return render(request, 'update_post.html',context={
        'form' : form
    })



####################### USER BLOG ####################
@login_required(login_url='usepage/')
def categories(request,slug,blogslug):
    categories=get_object_or_404(Category,slug=slug)
    post=BlogPost.category.get(categories=categories,slug=blogslug)
    return render(request, 'categories.html',context={
        'post' : post
    })


@login_required(login_url='userpage/')
def homepage(request):
    posts=BlogPost.objects.all()
    return render(request, 'home.html', context={
        'posts' : posts
    })
@login_required(login_url='userpage/')
def category(request,slug):
    category=get_object_or_404(Category,slug=slug)
    posts=category.category.all()
    return render(request, 'category.html', context={
        'posts' : posts
    })

def userpage(request):
    return render(request, 'userpage.html',context={})
    
@login_required(login_url='userpage/')
def user_post_detail(request,slug):
    post=get_object_or_404(BlogPost,slug=slug)
    post.views=post.views+1
    post.save()
    latest_posts=BlogPost.objects.all().order_by('-id')[0:3]
    comments=Comment.objects.filter(post=post)
            ################################################ BUG $$$$$$$$$$$$$$$$$$$
    if request.method == 'POST':
        try:
            reviews = Comment.objects.get(user__id=request.user.id, post=post)
            form = CommentForm(request.POST, instance=reviews)
            form.save()
            #messages.success(request, 'Thank you! Your review has been updated.')
            return redirect('homepage')
        except Comment.DoesNotExist:
            form = CommentForm(request.POST)
            if form.is_valid():
                data = Comment()
                data.comment = form.cleaned_data['comment']
                data.post = post
                data.user_id = request.user.id
                data.save()
                #messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect('homepage')
    return render(request, 'user_post_detail.html',context={
        'post' : post,
        'latest_posts' : latest_posts,
        'comments' : comments,

    })
@login_required(login_url='userpage/')
def like(request,slug):
    if request.method == "POST":
        like = Likes()
        like.post = get_object_or_404(BlogPost, slug=slug)
        like.user = request.user
        
        like.post.like = like.post.like + 1
        print('oldu')
        like.save()
    return HttpResponseRedirect(reverse('user_post_detail', args=[slug]))
    

def contact(request):
    form=ContactForm()
    if request.method=="POST":
        form=ContactForm(request.POST)
        if form.is_valid():
            print(form)
            model=Contact()
            model.email=form.cleaned_data['email']
            model.first_name=form.cleaned_data['first_name']
            model.last_name=form.cleaned_data['last_name']
            model.number=form.cleaned_data['number']
            model.message=form.cleaned_data['message']
            print(form)
            model.save()
            
            return redirect('userpage')
    return render(request, 'contact.html',context={
        'form' : form
    })
    



def deneme(request):
    return render(request,'tekrar1.html',context={})