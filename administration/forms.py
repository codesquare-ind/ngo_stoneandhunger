from django import forms
from projects.models import Case, MedicalCase, MedicineCase, EducationalCase, GeneralCase, ProvisionalCase


class CaseBaseForm(forms.ModelForm):
    class Meta:
        model = Case
        exclude = ['uuid', 'created_by', 'type', 'date_of_initiation', 'total_online']


class MedicalForm(CaseBaseForm):
    class Meta:
        model = MedicalCase
        exclude = ['created_by', 'date_of_initiation', 'type', 'uuid', 'total_online']
        widgets = {
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title', 'required': ''}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Case Description', 'required': ''}),
            'requested_amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Requested Amount', 'required': ''}),
            'total_collected': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Total Collected', 'required': ''}),
            'estimation_letter': forms.FileInput(attrs={'class': 'form-control'}),
            'admitted_in_hospital': forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'admitted_hos'}),
            'priority': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Priority', 'required': ''}),
            'other_financial_assistance': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Other Financial Assistances'}),
            'status': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Category', 'required': ''}),
            'nature_of_disease': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Disease', 'required': ''}),
            'name_of_hospital': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hospital', 'required': ''}),
        }


class MedicineForm(CaseBaseForm):
    class Meta:
        model = MedicineCase
        exclude = ['created_by', 'date_of_initiation', 'uuid', 'type', 'total_online']
        widgets = {
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title', 'required': 'true'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Case Description', 'required': 'true'}),
            'requested_amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Requested Amount', 'required': 'true'}),
            'total_collected': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Total Collected'}),
            'priority': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Priority'}),
            'estimation_letter': forms.FileInput(attrs={'class': 'form-control'}),
            'admitted_in_hospital': forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'admitted_hos1'}),
            'other_financial_assistance': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Other Financial Assistances'}),
            'status': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            'nature_of_disease': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Disease', 'required': 'true'}),
            'name_of_medicine': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Medicine', 'required': 'true'}),
            'name_of_hospital': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hospital', 'required': 'true'}),
        }


class EducationalForm(CaseBaseForm):
    class Meta:
        model = EducationalCase
        exclude = ['created_by', 'date_of_initiation', 'uuid', 'type', 'total_online']
        widgets = {
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title', 'required': 'true'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Case Description', 'width': '100%', 'required': 'true'}),
            'requested_amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Requested Amount', 'required': 'true'}),
            'total_collected': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Total Collected'}),
            'priority': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Priority'}),
            'death_cert': forms.FileInput(attrs={'class': 'form-control'}),
            'fee_structure': forms.FileInput(attrs={'class': 'form-control'}),
            'other_financial_assistance': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Other Financial Assistances'}),
            'status': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            'guardian': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mother/Father/Guardian', 'required': 'true'}),
            'name_of_school': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Institution', 'required': 'true'}),
            'location_of_school': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location of Institution', 'required': 'true'}),
            'grade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Grade', 'required': 'true'}),
        }


class ProvisionalForm(CaseBaseForm):
    class Meta:
        model = ProvisionalCase
        exclude = ['created_by', 'date_of_initiation', 'uuid', 'type', 'total_online']
        widgets = {
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title', 'required': 'true'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Case Description', 'required': 'true'}),
            'requested_amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Requested Amount', 'required': 'true'}),
            'total_collected': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Total Collected'}),
            'death_cert': forms.FileInput(attrs={'class': 'form-control'}),
            'priority': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Priority'}),
            'other_financial_assistance': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Other Financial Assistances'}),
            'status': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            'marital_status': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Marital Status', 'required': 'true'})
        }


class GeneralForm(CaseBaseForm):
    class Meta:
        model = GeneralCase
        exclude = ['created_by', 'date_of_initiation', 'uuid', 'type', 'total_online']
        widgets = {
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title', 'required': 'true', 'required': 'true'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Case Description', 'required': 'true'}),
            'requested_amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Requested Amount', 'required': 'true'}),
            'total_collected': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Total Collected'}),
            'priority': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Priority'}),
            'estimated_cost_cert': forms.FileInput(attrs={'class': 'form-control'}),
            'other_financial_assistance': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Other Financial Assistances'}),
            'status': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            'nature_of_aid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nature of Aid', 'required': 'true'}),
        }
