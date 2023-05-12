import json
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor.fields import RichTextFormField

from MyBlog.forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from common.decorators import ajax_required
from django.views.decorators.http import require_POST
from django.utils.module_loading import import_string
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from bootstrap_modal_forms.generic import BSModalCreateView
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from datetime import timedelta
from django.template import loader
from hitcount.views import HitCountDetailView
from verify_email.email_handler import send_verification_email


class AllKeywordsView(ListView):
    model = BlogPost
    template_name = "blog/blog.html"


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def add_category(request):
    try:
        categories = BlogPostCategories.objects.all()
        if request.method == "POST":
            form = CategoryForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                category = form.save(commit=False)
                type_id = request.POST.get('type')
                category.type_id = type_id
                category.save()
                obj = form.instance
                alert = True
                return render(request, "blog/add_categories.html", {'obj': obj, 'alert': alert})
        else:
            form = CategoryForm()
    except:
        pass
    return render(request, "blog/add_categories.html", {'form': form, 'categories': categories})

##################### Add New Post(new topic) and Update to the blog post ####################################-->

@login_required(login_url='/account/login')
def add_newtopic(request, cat_id):
    try:
        category = BlogPostCategories.objects.get(id=cat_id)
        #category = BlogPostCategories.objects.filter(slug=slug).first()
        object_list = BlogPost.objects.all()
        posts = BlogPost.objects.filter(category=cat_id).order_by('-dateTime')
        # if request.method=="GET":
        data = dict()
        if request.method == "POST":
            form = BlogPostForm(data=request.POST, files=request.FILES)
            formset = FileUploadForm(data=request.POST, files=request.FILES)
            if all([form.is_valid(), formset.is_valid()]):
                # if form.is_valid():
                blogpost = form.save(commit=False)
                blogpost.author = request.user
                blogpost.category = category  # BlogPostCategories.objects.get(id=cat_id)
                blogpost.save()
                files = Upload_Files(request, blogpost.id)
                add_image_newtopic(blogpost, files)
                obj = form.instance
                alert = True
                # When the submit button is pressed, the popup should disappear and refresh the main 
                return render(request, "blog/blog_category.html", {'posts': posts, 'category': category})
                #return render(request, "blog/blog_category.html", {'obj': obj, 'alert': alert})
                # return render(request, "blog/" + category.category_title + "/" + str(category.id), {'obj': obj, 'alert': alert})
        else:
            form = BlogPostForm()
            formset = FileUploadForm()
    except:
        pass
    return render(request, "blog/partial_add_newtopic.html", {'form': form, 'formset': formset, 'category': category})


def Upload_Files(request, post_id):
    try:
        form = FileUploadForm(data=request.POST, files=request.FILES)
        files = request.FILES.getlist('file')
        if request.method == 'POST':
            if form.is_valid():
                for f in files:
                    file_instance = FileUploads(file=f)
                    file_instance.post_id = post_id
                    file_instance.save()
        else:
            form = FileUploadForm()
    except:
        pass
    return files


def add_image_newtopic(blogpost, file):
    try:
        if (len(file) > 0):
            blogpost.image = file[0]  # file[] changed to 0 from 1
            blogpost.save()
            return HttpResponse('')
        else:
            return HttpResponse('')
    except:
        pass
    
    
