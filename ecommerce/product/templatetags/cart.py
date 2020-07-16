from django import template

register = template.Library()


@register.filter(name="is_in_cart")
def is_in_cart(product, cart):
    keys = cart.keys()

    for id in keys:
        if int(id) == product.id:
            return True
    return False


@register.filter(name="cart_count")
def cart_count(product, cart):
    keys = cart.keys()

    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    return False

@register.filter(name="item_price_total")
def item_price_total(product, cart):
    return product.price * cart_count(product, cart)
    
@register.filter(name="total_bill")
def total_bill(product, cart):
    sum = 0
    for p in product:
        sum = sum + item_price_total(p, cart)
    return sum

@register.filter(name="qty_count")
def qty_count(product, cart):
    qty = 0
    for p in product:
        qty = qty + cart_count(p, cart)
    return qty
