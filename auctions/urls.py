from django.conf.urls import url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("view_listing/<int:listing_id>", views.view_listing, name="view_listing"),
    path(
        "watch_list/<str:user_name>/<int:listing_id>",
        views.watch_listing,
        name="watch_list",
    ),
    path(
        "remove_item_from_watch_list/<int:listing_id>",
        views.remove_item_from_watchlist,
        name="remove_item_from_watchlist",
    ),
    path("close_listing/<int:listing_id>", views.close_listing, name="close_listing"),
    path("comments/<int:listing_id>", views.comments, name="comments"),
    path(
        "category_view/<int:listing_id>/<str:cgt_name>/",
        views.category_view,
        name="category_view",
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
