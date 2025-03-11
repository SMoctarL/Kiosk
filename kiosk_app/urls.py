from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-wave-account/', views.create_wave_account, name='create_wave_account'),
    path('create-om-account/', views.create_om_account, name='create_om_account'),
    path('customers/', views.customers_list, name='customers_list'),
    path('accounts/', views.accounts_list, name='accounts_list'),
    path('transactions/', views.transactions_list, name='transactions_list'),
    path('deposit/<str:customer_id>/', views.make_deposit, name='make_deposit'),
    path('withdraw/<str:customer_id>/', views.make_withdraw, name='make_withdraw'),
    path('transfer/<str:customer_id>/', views.make_transfer, name='make_transfer'),
    path('payment/<str:customer_id>/', views.make_payment, name='make_payment'),
    path('balance/<str:customer_id>/', views.show_balance, name='show_balance'),
] 