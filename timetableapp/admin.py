from django.contrib import admin
from .models import *

admin.site.register(Course)
admin.site.register(Lecturer)
admin.site.register(Classroom)
admin.site.register(Class)
admin.site.register(ClassCourse)
admin.site.register(SectionClassroom)
admin.site.register(Activity)
admin.site.register(Student)
admin.site.register(RequestChange)

