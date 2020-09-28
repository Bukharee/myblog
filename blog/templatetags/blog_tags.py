from django import template
import markdown
from django.utils.safestring import mark_safe
from ..models import Post
from django.db.models import Count


register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

@register.inclusion_tag('latest_posts.html')
def most_recent(count=3):
    latest_posts = Post.objects.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def most_commented(count=3):
    return Post.objects.annotate(
        total_comments = Count('comment')
    ).order_by('-total_comments')[:count]

@register.simple_tag
def num_of_comments():
    Post.objects.comment_set.count()