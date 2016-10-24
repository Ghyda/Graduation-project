from django.conf.urls import url

app_name = 'accounts'

urlpatterns = [
    url(r'^register$', 'accounts.views.register', name='register'),
    url(r'^login$', 'accounts.views.login', name='login'),
    url(r'^logout$', 'accounts.views.logout', name='logout'),
]
