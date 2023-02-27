from django.contrib import admin
from .models import Card, Order, Product, CardTrash


# Define the Card model admin
class CardAdmin(admin.ModelAdmin):
    # Define which fields will be displayed in the list view
    list_display = ('id', 'series', 'number', 'issue_date', 'status')
    # Define which fields will be clickable in the list view
    list_display_links = ('id', 'series', 'number')
    # Define which fields can be searched in the list view
    search_fields = ('series', 'number', 'issue_date', 'end_activity_date', 'status')
    # Define which fields can be edited in the list view
    list_editable = ('status',)
    # Define the available filters in the list view
    list_filter = ('issue_date', 'end_activity_date', 'last_usage_date', 'status')

    # Define a custom action to move selected cards to trash
    def move_to_trash(self, request, queryset):
        for card in queryset:
            # Create a new CardTrash object based on the selected Card object
            card_trash = CardTrash.objects.create(
                series=card.series,
                number=card.number,
                issue_date=card.issue_date,
                end_activity_date=card.end_activity_date,
                last_usage_date=card.last_usage_date,
                purchases_sum=card.purchases_sum,
                status=card.status,
                discount_percent=card.discount_percent
            )
            card_trash.save()
            # Delete the original Card object
            card.delete()

    # Define a short description for the custom action
    move_to_trash.short_description = 'Move selected cards to trash'

    # Add the custom action to the available actions in the list view
    actions = ['move_to_trash']


# Define the CardTrash model admin
class CardTrashAdmin(admin.ModelAdmin):
    # Define which fields will be displayed in the list view
    list_display = ('id', 'series', 'number', 'issue_date')
    # Define which fields will be clickable in the list view
    list_display_links = ('id', 'series', 'number')
    # Define which fields can be searched in the list view
    search_fields = ('series', 'number', 'issue_date', 'end_activity_date')
    # Define the available filters in the list view
    list_filter = ('issue_date', 'end_activity_date')

    # Define a custom action to recover selected cards from trash
    def recover(self, request, queryset):
        for card_trash in queryset:
            # Create a new Card object based on the selected CardTrash object
            card = Card.objects.create(
                series=card_trash.series,
                number=card_trash.number,
                issue_date=card_trash.issue_date,
                end_activity_date=card_trash.end_activity_date,
                last_usage_date=card_trash.last_usage_date,
                purchases_sum=card_trash.purchases_sum,
                status=card_trash.status,
                discount_percent=card_trash.discount_percent
            )
            card.save()
            # Delete the original CardTrash object
            card_trash.delete()

    # Define a short description for the custom action
    recover.short_description = 'Recover selected cards from trash'

    # Add the custom action to the available actions in the list view
    actions = ['recover']


class OrderAdmin(admin.ModelAdmin):
    # Define which fields will be displayed in the list view
    list_display = ('id', 'date', 'order_sum')
    # Define which fields will be clickable in the list view
    list_display_links = ('id',)
    # Define which fields can be searched in the list view
    search_fields = ('number', 'date')
    # Define the available filters in the list view
    list_filter = ('date',)


class ProductAdmin(admin.ModelAdmin):
    # Define which fields will be displayed in the list view
    list_display = ('id', 'name', 'price')
    # Define which fields will be clickable in the list view
    list_display_links = ('id', 'name')
    # Define which fields can be searched in the list view
    search_fields = ('name',)


# Register the models and their respective admins
admin.site.register(Card, CardAdmin)
admin.site.register(CardTrash, CardTrashAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
