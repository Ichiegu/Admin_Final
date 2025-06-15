from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=(
        ('admin', 'Administrator'),
        ('staff', 'Staff Member'),
        ('guest', 'Guest'),
    ), default='guest')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Service(models.Model):
    PRICING_TYPE_CHOICES = (
        ('per_head', 'Per Head'),
        ('per_space', 'Per Space'),
        ('per_cottage', 'Per Cottage'),
        ('per_night', 'Per Night'),
        ('per_hour', 'Per Hour'),
        ('fixed', 'Fixed Price'),
    )

    STATUS_CHOICES = (
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
        ('coming_soon', 'Coming Soon'),
    )

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    pricing_type = models.CharField(max_length=20, choices=PRICING_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    max_capacity = models.PositiveIntegerField(blank=True, null=True)
    additional_info = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Service.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        db_table = "services"

    def __str__(self):
        return self.name


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ]

    booking_id = models.CharField(max_length=20, unique=True)
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    guest_name = models.CharField(max_length=100, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    number_of_guests = models.PositiveIntegerField(default=1)
    special_requests = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.booking_id} - {self.guest.username}"

    class Meta:
        ordering = ['-created_at']


class Transaction(models.Model):
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('gcash', 'GCash'),
        ('paymaya', 'PayMaya'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    TRANSACTION_TYPES = [
        ('payment', 'Payment'),
        ('refund', 'Refund'),
    ]

    transaction_id = models.CharField(max_length=50, unique=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, default='payment')
    reference_code = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.booking.booking_id} ({self.status})"

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            # Generate a unique transaction ID
            prefix = 'TXN'
            date_str = timezone.now().strftime('%Y%m%d')
            last_transaction = Transaction.objects.filter(
                transaction_id__startswith=f"{prefix}{date_str}"
            ).order_by('-transaction_id').first()

            if last_transaction:
                last_number = int(last_transaction.transaction_id[-4:])
                new_number = last_number + 1
            else:
                new_number = 1

            self.transaction_id = f"{prefix}{date_str}{new_number:04d}"

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-transaction_date']
        indexes = [
            models.Index(fields=['transaction_id']),
            models.Index(fields=['status']),
            models.Index(fields=['transaction_date']),
            models.Index(fields=['payment_method']),
        ]


class Review(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user.username} - {self.rating} stars"


class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_images')
    image = models.ImageField(upload_to='reviews/')
    caption = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = "review_images"

    def __str__(self):
        return f"Image for {self.review}"


class Comment(models.Model):
    STATUS_CHOICES = (
        ('approved', 'Approved'),
        ('pending', 'Pending'),
        ('spam', 'Spam'),
    )

    comment_id = models.CharField(max_length=20, unique=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "comment"


class StaffMember(models.Model):
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('receptionist', 'Receptionist'),
        ('housekeeper', 'Housekeeper'),
        ('chef', 'Chef'),
        ('maintenance', 'Maintenance'),
        ('superadmin', 'Superadmin'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    hire_date = models.DateField()
    is_active = models.BooleanField(default=True)
    bio = models.TextField(blank=True)

    class Meta:
        db_table = "staff_member"


class BlogPost(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    published_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        db_table = "blog_posts"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {'Read' if self.is_read else 'Unread'}"


class Staff(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('on_leave', 'On Leave'),
    ]

    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to='staff_images/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    date_joined = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.position}"

    class Meta:
        ordering = ['name']
        verbose_name = 'Staff Member'
        verbose_name_plural = 'Staff Members'