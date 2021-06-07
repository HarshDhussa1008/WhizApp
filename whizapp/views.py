from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.template.loader import render_to_string
import traceback

from .forms import QuestionForm
from .models import Question,QuestionImages,CommentImages,Comment,CommentReply
from django.core.mail import send_mail
from django.core.signing import Signer
from django.views.decorators.cache import cache_control

# Create your views here.
signer=Signer()


def mailer(user):
    subject = 'Reset Password for WhizApp'
    message = f'Hi {user.first_name} Please click the below link to reset your password.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    link={'user': user.email}
    html_message = render_to_string('whizapp/confirm_template.html', {'link': signer.sign_object(link)})
    send_mail(subject, message, 'WhizApp '+email_from, recipient_list, html_message=html_message)
    
def cnf_mailer(user):
    subject = 'WhizApp Account Verification'
    message = f'Hi {user.first_name} Please click the below link to verify your email.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    link={'user': user.email}
    html_message = render_to_string('whizapp/verify_template.html', {'link': signer.sign_object(link)})
    send_mail(subject, message, 'WhizApp '+email_from, recipient_list, html_message=html_message)
    
def ans_mailer(user,qid):
    subject = 'WhizApp Answer Notification'
    message = f'Hey {user.first_name} Your question just got answered'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    link={'link': 'https://whizapp.herokuapp.com/home/'+qid}
    html_message = render_to_string('whizapp/answer_template.html', link)
    send_mail(subject, message, 'WhizApp '+email_from, recipient_list, html_message=html_message)


def index(request):
    context={}
    posts = Question.objects.filter().order_by('timestamp')
    context['posts'] = posts
    return render(request, 'whizapp/index.html',context)


def login(request):
    if request.method == 'POST':
        # print(request.POST['email'],request.POST['password'])
        user=User.objects.get(email=request.POST['email'])
        if not user.is_active:
                return render(request, 'whizapp/login.html', {'error': 'Please verify your account to continue!'})
        user = auth.authenticate(request, username=request.POST['email'], password=request.POST['password'])
        if user is not None:
            print('user exists')
            auth.login(request, user)
            try:
                remember = request.POST['remember_me']
                if remember:
                    settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
            except:
                    settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
            return redirect('home')
        else:
            print('incorrect credentials')
            return render(request, 'whizapp/login.html', {'error': 'Username or password is incorrect!'})
    print('no post')
    return render(request, 'whizapp/login.html')


def signup(request):
    if request.method == 'POST':
        try:
            # print(request.POST)
            User.objects.get(username=request.POST.get('email'))
            return render(request, 'whizapp/signup.html', {'error': 'An account with this email already exists!'})
        except User.DoesNotExist:
            print('no user')
            user = User.objects.create_user(first_name=request.POST['firstname'], last_name=request.POST['lastname'], password=request.POST['password'], username=request.POST['email'],email=request.POST['email'],is_active=False)
            print(user)
            cnf_mailer(user)
            #auth.login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('login')
    return render(request, 'whizapp/signup.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def home(request):
    # mailer(request.user)
    print(request.user.email)
    context={}
    form=QuestionForm()
    # print(request.user.is_staff)
    if request.user.is_staff:
        return redirect('/admin/')
    if request.method == "POST":
        print('post data')
        print(request.POST.dict())
        user = request.user
        desc=request.POST.get('description')
        title=request.POST.get('title')
        images = request.FILES.getlist('images')
        dept= request.POST.get('sel1')
        if title and dept:
            print('data valid')
            print(images)
            ques_obj=Question.objects.create(user=user,description=desc,title=title,department=dept)
            for image in images:
                photo = QuestionImages.objects.create(image=image,post=ques_obj)
                photo.save()
            print(ques_obj)
            return redirect('home')
    context['form']=form
    posts=Question.objects.filter().order_by('timestamp')
    context['posts']=posts
    return render(request, 'whizapp/home.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
# @login_required(login_url='/login/')
def post_detail(request,qid):
    context={}
    post=Question.objects.get(qid=qid)
    context['post'] = post
    img=QuestionImages.objects.filter(post=post)
    context['images']=img
    cmnts=Comment.objects.filter(qid=post).order_by('timestamp')
    context['count']=cmnts.count()
    context['comments'] = cmnts
    context['reply']={}
    for i in cmnts:
        context['reply'][i.cid]=CommentReply.objects.filter(comment=i).order_by('timestamp')
    if request.method == 'POST':
        user = request.user
        comm = request.POST.get('comment')
        images = request.FILES.getlist('images')
        if comm:
            print('data valid')
            print(images)
            comm_obj=Comment.objects.create(qid=post,user=user,description=comm)
            post.status='Answered'
            post.save()
            for image in images:
                photo = CommentImages.objects.create(image=image, post=comm_obj)
                photo.save()
            user=User.objects.get(email=post.user.email)
            ans_mailer(user,qid)
            return redirect('post_detail', qid)

    return render(request,'whizapp/post_details.html',context)


def reply(request,qid,cid):
    if request.method == 'POST':
        post=Question.objects.get(qid=qid)
        user=request.user
        cmnt=Comment.objects.get(cid=cid)
        text=request.POST.get('reply')
        CommentReply.objects.create(comment=cmnt,text=text,user=user)
        return  redirect('post_detail',qid)
    return redirect('index')


def forget(request):
    message={}
    if request.method == 'POST':
        email=request.POST.get('email')
        print(email)
        try:
            user=User.objects.get(email=email)
            print(user)
            mailer(user)
            message['response'] = 'Reset mail successfully sent to your registered email.'
        except Exception as e:
            traceback.print_exc()
            message['response'] = 'Email not found.'
        finally:
            return render(request, 'whizapp/forget.html', message)

    return render(request, 'whizapp/forget.html', message)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reset(request,hash):
    context={}
    print(request.user)
    if request.method=='POST':
        npswd=request.POST.get('new_password')
        cpswd = request.POST.get('cnf_password')
        if npswd==cpswd:
            user=User.objects.get(email=hash)
            user.set_password(npswd)
            user.save()
            return redirect('login')
        else:
            message='Password mismatch'
            return render(request, 'whizapp/forget.html', message)
    if not request.user.is_anonymous:
        context['user']=request.user.email
        return render(request,'whizapp/reset.html',context)
    user=signer.unsign_object(hash)
    context['user']=user['user']
    return render(request,'whizapp/reset.html',context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    if request.method=='POST':
        auth.logout(request)
        print('loggd out')
        return redirect('index')
    return render(request, 'whizapp/index.html')


def confirm(request,hash=None):
    if hash:
        mailid=signer.unsign_object(hash)
        print(mailid)
        user=User.objects.get(email=mailid['user'])
        user.is_active=True
        user.save()
        return redirect('login')
    return render(request,'whizapp/login.html')
    
