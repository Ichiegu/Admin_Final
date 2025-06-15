
# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import (
    Service, Booking, BlogPost,
    Review, ReviewImage, Transaction, Comment,
    StaffMember, Notification, UserProfile, Staff
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'phone')
    list_filter = ('user_type',)
    search_fields = ('user__username', 'user__email', 'phone')
    raw_id_fields = ('user',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'status', 'display_image')
    list_filter = ('status', 'pricing_type')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Image'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'guest', 'service', 'check_in', 'status', 'payment_method')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('booking_id', 'guest__username', 'service__name')
    date_hierarchy = 'created_at'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rating', 'status', 'created_at')
    list_filter = ('status', 'rating', 'created_at')
    search_fields = ('user__username', 'content')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    ordering = ('-created_at',)

@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ('review', 'caption', 'display_image')
    search_fields = ('review__booking__guest__username', 'caption')

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Image'

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'booking', 'amount', 'transaction_type', 'status', 'transaction_date')
    list_filter = ('status', 'transaction_type', 'payment_method')
    search_fields = ('transaction_id', 'booking__booking_id', 'reference_code')
    date_hierarchy = 'transaction_date'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_id', 'author', 'review', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('comment_id', 'author__username', 'review__review_id')

@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'hire_date', 'is_active')
    list_filter = ('role', 'is_active', 'hire_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')