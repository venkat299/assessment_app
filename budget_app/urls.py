"""budget_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

# urlpatterns = [
#     path('assessment', include('assessment.urls')),
#     path('admin/', admin.site.urls),
# ]

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

from budget_app import views

urlpatterns = [
                  url(r'^$', views.login_view, name='login_new'),
                  url(r'^login/$', views.login_view, name='login'),
                  # url(r'^accounts/login/$', views.login_view),
                  url(r'^logout/$', auth_views.LogoutView.as_view(), {'next_page': '/'}, name='logout'),
                  url(r'^assessment/', include('assessment.urls')),
                  url(r'^admin/', admin.site.urls),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
