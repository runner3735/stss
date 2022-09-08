
from django import forms
from .models import Setup, Document, Video, Note, Picture, Tag, Component, Course

class SetupForm(forms.ModelForm):
    class Meta:
        model = Setup
        fields = ['name', 'description', 'courses', 'room', 'location']
    
    def clean_name(self):
        return self.cleaned_data['name'].title()

class SetupNameForm(forms.ModelForm):
    class Meta:
        model = Setup
        fields = ['name',]

class SetupDescriptionForm(forms.ModelForm):
    class Meta:
        model = Setup
        fields = ['description',]

class SetupRoomForm(forms.ModelForm):
    class Meta:
        model = Setup
        fields = ['room',]

class SetupLocationForm(forms.ModelForm):
    class Meta:
        model = Setup
        fields = ['location',]

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['number', 'name']

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

class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ['name',]
    
    def clean_name(self):
        data = self.cleaned_data['name']
        if self.instance.pk:
            if data.lower() != self.instance.name.lower():
                raise forms.ValidationError("You can only edit the casing of a Component object.  You cannot change its content.")
        return data

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