def update_post(request, slug):
    try:
        post = BlogPost.objects.get(slug=slug)
        #request.FILES.getlist('file')
        
        # postfiles = FileUploads.objects.none()
        # if (FileUploads.objects.filter(post_id = post.id).exists() == True):
        #     postfiles = FileUploads.objects.get(post_id = post.id)
        #postfiles = []
        #postfiles.append(get_object_or_404(FileUploads, post_id = post.id))
            
        category = BlogPostCategories.objects.get(id=post.category_id)
        if request.method == "POST":
            form = BlogPostForm(data=request.POST, instance=post, files=request.FILES)
            formset = FileUploadForm(data=request.POST, files=request.FILES)
            if all([form.is_valid(), formset.is_valid()]):
                post = form.save()
                files = Upload_Files(request, post.id)
                return JsonResponse({'status': 'ok'})
                #return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"postChanged": None,  "showMessage": f"{post.title} updated." })})
                #return HttpResponse(status=204, headers={"postChanged": None, "showMessage": f"{post.title} updated."})
                #return render(request, "blog/partial_edit_blog_post.html", {'post': post, 'category': category})
        else:
            form = BlogPostForm(instance=post)
            #req = request.FILES['file']
            
            formset = FileUploadForm(FileUploads.objects.filter(post_id = post.id))
            # if (postfiles.exists() == False):
            #     formset = FileUploadForm()
            # else:
            #     formset = FileUploadForm(instance=postfiles)
            #formset = FileUploadForm()
    except:
        pass
    return render(request, "blog/partial_edit_blog_post.html", {'form': form, 'formset': formset, 'category': category})

###################### End Add New Post and Update to the blog post ####################################


###################### Update Topic to the blog post ####################################


class UpdatePostView(UpdateView):
    model = BlogPost
    template_name = 'blog/partial_edit_blog_post.html'
    fields = ['title', 'slug', 'content', 'image']
    widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'content': forms.CharField(widget=CKEditorWidget()),
        # 'content': RichTextFormField(config_name='default'), 
    }
    
###################### End Update Topic to the blog post ####################################


###################### List the blog post ####################################
# @ajax_required
def blogs_list(request):
    
    # Catch an anonymous user as he hits the site.
    if request.user.is_anonymous:
        request.session['cached_session_key'] = request.session.session_key
        
    active_users = User.objects.all().filter(last_login__gte=now()-timedelta(minutes=10)).count()
    #active_anonymous = User.objects.all().filter(last_login__gte=now()-timedelta(minutes=5)).count()
    
    types = TypeCategories.objects.all()
    categories = BlogPostCategories.objects.all().order_by('category_title')
    categories = BlogPostCategories.objects.filter().order_by('category_title')
    file_list = FileUploads.objects.all()
    object_list = BlogPost.objects.all()
    object_list = BlogPost.objects.filter().order_by('-dateTime', 'category')
    paginator = Paginator(object_list, 9)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, "blog/blog_list.html", {'posts': posts, 'types': types, 'categories': categories, 'files': file_list, 'active_users':active_users})

    # def blogs_list(request):
    #     types = TypeCategories.objects.all()
    #     categories = BlogPostCategories.objects.all().order_by('category_title')
    #     categories = BlogPostCategories.objects.filter().order_by('category_title')
    #     file_list = FileUploads.objects.all()
    #     object_list = BlogPost.objects.all()
    #     object_list = BlogPost.objects.filter().order_by('-dateTime', 'category')
    #     paginator = Paginator(object_list, 21)  # 3 posts in each page
    #     page = request.GET.get('page')
    #     try:
    #         posts = paginator.page(page)
    #     except PageNotAnInteger:
    #             # If page is not an integer deliver the first page
    #         posts = paginator.page(1)
    #     except EmptyPage:
    #         #if is_ajax(request=request):
    #         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    #             # If the request is AJAX and the page is out of range
    #             # return an empty page
    #             return HttpResponse('')
    #         # If page is out of range deliver last page of results
    #         posts = paginator.page(paginator.num_pages)
    #     #if is_ajax(request=request):
    #     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    #         return render(request, 'blog/blog_list_ajax.html', {'posts':posts, 'types': types, 'categories':categories, 'files':file_list})
    #     return render(request, "blog/blog_list.html", {'posts':posts, 'types': types, 'categories':categories, 'files':file_list})

    #return render(request, "blog/blog_category.html", {'posts': posts, 'category': category})

###################### End list the blog post ####################################


###################### List blog posts by category ####################################

