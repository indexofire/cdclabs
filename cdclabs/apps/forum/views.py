# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
#from onlineuser.models import getOnlineInfos
from forum.forms import EditPostForm, NewPostForm
from forum.models import Topic, ForumCategory, Forum, Post


def index(request, template_name="forum/forum_index.html"):
    categories = ForumCategory.objects.select_related(depth=1).all()
    latest_topics = Topic.objects.select_related(depth=1).all()[:10]
    #total_topics = Topic.objects.count()
    #total_posts = Post.objects.count()
    #total_users =  User.objects.count()
    #last_registered_user = User.objects.order_by('-date_joined')[0]
    extend_context = {
        'categories': categories,
        'topics': latest_topics,
        #'total_topics': total_topics,
        #'total_posts': total_posts,
        #'total_users': total_users,
        #'last_registered_user': last_registered_user,
    }
    #extend_context.update(getOnlineInfos(True))
    return render_to_response(template_name, extend_context, RequestContext(request))

def forum(request, forum_slug, template_name="forum/forum_forum.html"):
    forum = get_object_or_404(Forum, slug = forum_slug)
    topics = forum.topic_set.order_by('-sticky', '-last_reply_on').select_related()
    extend_context = {
        'forum': forum,
        'topics': topics,
    }
    return render_to_response(template_name, extend_context, RequestContext(request))

def topic(request, topic_id, template_name="forum/forum_topic.html"):
    topic = get_object_or_404(Topic, id=topic_id)
    topic.num_views += 1
    topic.save()
    objects = list(topic.post_set.order_by('created_on').select_related())
    #qs = Topic.objects.filter(pk=topic_id)
    #obj_dict = dict([(obj.id, obj) for obj in qs])
    #objects = Post.objects.filter(topic__in=qs).select_related()
    #relation_dict = {}
    #for obj in objects:
    #    relation_dict.setdefault(obj.topic_id,[]).append(obj)
    #for id, related in relation_dict.items():
    #    obj_dict[id]._related = related
    extend_context = {
        'topic': topic,
        'posts': objects,
        'replies': objects[1:],
        'thread': objects[0],
    }
    return render_to_response(template_name, extend_context, RequestContext(request))

def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return HttpResponseRedirect(post.get_absolute_url_ext())

def markitup_preview(request, template_name="forum/markitup_preview.html"):
    return render_to_response(template_name, {'message': request.POST['data']}, RequestContext(request))

@login_required
def new_post(request, forum_id=None, topic_id=None, form_class=NewPostForm, template_name='forum/forum_post.html'):
    qpost = topic = forum = first_post = preview = None
    show_subject_fld = True
    post_type = _(u'topic')
    if forum_id:
        forum = get_object_or_404(Forum, pk=forum_id)
    if topic_id:
        post_type = _(u'reply')
        topic = get_object_or_404(Topic, pk=topic_id)
        forum = topic.forum
        first_post = topic.post_set.order_by('created_on').select_related()[0]
        show_subject_fld = False
    if request.method == "POST":
        form = form_class(request.POST, user=request.user, forum=forum, topic=topic, \
                ip=request.META['REMOTE_ADDR'])
        preview = request.POST.get('preview', '')
        if form.is_valid() and request.POST.get('submit', ''):
            post = form.save()
            if topic:
                return HttpResponseRedirect(post.get_absolute_url_ext())
            else:
                return HttpResponseRedirect(reverse("forum_forum", args=[forum.slug]))
    else:
        initial={}
        qid = request.GET.get('qid', '')
        if qid:
            qpost = get_object_or_404(Post, id=qid)
            initial['message'] = "[quote=%s]%s[/quote]" % (qpost.posted_by.username, qpost.message)
        form = form_class(initial=initial)
    extend_context = {
        'forum':forum,
        'form':form,
        'topic':topic,
        'first_post':first_post,
        'post_type':post_type,
        'preview':preview,
        'show_subject_fld': show_subject_fld,
    }
    extend_context['unpublished_attachments'] = request.user.attachment_set.all().filter(activated=False)
    extend_context['is_new_post'] = True
    return render_to_response(template_name, extend_context, RequestContext(request))

@login_required
def edit_post(request, post_id, form_class=EditPostForm, template_name="forum/forum_post.html"):
    preview = None
    post_type = _('topic')
    edit_post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = form_class(instance=edit_post, user=request.user, data=request.POST)
        preview = request.POST.get('preview', '')
        if form.is_valid() and request.POST.get('submit', ''):
            edit_post = form.save()
            return HttpResponseRedirect('../')
    else:
        form = form_class(instance=edit_post)
    extend_context = {
        'form':form,
        'post': edit_post,
        'topic':edit_post.topic,
        'forum':edit_post.topic.forum,
        'post_type':post_type,
        'preview':preview,
    }
    extend_context['unpublished_attachments'] = request.user.attachment_set.all().filter(activated=False)
    extend_context['show_subject_fld'] = edit_post.topic_post
    return render_to_response(template_name, extend_context, RequestContext(request))

@login_required
def user_topics(request, user_id, template_name='forum/user_topics.html'):
    view_user = User.objects.get(pk=user_id)
    topics = view_user.topic_set.order_by('-created_on').select_related()
    extend_context = {
        'topics': topics,
        'view_user': view_user,
    }
    return render_to_response(template_name, extend_context, RequestContext(request))

@login_required
def user_posts(request, user_id, template_name='forum/user_posts.html'):
    view_user = User.objects.get(pk=user_id)
    posts = view_user.post_set.order_by('-created_on').select_related()
    extend_context = {
        'posts': posts,
        'view_user': view_user,
    }
    return render_to_response(template_name, extend_context, RequestContext(request))
