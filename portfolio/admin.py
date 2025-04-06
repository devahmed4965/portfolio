# portfolio/admin.py - النسخة المعدلة
from django.contrib import admin
from .models import (UserProfile, Section, VideoProject, PodcastEpisode,Skill, Experience, Certificate,Project,SocialLink # أضف هذه إذا قمت بتفعيلها في models.py
                    )
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# UserProfile Inline and UserAdmin (لا تغيير هنا)
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = _('Profile')
    fk_name = 'user'
    # يمكنك إضافة حقول للـ UserProfile مباشرة هنا إذا أردت
    # fields = ('bio', 'profile_picture', 'job_title', 'linkedin_url', 'github_url', 'website_url', 'contact_email')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    search_fields = ('title',)
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_profile_job_title')
    def get_profile_job_title(self, instance):
        try: return instance.profile.job_title
        except UserProfile.DoesNotExist: return _('No profile')
    get_profile_job_title.short_description = _('Job Title')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Section Admin
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'title', 'order', 'animation_style', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('order', 'animation_style', 'is_active')
    search_fields = ('identifier', 'title', 'content')

# VideoProject Admin (تحديث اسم النموذج)
@admin.register(VideoProject)
class VideoProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_poster_thumbnail', 'order', 'technologies', 'link', 'is_active')
    list_filter = ('is_active', 'technologies')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description', 'technologies')
    readonly_fields = ('display_poster_preview',) # لعرض صورة البوستر

    def display_poster_thumbnail(self, obj):
        if obj.poster_image: return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.poster_image.url)
        return _("No Poster")
    display_poster_thumbnail.short_description = _('Poster')

    def display_poster_preview(self, obj):
        if obj.poster_image: return format_html('<img src="{}" style="max-height: 200px; max-width: 300px;" />', obj.poster_image.url)
        return _("No Poster")
    display_poster_preview.short_description = _('Poster Preview')

# PodcastEpisode Admin (نموذج جديد)
@admin.register(PodcastEpisode)
class PodcastEpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_cover_thumbnail', 'publication_date', 'duration', 'order', 'is_active')
    list_filter = ('is_active', 'publication_date')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')
    readonly_fields = ('display_cover_preview',)
    date_hierarchy = 'publication_date' # يضيف فلتر تاريخ

    def display_cover_thumbnail(self, obj):
        if obj.cover_image: return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.cover_image.url)
        return _("No Cover")
    display_cover_thumbnail.short_description = _('Cover')

    def display_cover_preview(self, obj):
        if obj.cover_image: return format_html('<img src="{}" style="max-height: 200px; max-width: 300px;" />', obj.cover_image.url)
        return _("No Cover")
    display_cover_preview.short_description = _('Cover Preview')

# portfolio/admin.py - Modified

# ... (Keep UserProfile, UserAdmin, SectionAdmin, VideoProjectAdmin, PodcastEpisodeAdmin registrations) ...

# قم بتسجيل النماذج الاختيارية إذا قمت بتفعيلها في models.py
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_class', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name',)

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_or_institution', 'start_date', 'end_date', 'is_education')
    list_filter = ('is_education',)
    search_fields = ('title', 'company_or_institution', 'description')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('title', 'issuing_organization', 'date_issued', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'issuing_organization')

# ... (Keep site customization at the end) ...

# عناوين لوحة التحكم (لا تغيير هنا)
admin.site.site_header = _("Portfolio Control Panel")
admin.site.site_title = _("Portfolio Management")
admin.site.index_title = _("Welcome to the Control Panel")

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'icon_class') # Columns to show in the admin list view
    search_fields = ('platform', 'url') # Enable searching by platform or URL