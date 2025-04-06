from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

# --- User Profile (Includes contact_email) ---
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name=_("User"))
    bio = models.TextField(blank=True, verbose_name=_("Bio"))
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, verbose_name=_("Profile Picture"))
    job_title = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Job Title(s)"),
        help_text=_("e.g., Web Developer | Graphic Designer")
    )
    linkedin_url = models.URLField(blank=True, verbose_name=_("LinkedIn Profile URL"))
    github_url = models.URLField(blank=True, verbose_name=_("GitHub Profile URL"))
    website_url = models.URLField(blank=True, verbose_name=_("Personal Website URL"))
    contact_email = models.EmailField(blank=True, verbose_name=_("Contact Email"))

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")


# --- Dynamic Sections (Identifier made nullable) ---
ANIMATION_CHOICES = [
    ('', _('None')),
    ('fade-up', _('Fade Up')),
    ('fade-down', _('Fade Down')),
    ('fade-left', _('Fade Left')),
    ('fade-right', _('Fade Right')),
    ('zoom-in', _('Zoom In')),
    # Add more AOS animations if desired
]

class Section(models.Model):
    identifier = models.CharField(
        max_length=50,
        unique=True,
        null=True,        # Allows the database column to be NULL
        blank=True,       # Allows the field to be blank in forms/admin
        verbose_name=_("Identifier"),
        help_text=_("Unique ID for this section (e.g., 'about', 'contact_info'). Used internally.")
    )
    title = models.CharField(max_length=100, blank=True, verbose_name=_("Section Title (Optional)"))
    content = models.TextField(blank=True, verbose_name=_("Content (HTML allowed if needed)"))
    order = models.IntegerField(default=0, verbose_name=_("Order"))
    animation_style = models.CharField(
        max_length=50,
        choices=ANIMATION_CHOICES,
        blank=True,
        default='fade-up',
        verbose_name=_("AOS Animation Style")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Active?"))

    def __str__(self):
        return self.identifier if self.identifier else f"Section ID {self.pk}"

    class Meta:
        ordering = ['order']
        verbose_name = _("Managed Section")
        verbose_name_plural = _("Managed Sections")


# --- Video Projects (Using the Video Model structure) ---
class VideoProject(models.Model):  # Renamed for clarity
    title = models.CharField(max_length=100, verbose_name=_("Project Title"))
    description = models.TextField(verbose_name=_("Description"))
    video_file = models.FileField(upload_to='project_videos/', verbose_name=_("Video File"))
    poster_image = models.ImageField(
        upload_to='project_posters/',
        blank=True,
        null=True,
        verbose_name=_("Video Poster Image (Optional)")
    )
    technologies = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Technologies Used"),
        help_text=_("Comma-separated (e.g., HTML, CSS, Python)")
    )
    link = models.URLField(blank=True, null=True, verbose_name=_("Project Link (Optional)"))
    order = models.IntegerField(default=0, verbose_name=_("Order"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active?"))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']
        verbose_name = _("Video Project")
        verbose_name_plural = _("Video Projects")


# --- Skills ---
class Skill(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Skill Name"))
    icon_class = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Font Awesome Icon Class (e.g., 'fab fa-python')")
    )
    icon_image = models.ImageField(
        upload_to='skill_icons/',
        blank=True,
        null=True,
        verbose_name=_("Icon Image (alternative)")
    )
    color = models.CharField(
        max_length=7,
        blank=True,
        help_text=_("Hex color code (e.g., #3776ab)"),
        verbose_name=_("Icon Color")
    )
    order = models.IntegerField(default=0, verbose_name=_("Order"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active?"))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")


# --- Experience ---
class Experience(models.Model):
    title = models.CharField(max_length=150, verbose_name=_("Title / Position"))
    company_or_institution = models.CharField(max_length=100, verbose_name=_("Company / Institution"))
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(blank=True, null=True, verbose_name=_("End Date (Leave blank if current)"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    is_education = models.BooleanField(default=False, verbose_name=_("Is this education?"))
    order = models.IntegerField(default=0, verbose_name=_("Order (Recent first)"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active?"))  # Added is_active field

    def __str__(self):
        return f"{self.title} at {self.company_or_institution}"

    class Meta:
        ordering = ['-start_date']
        verbose_name = _("Experience/Education")
        verbose_name_plural = _("Experience/Education")


# --- Certificates ---
class Certificate(models.Model):
    title = models.CharField(max_length=150, verbose_name=_("Certificate Title"))
    issuing_organization = models.CharField(max_length=100, blank=True, verbose_name=_("Issuing Organization"))
    image = models.ImageField(upload_to='certificates/', verbose_name=_("Certificate Image/Screenshot"))
    link = models.URLField(blank=True, null=True, verbose_name=_("Verification Link (Optional)"))
    date_issued = models.DateField(blank=True, null=True, verbose_name=_("Date Issued (Optional)"))
    order = models.IntegerField(default=0, verbose_name=_("Order"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active?"))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']
        verbose_name = _("Certificate")
        verbose_name_plural = _("Certificates")


class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان المشروع")
    description = models.TextField(verbose_name="وصف المشروع")
    technologies = models.CharField(max_length=500, blank=True, null=True, verbose_name="التقنيات المستخدمة")
    image = models.ImageField(upload_to='projects/', blank=True, null=True, verbose_name="صورة المشروع")
    link = models.URLField(blank=True, null=True, verbose_name="رابط المشروع")
    order = models.PositiveIntegerField(default=0, verbose_name="الترتيب")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']
        verbose_name = "مشروع"
        verbose_name_plural = "مشاريعي"
# --- Podcast Episodes ---
class PodcastEpisode(models.Model):
    title = models.CharField(max_length=150, verbose_name=_("Episode Title"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    cover_image = models.ImageField(upload_to='podcast_covers/', verbose_name=_("Cover Image"))
    audio_file = models.FileField(upload_to='podcast_audio/', verbose_name=_("Audio File (MP3, etc.)"))
    duration = models.CharField(max_length=20, blank=True, verbose_name=_("Duration (e.g., 30:15)"))
    publication_date = models.DateField(verbose_name=_("Publication Date"))
    order = models.IntegerField(default=0, verbose_name=_("Order (Recent first usually)"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active?"))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publication_date', 'order']
        verbose_name = _("Podcast Episode")
        verbose_name_plural = _("Podcast Episodes")


# --- Signal to create or update user profile ---
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    profile, created = UserProfile.objects.get_or_create(user=instance)
    if not created:
        profile.save()

# portfolio/models.py
from django.db import models

# ... (Keep your existing models: PodcastEpisode, VideoProject, Certificate, Experience, Skill, Project) ...

class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('github', 'GitHub'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('whatsapp', 'WhatsApp'),
        ('telegram', 'Telegram'),
        # Add other platforms as needed
    ]
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES, unique=True, verbose_name="المنصة")
    url = models.URLField(max_length=200, verbose_name="الرابط (URL)")
    icon_class = models.CharField(max_length=50, blank=True, null=True, verbose_name="فئة الأيقونة (مثل fab fa-facebook-f)", help_text="اختياري: أدخل فئة Font Awesome (مثل fab fa-linkedin). إذا تركت فارغاً، سيتم استخدام اسم المنصة.")

    class Meta:
        verbose_name = "رابط تواصل اجتماعي"
        verbose_name_plural = "روابط التواصل الاجتماعي"
        ordering = ['platform'] # Optional: order links alphabetically by platform

    def __str__(self):
        return self.get_platform_display() # Display the human-readable platform name