
# Project imports
from .models import Record, Patient, Professional, Case, Secretary

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ProfessionalInline(admin.StackedInline):
    model = Professional
    can_delete = False
    verbose_name_plural = 'professional'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfessionalInline, )

# Register your models here.

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Professional)
admin.site.register(Record)
admin.site.register(Patient)
admin.site.register(Case)
admin.site.register(Secretary)
