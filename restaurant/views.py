# File: restaurant/views.py
# Author: Jack Lee (jacklee@bu.edu)
# Date: September 2024
# Description: Views for the restaurant application handling main page, order form, and confirmation

from django.shortcuts import render
import random
import time

# main page view
def main(request):
    """
    Renders the main page of the restaurant with welcome information.
    """
    return render(request, 'restaurant/main.html')

# order page view
def order(request):
    """
    Displays the order form with menu items and a randomly selected daily special.
    """
    # daily specials - pick one at random
    daily_specials = [
        'Lychee Green Tea with Crystal Boba',
        'Brown Sugar Milk Tea with Tapioca Pearls',
        'Passion Fruit Green Tea with Popping Boba',
        'Taro Milk Tea with Pudding',
        'Matcha Latte with Red Bean'
    ]

    daily_special = random.choice(daily_specials)

    context = {
        'daily_special': daily_special,
    }

    return render(request, 'restaurant/order.html', context)

# confirmation page view
def confirmation(request):
    """
    Processes order form data and displays confirmation with order details and pickup time.
    """
    if request.method == 'POST':
        # get form data
        customer_name = request.POST.get('name', '')
        customer_phone = request.POST.get('phone', '')
        customer_email = request.POST.get('email', '')
        special_instructions = request.POST.get('instructions', '')

        # get ordered items and calculate total
        ordered_items = []
        total_price = 0.0

        # regular menu items
        if request.POST.get('classic_milk_tea'):
            ordered_items.append('Classic Milk Tea - $5.50')
            total_price += 5.50

        if request.POST.get('thai_tea'):
            ordered_items.append('Thai Tea - $6.00')
            total_price += 6.00

        if request.POST.get('mango_green_tea'):
            ordered_items.append('Mango Green Tea - $5.75')
            total_price += 5.75

        if request.POST.get('strawberry_smoothie'):
            ordered_items.append('Strawberry Smoothie - $6.25')
            total_price += 6.25

        if request.POST.get('honeydew_milk_tea'):
            ordered_items.append('Honeydew Milk Tea - $5.75')
            total_price += 5.75

        if request.POST.get('oolong_tea'):
            ordered_items.append('Premium Oolong Tea - $4.50')
            total_price += 4.50

        # daily special
        if request.POST.get('daily_special'):
            daily_special_name = request.POST.get('daily_special_name', 'Daily Special')
            ordered_items.append(f'{daily_special_name} - $6.50')
            total_price += 6.50

        # calculate pickup time (30-60 minutes from now)
        pickup_minutes = random.randint(30, 60)
        pickup_time = time.time() + (pickup_minutes * 60)
        pickup_time_formatted = time.strftime('%I:%M %p', time.localtime(pickup_time))

        context = {
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'customer_email': customer_email,
            'special_instructions': special_instructions,
            'ordered_items': ordered_items,
            'total_price': f'{total_price:.2f}',
            'pickup_time': pickup_time_formatted,
        }

        return render(request, 'restaurant/confirmation.html', context)

    # if not POST, redirect to order page
    return render(request, 'restaurant/order.html')
