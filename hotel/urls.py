from django.urls import path
from hotel import views

# urlpatterns = [
#     path("", views.home, name="home"),
#     path("register/", views.register, name="register"),
#     path("login/", views.login_view, name="login"),
#     path("logout/", views.logout_view, name="logout"),
#     path("admin/", views.admin_dashboard, name="admin_dashboard"),
#     path("add_hotel/", views.add_hotel, name="add_hotel"),
#     path("delete_hotel/<str:hotel_name>/", views.delete_hotel, name="delete_hotel"),
#     path("add_room/", views.add_room, name="add_room"),
#     path("delete_room/<str:hotel_name>/<str:room_type>/", views.delete_room, name="delete_room"),
#     path("dashboard/", views.user_dashboard, name="user_dashboard"),
#     path("book/<str:hotel_name>/<str:room_type>/", views.book_room, name="book_room"),
#     path("cancel/<str:hotel_name>/<str:room_type>/", views.cancel_booking, name="cancel_booking"),
# ]


urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),  # ✅ Updated
    path("add_hotel/", views.add_hotel, name="add_hotel"),
    path("delete_hotel/<str:hotel_name>/", views.delete_hotel, name="delete_hotel"),
    path("add_room/", views.add_room, name="add_room"),
    path("delete_room/<str:hotel_name>/<str:room_type>/", views.delete_room, name="delete_room"),
    path("dashboard/", views.user_dashboard, name="user_dashboard"),
    path("book/<str:hotel_name>/<str:room_type>/", views.book_room, name="book_room"),
    path("cancel/<str:hotel_name>/<str:room_type>/", views.cancel_booking, name="cancel_booking"),
]
