from others.models import Messages
from orders.models import Order

def get_unreaded_messages(context):
    messages = Messages.objects.filter(readed=False)
    count_unreaded_messages = messages.count()
    unreaded_messages = messages.order_by('readed','-created')[:3]
    return {'unreaded_messages': unreaded_messages, 'count_unreaded_messages': count_unreaded_messages}

def get_unpaid_orders(context):
     orders = Order.objects.filter(paid=False)
     count_unpaid_orders = orders.count()
     unpaid_orders = orders.order_by('created')[:3]
     return {'unpaid_orders': unpaid_orders, 'count_unpaid_orders': count_unpaid_orders}