def blogByCategory(request, slug, cat_id):
    # Catch an anonymous user as he hits the site.
    if request.user.is_anonymous:
        request.session['cached_session_key'] = request.session.session_key
        
    # categories = BlogPostCategories.objects.all()
    category = BlogPostCategories.objects.filter(slug=slug).first()
    object_list = BlogPost.objects.all()
    object_list = BlogPost.objects.filter(category=cat_id).order_by('-dateTime')
    paginator = Paginator(object_list, 9)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, "blog/blog_category.html", {'posts': posts, 'category': category})

###################### End list the blog post by category ####################################

   
###################### Add Comment to blog post ####################################

@login_required(login_url='/account/login')
def add_comment(request, slug):
    try:
        post = BlogPost.objects.filter(slug=slug).first()

        category = BlogPostCategories.objects.filter(id=post.category_id).first()
        comments = Comment.objects.filter(blog=post)
        files = FileUploads.objects.filter(post_id=post.id)
        queryset = BlogPost.objects.annotate(num_views=Count('viewers')).order_by('-num_views')
        datas = get_object_or_404(queryset, slug=slug)

        if request.method == "POST":
            form = CommentForm(request.POST)
            formset = CommentFileUploadForm(data=request.POST, files=request.FILES)
            if all([form.is_valid(), formset.is_valid()]):
                comment = form.save(commit=False)
                comment.user = request.user
                comment.blog = post
                comment.save()
                Comment_Upload_Files(request, comment.id)
                comments = Comment.objects.filter(blog=post)

                commentfiles = CommentFileUploads.objects.none()
                for comment in comments:
                    commentfiles = commentfiles | CommentFileUploads.objects.filter(comment_id=comment.id)

                commentfiles = CommentFileUploads.objects.filter(comment_id=comment.id)
                
                return HttpResponse(status=204, headers={"movieListChanged": None, "showMessage": f"{post.title} updated."})
                #return render(request, "blog/blog_details.html",
                #              {'post': post, 'comments': comments, 'commentfiles': commentfiles, 'datas': datas, 'files': files, 'category': category})
                # return render(request, 'blog/blog_detailes.html', { 'form': form, 'post':post})
        else:
            form = CommentForm()
            formset = CommentFileUploadForm()
    except:
        pass
    return render(request, 'blog/partial_add_comment.html', {'form': form, 'formset': formset, 'post': post, 'category': category})

def Comment_Upload_Files(request, comment_id):
    try:
        form = CommentFileUploadForm(data=request.POST, files=request.FILES)
        files = request.FILES.getlist('file')
        if request.method == 'POST':
            if form.is_valid():
                for f in files:
                    file_instance = CommentFileUploads(file=f)
                    file_instance.comment_id = comment_id
                    file_instance.save()
        else:
            form = CommentFileUploadForm()
    except:
        pass
    return files


@login_required(login_url='en/account/login')
def reply_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    
    post = BlogPost.objects.filter(id=comment.blog_id).first()
    category = BlogPostCategories.objects.filter(id=post.category_id).first()
    files = FileUploads.objects.filter(post_id=post.id)
    #queryset = BlogPost.objects.annotate(num_views=Count('viewers')).order_by('-num_views')
    #datas = get_object_or_404(queryset, pk=comment_id)
    form = Reply_CommentForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            reply_comment = form.save(commit=False)
            reply_comment.replier_name = request.user
            reply_comment.comment = comment
            reply_comment.save()
            
            replycomment = ReplyComment.objects.filter(comment_id=comment_id)
            messages.success(request, 'Comment replied!')
            
            return HttpResponse(status=204, headers={"movieListChanged": None, "showMessage": f"{post.title} updated."})
            #return render(request, "blog/blog_details.html", {'post': post, 'comments': comment, 'replycomment': replycomment, 'files': files, 'category': category})
            # return render(request, 'blog/blog_details.html', { 'form': form, 'post':post})
    else:
        form = Reply_CommentForm()
    return render(request, 'blog/partial_add_reply_comment.html', {'form': form, 'post': post, 'comments': comment, 'category': category})
 
