

def is_customer(user):
    return user.groups.filter(name='customer').exists()

def is_staff_view(user):
    return user.groups.filter(name='staff_view').exists()

def is_staff(user):
    return user.groups.filter(name='staff').exists()

def is_admin(user):
    return user.groups.filter(name='Administrator').exists()