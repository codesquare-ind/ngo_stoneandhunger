from django.contrib import admin
from .models import Case, FamilyMembers, EducationalCase, MedicalCase, MedicineCase, ProvisionalCase, GeneralCase, ProjectDonation


admin.site.register(Case)
admin.site.register(GeneralCase)
admin.site.register(EducationalCase)
admin.site.register(MedicineCase)
admin.site.register(MedicalCase)
admin.site.register(ProvisionalCase)
admin.site.register(FamilyMembers)
admin.site.register(ProjectDonation)