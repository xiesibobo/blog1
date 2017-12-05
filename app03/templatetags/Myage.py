from django import template


from django.utils.safestring import mark_safe

register=template.Library()



@register.filter
def yuanling(t):
    import datetime




    create_time=datetime.datetime(year=t.year,month=t.month,day=t.day)
    ret=datetime.datetime.now()-create_time
    print(str(ret)[:-17])

    return str(ret)[:-17]
