from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Company, Manager, JobPosting, Review, CompanyAggregate


# ==================== RESOURCES (Import/Export) ====================

class CompanyResource(resources.ModelResource):
    class Meta:
        model = Company
        fields = ('id', 'name', 'domain', 'lat', 'lng', 'city', 'region', 'country', 'logo_url', 'industry', 'size')
        skip_unchanged = True
        report_skipped = True


class ManagerResource(resources.ModelResource):
    class Meta:
        model = Manager
        fields = ('id', 'company', 'display_name', 'title', 'team', 'location', 'is_verified')
        skip_unchanged = True


class JobPostingResource(resources.ModelResource):
    class Meta:
        model = JobPosting
        fields = ('id', 'company', 'title', 'team', 'location', 'lat', 'lng', 'is_remote', 'source', 'url', 'salary')
        skip_unchanged = True


class ReviewResource(resources.ModelResource):
    class Meta:
        model = Review
        fields = ('id', 'company', 'manager', 'autonomy', 'feedback_quality', 'clarity', 'fairness',
                  'work_life_balance', 'duration', 'sentiment', 'would_work_again', 'tags', 'summary')
        skip_unchanged = True


# ==================== INLINE ADMIN ====================

class ManagerInline(admin.TabularInline):
    model = Manager
    extra = 0
    fields = ['display_name', 'title', 'team', 'is_verified']


class JobPostingInline(admin.TabularInline):
    model = JobPosting
    extra = 0
    fields = ['title', 'team', 'location', 'is_remote', 'url']


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    fields = ['autonomy', 'feedback_quality', 'clarity', 'fairness', 'work_life_balance', 'sentiment']
    readonly_fields = ['autonomy', 'feedback_quality', 'clarity', 'fairness', 'work_life_balance', 'sentiment']


# ==================== ADMIN CLASSES ====================

@admin.register(Company)
class CompanyAdmin(ImportExportModelAdmin):
    resource_class = CompanyResource
    list_display = ['name', 'city', 'region', 'industry', 'size', 'job_count', 'manager_count', 'created_at']
    list_filter = ['industry', 'size', 'region', 'country']
    search_fields = ['name', 'domain', 'city']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ManagerInline, JobPostingInline]

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'domain', 'industry', 'size')
        }),
        ('Location', {
            'fields': ('lat', 'lng', 'city', 'region', 'country')
        }),
        ('Branding', {
            'fields': ('logo_url',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def job_count(self, obj):
        return obj.jobs.count()
    job_count.short_description = 'Jobs'

    def manager_count(self, obj):
        return obj.managers.count()
    manager_count.short_description = 'Managers'


@admin.register(Manager)
class ManagerAdmin(ImportExportModelAdmin):
    resource_class = ManagerResource
    list_display = ['display_name', 'company', 'title', 'team', 'is_verified', 'review_count', 'created_at']
    list_filter = ['is_verified', 'company__industry']
    search_fields = ['display_name', 'title', 'team', 'company__name']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['company']
    inlines = [ReviewInline]

    fieldsets = (
        ('Basic Info', {
            'fields': ('company', 'display_name', 'title', 'team', 'location')
        }),
        ('Verification', {
            'fields': ('is_verified',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def review_count(self, obj):
        return obj.reviews.count()
    review_count.short_description = 'Reviews'


@admin.register(JobPosting)
class JobPostingAdmin(ImportExportModelAdmin):
    resource_class = JobPostingResource
    list_display = ['title', 'company', 'team', 'location', 'is_remote', 'source', 'created_at']
    list_filter = ['is_remote', 'source', 'company__industry']
    search_fields = ['title', 'team', 'company__name', 'location']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['company']


@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    resource_class = ReviewResource
    list_display = ['company', 'manager', 'avg_score', 'sentiment', 'would_work_again', 'created_at']
    list_filter = ['sentiment', 'would_work_again', 'duration']
    search_fields = ['company__name', 'manager__display_name', 'summary']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    autocomplete_fields = ['company', 'manager']

    fieldsets = (
        ('Target', {
            'fields': ('company', 'manager')
        }),
        ('Ratings (1-5)', {
            'fields': ('autonomy', 'feedback_quality', 'clarity', 'fairness', 'work_life_balance')
        }),
        ('Feedback', {
            'fields': ('duration', 'sentiment', 'would_work_again', 'tags', 'summary')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def avg_score(self, obj):
        score = obj.average_score
        if score:
            return f"{score:.1f}"
        return "-"
    avg_score.short_description = 'Avg Score'


@admin.register(CompanyAggregate)
class CompanyAggregateAdmin(admin.ModelAdmin):
    list_display = ['company', 'n_contributors', 'overall', 'confidence', 'is_publishable', 'updated_at']
    list_filter = ['confidence', 'is_publishable']
    search_fields = ['company__name']
    ordering = ['-updated_at']
    readonly_fields = ['updated_at']
    autocomplete_fields = ['company']

    fieldsets = (
        ('Company', {
            'fields': ('company',)
        }),
        ('Statistics', {
            'fields': ('n_contributors', 'confidence', 'is_publishable')
        }),
        ('Average Scores', {
            'fields': ('avg_autonomy', 'avg_feedback_quality', 'avg_clarity', 'avg_fairness', 'avg_work_life_balance')
        }),
        ('AI-Generated Content', {
            'fields': ('public_summary', 'top_tags', 'best_for', 'hard_for')
        }),
        ('Timestamps', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )

    def overall(self, obj):
        score = obj.overall_score
        if score:
            return f"{score:.1f}"
        return "-"
    overall.short_description = 'Overall Score'


# Customize admin site
admin.site.site_header = "ManagerPulse Admin"
admin.site.site_title = "ManagerPulse Admin Portal"
admin.site.index_title = "Welcome to ManagerPulse Admin"
