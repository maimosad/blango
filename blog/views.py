from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.urls import reverse

from blog.models import Post
from blog.forms import CommentForm
import logging

logger = logging.getLogger(__name__)
# Create your views here.
def index(request):
    posts = Post.objects.filter(published_at__lte=timezone.now())
    return render(request, "blog/index.html", {"posts": posts})
def post_detail(request, slug):
    # Returns the Post Content field
    post = get_object_or_404(Post, slug=slug)
    
    # Create a Comment using the posted form data\
    # Return the comment / post view

    if request.user.is_active:
        # Check for active user. Inactive user means comment_form=None
        if request.method == "POST":
            # If not POST, a blank CommentForm is created.
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                # If POST, create the CommentForm using the posted data. If valid, form will be saved.
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                # log a message when a comment is created (logs directly after saving comment)
                logger.info("Created comment on Post %d for user %s", post.pk, request.user)
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None

    return render(request, "blog/post-detail.html", {"post": post, "comment_form": comment_form})
