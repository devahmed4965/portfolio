# portfolio/views.py

from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from .models import (
    UserProfile, Section, VideoProject, PodcastEpisode,
    Skill, Experience, Certificate, Project,
    SocialLink  # Ensure SocialLink is imported
)

def home(request):
    # Retrieve the first user profile (modify logic as needed)
    user_profile = UserProfile.objects.first()

    # Retrieve other content sections
    about_section = Section.objects.filter(identifier='about', is_active=True).first()
    skills = Skill.objects.filter(is_active=True).order_by('order')
    experiences = Experience.objects.filter(is_active=True).order_by('-start_date')
    certificates = Certificate.objects.filter(is_active=True).order_by('order')
    podcast_episodes = PodcastEpisode.objects.filter(is_active=True).order_by('-publication_date')

    # --- Process Video Projects ---
    video_projects_qs = VideoProject.objects.filter(is_active=True).order_by('order')
    video_projects_list = []  # New list to store processed projects
    for project in video_projects_qs:
        if project.technologies:
            # Create a new attribute 'technologies_list' by splitting the comma-separated string,
            # stripping extra spaces, and filtering out any empty values
            project.technologies_list = [tech.strip() for tech in project.technologies.split(',') if tech.strip()]
        else:
            project.technologies_list = []
        video_projects_list.append(project)
    # --- End of Video Projects Processing ---

    # Retrieve projects for the "My Projects" section (adjust ordering as needed)
    projects = Project.objects.all().order_by('order') # Assuming Project model is the general one

    # Retrieve social links
    social_links = SocialLink.objects.filter(url__isnull=False).exclude(url__exact='').order_by('platform') # Fetch active social links, ordered

    context = {
        'profile': user_profile,
        'about_section': about_section,
        'skills': skills,
        # Use the processed list for video projects
        'video_projects': video_projects_list,
        'experiences': experiences,
        'certificates': certificates,
        'podcast_episodes': podcast_episodes,
        'projects': projects,  # Pass the general projects to the template
        'user': request.user,
        'social_links': social_links, # Pass social links to the template

        # Safely determine the site owner's name
        'site_owner_name': (
            user_profile.user.get_full_name()
            if user_profile and user_profile.user and user_profile.user.get_full_name()
            else (user_profile.user.username if user_profile and user_profile.user else _("ملفي الشخصي"))
        ),
    }
    return render(request, 'portfolio/index.html', context)

# Add other views here if you have them (like contact_form_submit, etc.)