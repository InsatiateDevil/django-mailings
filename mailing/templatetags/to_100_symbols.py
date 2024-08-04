from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(needs_autoescape=True)
def to_100_symbols(text, autoescape=True):
    if len(text) > 100:
        splited_text = text.split(' ')
        count_len = 0
        count_word = 0
        for word in splited_text:
            if (count_len + len(word)) <= 100:
                count_len += len(word)
                count_word += 1
            else:
                break
        return mark_safe(f"{' '.join(splited_text[:count_word])}...")
    return mark_safe(text)
