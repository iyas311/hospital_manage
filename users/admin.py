from django.contrib import admin
from .models import DoctorProfile, PatientProfile, CustomUser

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'is_approved', 'approve_doctor')
    list_filter = ('is_approved', 'specialization')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_editable = ('is_approved',)

    def approve_doctor(self, obj):
        if not obj.is_approved:
            return "❌ Not Approved"
        return "✅ Approved"
    approve_doctor.short_description = 'Approval Status'
    approve_doctor.admin_order_field = 'is_approved'


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'phone')


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_active')
    list_filter = ('user_type', 'is_active')
