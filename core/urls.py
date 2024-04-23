from django.urls import path

from .views import *
urlpatterns = [
    path('', index, name='home'),

    path('ulgama-giris/', admin_login, name='login'),
    path('ulgamdan_cykys/', admin_logout, name='logout'),
    path('hasabat/', hasabat, name='hasabat'),

    path('isgar-gosmak/', register, name='register'),
    path('isgarlerin-gory/', StaffMembers.as_view(), name='staff_members'),
    path('isgar/<slug:slug>/', PersonView.as_view(), name='staff'),
    path('isgar/<slug:slug>/ayyrmak/', PersonDeleteView.as_view(), name='delete'),
    path('isgar/uytgetmek/<slug:slug>/', PersonUpdateView.as_view(), name='update'),

    path('giris-statistikasy/', get_in_work, name='input_statistics'),

]


handler404 = 'core.views.error_404'
handler500 = 'core.views.error_500'
handler403 = 'core.views.error_403'
handler400 = 'core.views.error_400'