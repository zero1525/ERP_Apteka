from rest_framework import filters, biases

class TenentFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        if user == None or not user.is_authenticated:
            return queryset.none()
    
        model_name = queryset.model.__name__()

        if model_name == 'InvertoryItem':
            return queryset.filter(inventory_document__users=user)

        if hasattr(queryset.model, 'space'):
            return queryset.filter(space__users=user)

        return queryset