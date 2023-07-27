import os

from django.dispatch import receiver
from django.db.models.signals import m2m_changed


from .models import PostCategory, Category, Post
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string


@receiver(m2m_changed, sender=PostCategory)
def test_signal(sender, instance, action, model, pk_set, **kwargs):
    if action == 'post_add':
        post_was_add_this_category = Category.objects.get(pk=list(pk_set)[0])
        user_emails_names_subscribed = post_was_add_this_category.subscribers_set.exclude(user__email='') \
            .values_list('user__email', 'user__username')
        user_emails_names_subscribed = dict(user_emails_names_subscribed)

        # send e-mails
        # некогда было рефач
        # лучше передать его в scheduler в будущем
        connection = get_connection()
        connection.open()
        emails = []
        title = instance.title
        text = instance.text

        for recipient in user_emails_names_subscribed:
            context = {'username': user_emails_names_subscribed[recipient],
                       'title': title, 'text': text,
                       'category':post_was_add_this_category.new_category,
                       'link':f'http://127.0.0.1:8000/news/{instance.id}'}
            html_content = render_to_string('subscribers.html', context)
            email = EmailMultiAlternatives(
                subject=title,
                body=text,
                from_email=os.getenv('E_MAIL_FULL'),
                to=[recipient]
            )
            email.attach_alternative(html_content, "text/html")
            emails.append(email)
        connection.send_messages(emails)
        connection.close()