from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta


class Order(models.Model):
    number = models.CharField(max_length=100)
    date = models.DateTimeField()
    order_sum = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    card = models.ForeignKey('Card', on_delete=models.CASCADE, related_name='orders')

    def save(self, *args, **kwargs):
        # Call the parent save method to save the order
        super(Order, self).save(*args, **kwargs)

        # Update the last usage datetime of the card
        self.card.last_usage_date = timezone.now()
        self.card.save()


class Product(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)


class Card(models.Model):
    series = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    issue_date = models.DateTimeField(default=datetime.now)
    end_activity_date = models.DateTimeField(null=True, blank=True)
    last_usage_date = models.DateTimeField(null=True, blank=True)
    purchases_sum = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    STATUS_CHOICES = [
        ('not_activated', 'Not Activated'),
        ('activated', 'Activated'),
        ('expired', 'Expired'),
    ]
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='not_activated',
    )
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    card_orders = models.ManyToManyField('Order', blank=True, related_name='cards')

    def save(self, *args, **kwargs):
        if not self.end_activity_date:
            # Calculate expiration datetime by adding one year to the issue datetime
            expiration_timedelta = timedelta(days=365)
            self.end_activity_date = self.issue_date + expiration_timedelta

        super(Card, self).save(*args, **kwargs)



    def update_status(self):
        """
        Update the status of the card to "expired" if its validity period has passed.
        """
        if self.status != 'expired' and timezone.now() > self.end_activity_date:
            self.status = 'expired'
            self.save()


class CardTrash(models.Model):
    series = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    issue_date = models.DateTimeField(default=datetime.now)
    end_activity_date = models.DateTimeField(null=True, blank=True)
    last_usage_date = models.DateTimeField(null=True, blank=True)
    purchases_sum = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    STATUS_CHOICES = [
        ('not_activated', 'Not Activated'),
        ('activated', 'Activated'),
        ('expired', 'Expired'),
    ]
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='not_activated',
    )
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.series} {self.number}'

    class Meta:
        verbose_name_plural = 'Card Trash'
