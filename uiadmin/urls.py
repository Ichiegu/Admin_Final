from django.urls import path
from .views import (
    login_view, register_view, logout_view, dashboard,
    booking_view, blogs_view, services_view, staff_view,
    update_booking, delete_booking, add_booking_view,
    update_transaction_status, transaction_list,
    edit_transaction, update_transaction, delete_transaction,
    transaction_receipt, export_transactions, delete_service,
    edit_service, add_staff, get_staff_details, edit_staff,
    delete_staff, get_service_details, reviews_dashboard,
    update_review_status, get_review_details, edit_review, delete_review,
    get_blog_details, add_blog_post, edit_blog_post, delete_blog_post,
    clear_booking_session, get_booking_stats, reports_view, booking_detail,
    profile_update_view, settings_view
)

urlpatterns = [
    # Authentication URLs
    path('', dashboard, name='home'),  # Changed to dashboard
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    # Profile and Settings URLs
    path('profile/update/', profile_update_view, name='profile_update'),
    path('settings/', settings_view, name='settings'),

    # Main URLs
    path('dashboard/', dashboard, name='dashboard'),
    path('booking/', booking_view, name='booking'),
    path('booking/<str:booking_id>/', booking_detail, name='booking_detail'),
    path('add-booking/', add_booking_view, name='add_booking'),
    path('booking/clear-session/', clear_booking_session, name='clear_booking_session'),
    path('booking/stats/', get_booking_stats, name='get_booking_stats'),
    path('blogs/', blogs_view, name='blogs'),
    path('reports/', reports_view, name='reports'),

    # Services URLs
    path('services/', services_view, name='services'),
    path('services/<int:service_id>/details/', get_service_details, name='get_service_details'),
    path('services/<int:service_id>/delete/', delete_service, name='delete_service'),
    path('services/<int:service_id>/edit/', edit_service, name='edit_service'),

    # Staff URLs
    path('staff/', staff_view, name='staff'),
    path('staff/dashboard/', staff_view, name='staff_dashboard'),
    path('staff/add/', add_staff, name='add_staff'),
    path('staff/<int:staff_id>/details/', get_staff_details, name='get_staff_details'),
    path('staff/<int:staff_id>/edit/', edit_staff, name='edit_staff'),
    path('staff/<int:staff_id>/delete/', delete_staff, name='delete_staff'),

    # Booking API Endpoints
    path('booking/<int:booking_id>/update/', update_booking, name='update_booking'),
    path('booking/<int:booking_id>/delete/', delete_booking, name='delete_booking'),

    # Transaction URLs
    path('transactions/', transaction_list, name='transaction_list'),
    path('transaction/<int:transaction_id>/update-status/', update_transaction_status,
         name='update_transaction_status'),
    path('transactions/<int:pk>/edit/', edit_transaction, name='edit_transaction'),
    path('transactions/<int:pk>/update/', update_transaction, name='update_transaction'),
    path('transactions/<int:pk>/delete/', delete_transaction, name='delete_transaction'),
    path('transactions/<int:pk>/receipt/', transaction_receipt, name='transaction_receipt'),
    path('transactions/export/', export_transactions, name='export_transactions'),

    # Review Management URLs
    path('reviews/', reviews_dashboard, name='reviews_dashboard'),
    path('reviews/<int:review_id>/update-status/', update_review_status, name='update_review_status'),
    path('reviews/<int:review_id>/details/', get_review_details, name='get_review_details'),
    path('reviews/<int:review_id>/edit/', edit_review, name='edit_review'),
    path('reviews/<int:review_id>/delete/', delete_review, name='delete_review'),

    # Blog management URLs
    path('blogs/<int:post_id>/details/', get_blog_details, name='get_blog_details'),
    path('blogs/add/', add_blog_post, name='add_blog_post'),
    path('blogs/<int:post_id>/edit/', edit_blog_post, name='edit_blog_post'),
    path('blogs/<int:post_id>/delete/', delete_blog_post, name='delete_blog_post'),
]