###################### End add comment to blog post ####################################


def blog_details(request, slug): 
    post = BlogPost.objects.filter(slug=slug).first()
    # To know how many authenticated users and anonymous users that viewed the post.
    post_viewed(request=request, post_id=post.id) 
    try:
        category = BlogPostCategories.objects.filter(id=post.category_id).first()
        files = FileUploads.objects.filter(post_id=post.id)
        queryset = BlogPost.objects.annotate(num_views=Count('viewers')).order_by('-num_views')
        datas = get_object_or_404(queryset, slug=slug)
        comments = Comment.objects.filter(blog=post)
        
        replycomment = ReplyComment.objects.none()
        for comment in comments:
            replycomment = replycomment | ReplyComment.objects.filter(comment_id=comment.id)    # Queryset union using | operator in Django

        commentfiles = CommentFileUploads.objects.none()
        for comment in comments:
            commentfiles = commentfiles | CommentFileUploads.objects.filter(comment_id=comment.id)  # Queryset union using | operator in Django
    except:
        pass
    return render(request, "blog/blog_details.html", {'post': post, 'comments': comments, 'commentfiles': commentfiles, 'datas': datas, 'files': files, 'replycomment': replycomment, 'category': category})


def post_viewed(request, post_id):
    if post_id:
        try:
            post = BlogPost.objects.get(id=post_id)
         
            if request.user.is_authenticated:
                post.viewers.add(request.user)
            elif request.user.is_anonymous:
                request.session['cached_session_key'] = request.session.session_key
                #post.viewers.add()
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})

@login_required(login_url='en/account/login')
def reply_comments(request, comment_id):
    if request.method == "POST":
        user = request.user
        content = request.POST.get('content', '')
        blog_id = request.POST.get('blog_id', '')
        #comment = Comment(user = user, content = content, blog=post)
        #comment.save()
    #return  render(request, "blog/blog_details.html", {'post':post, 'comments':comments, 'datas':datas, 'files':files, 'category':category})


# def BlogPostLike(request, pk):
#     post = get_object_or_404(BlogPost, id=request.POST.get('blogpost_id'))
#     if post.likes.filter(id=request.user.id).exists():
#         post.likes.remove(request.user)
#     else:
#         post.likes.add(request.user)

#     return HttpResponseRedirect(reverse('blogpost-detail', args=[str(pk)]))


# def replyComment(request,id):
#    comments = Comment.objects.get(id=id)

#    if request.method == 'POST':
#        replier_name = request.user
#        reply_content = request.POST.get('reply_content')

#        newReply = ReplyComment(replier_name=replier_name, reply_content=reply_content)
#        newReply.reply_comment = comments
#        newReply.save()
#        messages.success(request, 'Comment replied!')
#        return redirect('blog/blog_details.html')


# def blogs_commentsbyCategory(request, slug, cat_id):
#     post = BlogPost.objects.filter(slug=slug, category=cat_id).first()
#     comments = Comment.objects.filter(blog=post)
#     if request.method == "POST":
#         user = request.user
#         content = request.POST.get('content', '')
#         blog_id = request.POST.get('blog_id', '')
#         comment = Comment(user=user, content=content, blog=post)
#         comment.save()
#     return render(request, "blog/blog_details.html", {'post': post, 'comments': comments})


def Delete_Blog_Post(request, slug):
    posts = BlogPost.objects.get(slug=slug)
    if request.method == "POST":
        posts.delete()
        return redirect('/')
    return render(request, 'blog/delete_blog_post.html', {'posts': posts})


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        blogs = BlogPost.objects.filter(title__contains=searched)
        return render(request, "blog/search.html", {'searched': searched, 'blogs': blogs})
    else:
        return render(request, "blog/search.html", {})


# def Register(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         email = request.POST['email']
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']

#         if password1 != password2:
#             messages.error(request, "Passwords do not match.")
#             return redirect('blog/register')

