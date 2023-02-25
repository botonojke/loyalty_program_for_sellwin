from django.shortcuts import render
from django.views import View
from datetime import datetime, timedelta

from . import models
from .models import Card


class CardGeneratorView(View):
    def get(self, request):
        # Render the initial form template
        return render(request, 'card_generator.html')

    def post(self, request):
        # Get input data from the form
        series = request.POST.get('series')
        number_start = 1
        number = int(request.POST.get('number'))
        from_date = datetime.strptime(request.POST.get('issue_date'), '%Y-%m-%d').date()
        to_date = datetime.strptime(request.POST.get('end_activity_date'), '%Y-%m-%d').date()

        # Get the last card number from the database and add 1 to start the new card numbers from the next number
        last_card_number = int(Card.objects.all().order_by('-number').values()[0]['number']) + 1

        # Generate and save new card objects with the specified attributes
        for numbers in range(number_start, number + 1):
            card = Card(
                series=series,
                number=last_card_number,
                issue_date=from_date,
                end_activity_date=to_date,
                last_usage_date=None,
                purchases_sum=0,
                status='active',
                discount_percent=0
            )
            card.save()
            last_card_number += 1

        # Render the success template with a success message
        return render(request, 'success.html', {'success': True})
