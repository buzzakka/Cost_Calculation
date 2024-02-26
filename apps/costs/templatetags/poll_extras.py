from django import template

register = template.Library()


@register.filter
def ru_month(value: int) -> str:
    """Возвращает русское название месяцв
    Args:
        value (int): цифровое значение месяца
    Returns:
        Русскоязычное название месяца (str)
    """
    months: list[str] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
                         'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    return months[value - 1]
