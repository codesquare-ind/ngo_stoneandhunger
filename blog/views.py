from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import BlogPost, Comment
from .forms import CommentForm, BlogPostForm
from account.decorators import allowed_roles


def blog(request):
    recent_posts = BlogPost.objects.all().order_by('-posted_on')[:10]
    context = {'recent_posts': recent_posts}
    return render(request, 'blog/index.html', context)


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def create_blog(request):
    form = BlogPostForm()
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            b = form.save(commit=False)
            b.posted_by = request.user
            b.save()
            return redirect('a_blog')
    context = {'form': form}
    return render(request, 'blog/create_blog.html', context)


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def edit_blog(request, uuid):
    blog_post = BlogPost.objects.get(uuid=uuid)
    form = BlogPostForm(instance=blog_post)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog_post)
        if form.is_valid():
            form.save()
            return redirect('a_blog')
    context = {'form': form, 'edit': True}
    return render(request, 'blog/create_blog.html', context)


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def delete_blog(request, uuid):
    b_post = BlogPost.objects.get(uuid=uuid)
    b_post.delete()
    return redirect('a_blog')


def details(request, uuid):
    blog_post = BlogPost.objects.get(uuid=uuid)
    others = BlogPost.objects.exclude(uuid=uuid).order_by('-posted_on')[:5]
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = blog_post
            comment.posted_by = request.user
            comment.save()
    context = {'blog': blog_post, 'form': form, 'others': others}
    return render(request, 'blog/details.html', context)


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'user', 'subadmin'])
def edit_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
    return redirect('blog_post', comment.post.uuid)


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'user', 'subadmin'])
def delete_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    comment.delete()
    return redirect('blog_post', comment.post.uuid)