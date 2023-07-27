from django import template

register = template.Library()

@register.filter(name='censor')
def censor(text):
    bad_words = ('Теперь', 'нового', 'вышло')
    for word in bad_words:
        if word in text:
            text = text.replace(word, '*****')
    return text