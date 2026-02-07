from django.db import models
from django.conf import settings
import json

# Check if using SQLite (demo mode) or PostgreSQL (production)
USE_SQLITE = getattr(settings, 'USE_SQLITE', True)


class Company(models.Model):
    """Company profiles"""
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True, verbose_name="Latitude")
    lng = models.FloatField(null=True, blank=True, verbose_name="Longitude")
    city = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    logo_url = models.URLField(max_length=500, null=True, blank=True, verbose_name="Logo URL")
    industry = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True, help_text="e.g., 1-10, 11-50, 51-200, 201-500, 500+")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Manager(models.Model):
    """Manager profiles"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='managers')
    display_name = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True, help_text="e.g., Engineering Manager")
    team = models.CharField(max_length=255, null=True, blank=True, help_text="e.g., Platform, Mobile")
    location = models.CharField(max_length=255, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        name = self.display_name or 'Manager'
        return f"{name} at {self.company.name}"


class JobPosting(models.Model):
    """Job postings at companies"""
    SOURCE_CHOICES = [
        ('manual', 'Manual'),
        ('greenhouse', 'Greenhouse'),
        ('lever', 'Lever'),
        ('other', 'Other'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    team = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    is_remote = models.BooleanField(default=False)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, default='manual')
    url = models.URLField(max_length=500, null=True, blank=True)
    salary = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} at {self.company.name}"


class Review(models.Model):
    """Anonymous reviews/feedback (simplified for demo)"""
    DURATION_CHOICES = [
        ('<3m', 'Less than 3 months'),
        ('3-12m', '3-12 months'),
        ('1-3y', '1-3 years'),
        ('3y+', 'More than 3 years'),
    ]

    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='reviews')
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')

    # Ratings (1-5)
    autonomy = models.IntegerField(null=True, blank=True, help_text="1-5 rating")
    feedback_quality = models.IntegerField(null=True, blank=True, help_text="1-5 rating")
    clarity = models.IntegerField(null=True, blank=True, help_text="1-5 rating")
    fairness = models.IntegerField(null=True, blank=True, help_text="1-5 rating")
    work_life_balance = models.IntegerField(null=True, blank=True, help_text="1-5 rating")

    duration = models.CharField(max_length=20, choices=DURATION_CHOICES, null=True, blank=True)
    sentiment = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, null=True, blank=True)
    would_work_again = models.CharField(max_length=20, null=True, blank=True, choices=[
        ('yes', 'Yes'),
        ('unsure', 'Unsure'),
        ('no', 'No'),
    ])
    tags = models.TextField(null=True, blank=True, help_text="Comma-separated tags")
    summary = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review for {self.company.name}"

    @property
    def average_score(self):
        scores = [self.autonomy, self.feedback_quality, self.clarity, self.fairness, self.work_life_balance]
        valid_scores = [s for s in scores if s is not None]
        if valid_scores:
            return sum(valid_scores) / len(valid_scores)
        return None


class CompanyAggregate(models.Model):
    """Aggregated scores for companies"""
    CONFIDENCE_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='aggregate')
    n_contributors = models.IntegerField(default=0, verbose_name="Number of Contributors")

    # Average scores
    avg_autonomy = models.FloatField(null=True, blank=True)
    avg_feedback_quality = models.FloatField(null=True, blank=True)
    avg_clarity = models.FloatField(null=True, blank=True)
    avg_fairness = models.FloatField(null=True, blank=True)
    avg_work_life_balance = models.FloatField(null=True, blank=True)

    confidence = models.CharField(max_length=20, choices=CONFIDENCE_CHOICES, default='low')
    public_summary = models.TextField(null=True, blank=True)
    top_tags = models.TextField(null=True, blank=True, help_text="Comma-separated tags")
    best_for = models.TextField(null=True, blank=True)
    hard_for = models.TextField(null=True, blank=True)
    is_publishable = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company Aggregate"
        verbose_name_plural = "Company Aggregates"

    def __str__(self):
        return f"Aggregate for {self.company.name}"

    @property
    def overall_score(self):
        scores = [self.avg_autonomy, self.avg_feedback_quality, self.avg_clarity,
                  self.avg_fairness, self.avg_work_life_balance]
        valid_scores = [s for s in scores if s is not None]
        if valid_scores:
            return sum(valid_scores) / len(valid_scores)
        return None