#         user = User.objects.create_user(username, email, password1)
#         user.first_name = first_name
#         user.last_name = last_name
#         user.save()
#         return render(request, 'blog/login.html')
#     return render(request, "blog/register.html")


# def Login(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']

#         user = authenticate(username=username, password=password)

#         if user is not None:
#             login(request, user)
#             messages.success(request, "Successfully Logged In")
#             return redirect("/")
#         else:
#             messages.error(request, "Invalid Credentials")
#         return render(request, 'blog/login.html')
#     return render(request, "blog/login.html")


def Logout(request):
    messages.success(request, "Successfully logged out")
    return redirect('/')


###################### Blog post Shared, Like ####################################

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(BlogPost, id=post_id)
    sent = False
    # global form
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            #post_url = post.get_absolute_url()
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}"
            sendermail = request.user.email
            receipientmail = [cd['recepient_email']]
            send_mail(subject, message, sendermail, receipientmail)
            sent = True
            return redirect('/en/blog/{{post.slug}}/{{post.id}}')
    else:
        form = EmailPostForm()
    return render(request, 'blog/partial_share.html', {'post': post, 'form': form, 'sent': sent})


@ajax_required
@login_required(login_url='en/account/login')
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = BlogPost.objects.get(id=post_id)
            if action == 'like':
                post.users_like.add(request.user)
            else:
                post.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})




###################### End blog post Shared, Like, Viewed ####################################


######################  Follow system ###############################

@login_required(login_url='en/account/login')
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'blog/user/list.html', {'section': 'people', 'users': users})


@login_required(login_url='en/account/login')
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'blog/user/detail.html', {'section': 'people', 'user': user})

#####################################################################


###################### Advertisement on blog post category ####################################
@login_required(login_url='/account/login')
def advertisement(request, category_id):
    category = get_object_or_404(BlogPostCategories, id=category_id)
    if request.method == "POST":
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/en/partial_advertisement/{{ category_id }}')
    else:
       form = AdvertisementForm()
    return render(request, 'blog/partial_advertisement.html', {'form': form, 'category': category})

def edit_advertisement(request, pk):
    category = get_object_or_404(BlogPostCategories, id=request.category.id)
    advert = get_object_or_404(Advertisement, pk=pk)
    if request.method == "POST":
        form = AdvertisementForm(request.POST, instance=advert)
        if form.is_valid():
            form.save()
            return redirect('/en/partial_advertisement/{{ category_id }}')
    else:
       form = AdvertisementForm(instance=advert)
    return render(request, 'blog/partial_advertisement.html', {'form': form, 'category': category})

###################### End Advertisement on blog post category ####################################

def site_statistics(request):
    return render(request, 'blog/partial_site_statistics.html')
    



# @login_required
# def user_list(request):
#     users = User.objects.filter(is_active=True)
#     return render(request, 'account/user/list.html', {'section': 'people', 'users': users})

# @login_required
# def user_detail(request, username):
#     user = get_object_or_404(User, username=username, is_active=True)
#     return render(request, 'account/user/detail.html', {'section': 'people', 'user': user})




# def blogs_comments(request, slug):
#     post = BlogPost.objects.filter(slug=slug).first()
#     category = BlogPostCategories.objects.filter(id=post.category_id).first()
#     files = FileUploads.objects.filter(post_id=post.id)

#     queryset = BlogPost.objects.annotate(num_views=Count('viewers')).order_by('-num_views')
#     datas = get_object_or_404(queryset, slug=slug)

#     comments = Comment.objects.filter(blog=post)
#     if request.method == "POST":
#         user = request.user
#         content = request.POST.get('content', '')
#         blog_id = request.POST.get('blog_id', '')
#         comment = Comment(user=user, content=content, blog=post)
#         comment.save()
#     return render(request, "blog/blog_details.html",
#                   {'post': post, 'comments': comments, 'datas': datas, 'files': files, 'category': category})