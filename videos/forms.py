from .models import Video
from django import forms

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['url']
        labels = {'url':'YouTube URL'}

class SearchForm(forms.Form):
    search_term = forms.CharField(max_length=100, label='Search for videos (just type and wait, do not press enter!):')
