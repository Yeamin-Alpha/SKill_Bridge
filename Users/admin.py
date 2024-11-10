from django.contrib import admin
from .models import ProfileImage, PublicProfile, SkillOption, profile,Skill
admin.site.register(profile)
admin.site.register(Skill)
admin.site.register(SkillOption)
admin.site.register(PublicProfile)
admin.site.register(ProfileImage)