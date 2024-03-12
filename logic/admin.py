from django.contrib import admin
from django import forms
from .models import Topic, Video, Session, Course, Participant, ParticipantSession
class VideoInline(admin.TabularInline):
    model = Video
    extra = 1


class SessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'week')
    #inlines = [VideoInline]
    filter_horizontal = ('topics','videos')


# class CourseAdminForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = '__all__'
#         widgets = {
#             'sessions': forms.CheckboxSelectMultiple,
#         }

class SessionInline(admin.TabularInline):
    model = Session
    extra = 0
class CourseAdmin(admin.ModelAdmin):
    inlines = [SessionInline]
    #form = CourseAdminForm
    #filter_horizontal = ('sessions',)


# class ParticipantAdmin(admin.ModelAdmin):

#     filter_horizontal = ('courses')


admin.site.register(Topic)
admin.site.register(Video)
admin.site.register(Session, SessionAdmin)
admin.site.register(Course, CourseAdmin)
# admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Participant)
admin.site.register(ParticipantSession)