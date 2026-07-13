from django.urls import path

from .views import OfferDetailSingleView, OfferDetailView, OfferListCreateView

urlpatterns = [
    path('offers/', OfferListCreateView.as_view(), name='offer-list'),
    path('offers/<int:pk>/', OfferDetailView.as_view(), name='offer-detail'),
    path(
        'offerdetails/<int:pk>/',
        OfferDetailSingleView.as_view(),
        name='offerdetail-detail',
    ),
]
