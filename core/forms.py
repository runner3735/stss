
from django import forms
from .models import Asset, Document, Video, Note, Picture, Tag, Purchase

class DateInput(forms.DateInput):
    input_type = 'date'

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'nickname', 'location']
    
    def clean_name(self):
        return self.cleaned_data['name'].title()

class AssetNumberForm(forms.Form):
    number = forms.DecimalField(label='Asset Number', max_digits=4, decimal_places=0)
    cost = forms.DecimalField(label='Cost', max_digits=10, decimal_places=2)

class AssetIdentifierForm(forms.Form):
    identifier = forms.DecimalField(label='Asset Tag Number', max_digits=4, decimal_places=0)

class AssetCloneForm(forms.Form):
    identifier = forms.DecimalField(label='Asset Tag Number', max_digits=4, decimal_places=0)
    serial = forms.CharField(max_length=128, required=False)
    room = forms.BooleanField(required=False)
    department = forms.BooleanField(required=False)
    contacts = forms.BooleanField(required=False)
    tags = forms.BooleanField(required=False)

class TextForm(forms.Form):
    text = forms.CharField(label='Text', max_length=128)

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

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'file']

class DocumentNameForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name',]

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text',]

class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ['name', 'file']

class PictureNameForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ['name',]

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

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['date', 'method', 'reference', 'total', 'shipping']
        widgets = {'date': DateInput()}

# class ComponentForm(forms.ModelForm):
#     class Meta:
#         model = Component
#         fields = ['name',]
    
#     def clean_name(self):
#         data = self.cleaned_data['name']
#         if self.instance.pk:
#             if data.lower() != self.instance.name.lower():
#                 raise forms.ValidationError("You can only edit the casing of a Component object.  You cannot change its content.")
#         return data

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['file', 'name']

class YoutubeForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['url',]

class VideoNameForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['name',]

class VideoThumbnailForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['thumbnail',]

