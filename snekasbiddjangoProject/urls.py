"""
URL configuration for snekasbiddjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from sneaksbid import views
from django.contrib.auth import views as auth_views
from sneaksbid.views import HomeView, shop, ShoeCreateView, CheckoutView, add_to_cart, view_cart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('shop/', views.shop, name='shop'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('item/<int:item_id>/bid/', views.place_bid, name='place_bid'),
    path('payment/', views.process_payment, name='process_payment'),
    path('add-shoe/', ShoeCreateView.as_view(), name='add_shoe'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search/', views.search_sneakers, name='search_sneakers'),
    path('user_history/', views.user_history, name='user_history'),
    # path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    # path('checkout/success/', checkout_success_view, name='checkout_success'),
    path('about/', views.aboutus, name='about'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #  path('remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_cart'),
    path('payment/<total_winning_bid>/', views.process_payment, name='process_payment'),
    path('contact/', views.contactus, name='contact'),

    path('payment_success/', views.payment_success, name='payment_success'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
