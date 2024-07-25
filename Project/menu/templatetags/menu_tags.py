from django import template
from menu.models import MenuItem

register = template.Library()

def get_menu_items(menu_name, current_url):
    menu_items = MenuItem.objects.filter(menu__name=menu_name).select_related('parent')

    menu_dict = {}
    for item in menu_items:
        menu_dict.setdefault(item.parent, []).append(item)

    def build_menu(items, parent=None):
        result = ''
        for item in items:
            if item.parent == parent:
                is_active = current_url in [item.url, item.get_absolute_url()]
                expanded = 'expanded' if is_active else ''
                result += f'<li class="{expanded}">'

                link = item.url or f"{item.named_url}"
                result += f'<a href="{link}">{item.title}</a>'

                children = build_menu(items, item)
                if children:
                    result += f'<ul>{children}</ul>'

                result += '</li>'
        return result

    return build_menu(menu_dict.get(None, []))

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    current_url = context['request'].path
    return get_menu_items(menu_name, current_url)