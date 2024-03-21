
from django import forms
from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class PeopleSearchForm(forms.Form):
    status = forms.ChoiceField(choices=[('', 'Active')] + Person.status_choices + [(5, 'All')], required=False)
    search = forms.CharField(max_length=128, required=False)

class AssetSearchForm(forms.Form):
    sortby = forms.ChoiceField(choices=[('-id', 'Created'),('name', 'Name'),('model', 'Model'),('inventoried', 'Inventory Date'),('-identifier', 'Asset Tag'),('department', 'Department')], required=False, initial='-id')
    status = forms.ChoiceField(choices=Asset.status_choices + [('','All')], required=False, initial=1)
    searchin = forms.ChoiceField(choices=[('N', 'Name/Nickname'),('M', 'Manufacturer'),('L', 'Model'),('S', 'Serial Number'),('I', 'Asset Tag'),('D', 'Inventory Date'),('T', 'Department')], required=False, initial='N')
    search = forms.CharField(max_length=128, required=False)

class JobSearchForm(forms.Form):
    sortby = forms.ChoiceField(choices=[('-id', 'Created'),('status', 'Status'),('kind', 'Type'),('category', 'Category'),('deadline', 'Deadline')], required=False, initial='-id')
    status = forms.ChoiceField(choices=Job.status_choices + [('','All')], required=False, initial=1)
    searchin = forms.ChoiceField(choices=[('N', 'Name'),('D', 'Details'),('B', 'Budget'),('C', 'Course'),('L', 'Location'),('Y', 'Year')], required=False, initial='N')
    search = forms.CharField(max_length=128, required=False)

class PurchaseSearchForm(forms.Form):
    sortby = forms.ChoiceField(choices=[('-id', 'Created'),('-date', 'Date'),('vendor', 'Vendor'),('reference', 'Reference'),('-total', 'Total'),('purchaser', 'Purchaser')], required=False, initial='-id')
    method = forms.ChoiceField(choices=[('', 'Any')] + Purchase.method_choices, required=False)
    searchin = forms.ChoiceField(choices=[('V', 'Vendor'),('R', 'Reference'),('D', 'Date'),('P', 'Purchaser')], required=False, initial='R')
    search = forms.CharField(max_length=128, required=False)

class AssetNumberForm(forms.Form):
    number = forms.DecimalField(label='Asset Number', max_digits=4, decimal_places=0)
    cost = forms.DecimalField(label='Cost', max_digits=10, decimal_places=2)

class AssetIdentifierForm(forms.Form):
    identifier = forms.DecimalField(label='Asset Tag Number', max_digits=4, decimal_places=0)

class JobIdentifierForm(forms.Form):
    identifier = forms.CharField(label='Job ID', max_length=8)

class AssetCloneForm(forms.Form):
    identifier = forms.DecimalField(label='Asset Tag Number', max_digits=4, decimal_places=0)
    serial = forms.CharField(max_length=128, required=False)
    room = forms.BooleanField(required=False)
    department = forms.BooleanField(required=False)
    contacts = forms.BooleanField(required=False)
    tags = forms.BooleanField(required=False)

class TextForm(forms.Form):
    text = forms.CharField(max_length=128, required=False)

class DepartmentForm(forms.Form):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label=None)

class RoomForm(forms.Form):
    room = forms.ModelChoiceField(queryset=Room.objects.all(), empty_label=None)

# Download

class DownloadForm(forms.ModelForm):
    class Meta:
        model = Download
        fields = ['url', 'quality']

# Asset

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'nickname', 'location']
    
    def clean_name(self):
        return self.cleaned_data['name'].title()
    
class AssetInfoForm(forms.Form):
    manufacturer = forms.CharField(label='Manufacturer', max_length=128, required=False)
    model = forms.CharField(label='Model', max_length=128, required=False)
    name = forms.CharField(label='Name', max_length=128, required=False)

class AssetNameForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name',]

class AssetNicknameForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['nickname',]

class AssetModelForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['model',]

class AssetInventoriedForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['inventoried',]

class AssetSerialForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['serial',]

class AssetStatusForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['status',]

class AssetLocationForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['location',]

# Job
        
class JobNameForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['name',]

class JobBudgetForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['budget',]

class JobCourseForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['course',]

class JobLocationForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['location',]

class JobOpenedForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['opened',]

class JobDeadlineForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['deadline',]

class JobClosedForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['closed',]

class JobStatusForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['status',]

class JobCategoryForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['category',]

class JobKindForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['kind',]

class JobDetailsForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['details',]

# PMI

class PMIForm(forms.ModelForm):
    class Meta:
        model = PMI
        fields = ['last_job', 'frequency']

    def clean_last_job(self):
        data = self.cleaned_data['last_job']
        if self.instance.pk:
            if not Job.objects.filter(identifier=data).exists():
                raise forms.ValidationError("You must enter the identifier of an existing job, or leave blank.")
        return data
    
class PMINameForm(forms.ModelForm):
    class Meta:
        model = PMI
        fields = ['name',]        

class PMIFrequencyForm(forms.ModelForm):
    class Meta:
        model = PMI
        fields = ['frequency',] 

class PMILocationForm(forms.ModelForm):
    class Meta:
        model = PMI
        fields = ['location',]        

class PMILastForm(forms.ModelForm):
    class Meta:
        model = PMI
        fields = ['last',]

class PMINextForm(forms.ModelForm):
    class Meta:
        model = PMI
        fields = ['next',]        

class PMIDetailsForm(forms.ModelForm):
    class Meta:
        model = PMI
        fields = ['details',]   

# Person
        
class PersonNewForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first', 'last',]        
        
class PersonPhoneForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['phone',]

class PersonEmailForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['email',]

class PersonStatusForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['status',]

# File

class FileNameForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name',]

# Note
        
class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text',]

# Tag
        
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['text',]
    
    def clean_text(self):
        data = self.cleaned_data['text']
        if self.instance.pk:
            if data.lower() != self.instance.text.lower():
                raise forms.ValidationError("You can only edit the casing of a Tag object.  You cannot change its content.")
        return data

# Purchase
    
class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['date', 'method', 'reference', 'vreference', 'funding', 'edorda', 'total', 'shipping']
        widgets = {'date': DateInput()}

class PurchaseEditForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['date', 'purchaser', 'method', 'reference', 'vendor', 'vreference', 'funding', 'edorda', 'total', 'shipping']
        widgets = {'date': DateInput()}

# Work
        
class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ['date', 'hours', 'summary']
        widgets = {'date': DateInput()}
