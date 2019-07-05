from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import app.views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app.views.home, name='home'),
    path('new', app.views.new, name="new"),
    path('<int:trip_id>', app.views.detail, name="detail"),
    path('promotion', app.views.promotion, name="promotion"),
    path('app/edit/<int:trip_id>', app.views.edit, name="edit"),
    path('app/delete/<int:trip_id>', app.views.delete, name="delete"),
    path('signup/', app.views.signup, name="signup"),
    path('login/', app.views.login, name="login"),
    path('logout/', app.views.logout, name="logout"),
    path('<int:trip_id>/comment/create', app.views.comment_create, name="comment_create"),
    path('<int:trip_id>/comment/<int:comment_id>/delete', app.views.comment_delete, name="comment_delete"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
