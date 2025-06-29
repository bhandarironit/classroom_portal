from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StudentProfile, TeacherProfile
from .models import ClassRoom, Subject, Module, Assignment, StudentAssignment

admin.site.site_header = "Classroom Management Admin"
admin.site.site_title = "Classroom Admin"
admin.site.index_title = "Welcome to the Dashboard"

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Role Info', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role', 'is_staff', 'is_superuser', 'is_active')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)

# Optional: register student and teacher profiles
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'enrollment_number', 'roll_number', 'grade')
    search_fields = ('user__username', 'enrollment_number', 'roll_number')
    list_filter = ('grade',)

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'subject', 'qualification')
    search_fields = ('user__username', 'employee_id')
    list_filter = ('subject',)


@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'section')
    search_fields = ('name', 'section')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('classrooms',)
    search_fields = ('name',)

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject')
    search_fields = ('name', 'subject__name')
    list_filter = ('subject',)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'teacher', 'classroom', 'due_date', 'total_marks')
    list_filter = ('subject', 'classroom', 'teacher')
    search_fields = ('title',)

@admin.register(StudentAssignment)
class StudentAssignmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'marks_obtained', 'submission_date', 'status')
    list_filter = ('assignment', 'status')
    search_fields = ('student__user__username', 'assignment__title')
