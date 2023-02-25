from .models import Card
from rest_framework import viewsets, permissions, generics
from .serializers import CardSerializer


class CardViewSet(viewsets.ModelViewSet):
    # Use the CardSerializer to serialize and deserialize Card objects
    serializer_class = CardSerializer
    # Retrieve all Card objects from the database
    queryset = Card.objects.all()

    # Allow anyone to access this viewset
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        # Call the update_status method on each card object
        queryset = super().get_queryset()
        for card in queryset:
            card.update_status()  # Update the status of the card object
        return queryset
