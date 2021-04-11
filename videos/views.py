from django.shortcuts import render, redirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView
from .models import Theme, Video
from .forms import VideoForm, SearchForm
from django.http import Http404, JsonResponse
from django.forms.utils import ErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import urllib
import requests

YOUTUBE_API_KEY = 'AIzaSyBWJ35sxnDu9bEVr0wdQ1IMB8ZauscIFEI'

def HomePageView(request):
    recent_themes = Theme.objects.all().order_by('-id')[:3]
    return render(request, 'home.html', {'recent_themes':recent_themes})

@login_required
def DashboardView(request):
    themes = Theme.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'themes':themes})

class ThemeCreateView(LoginRequiredMixin, CreateView):
    model = Theme
    fields = ['title']
    template_name = 'create_theme.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(ThemeCreateView, self).form_valid(form)
        return redirect('dashboard')

class ThemeDetailView(DetailView):
    model = Theme
    template_name = 'detail_theme.html'

class ThemeUpdateView(LoginRequiredMixin, UpdateView):
    model = Theme
    fields = ['title']
    template_name = 'update_theme.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        theme = super(ThemeUpdateView, self).get_object()
        if not theme.user == self.request.user:
            raise Http404
        return theme

class ThemeDeleteView(LoginRequiredMixin, DeleteView):
    model = Theme
    template_name = 'delete_theme.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        theme = super(ThemeDeleteView, self).get_object()
        if not theme.user == self.request.user:
            raise Http404
        return theme

@login_required
def AddVideoView(request, pk):
    form = VideoForm()
    search_form = SearchForm()
    theme = Theme.objects.get(pk=pk)
    if not theme.user == request.user:
        raise Http404

    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            video = Video()
            video.theme = theme
            video.url = form.cleaned_data['url']
            parsed_url = urllib.parse.urlparse(video.url)
            video_id = urllib.parse.parse_qs(parsed_url.query).get('v')

            if video_id:
                video.youtube_id = video_id[0]
                response = requests.get(f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={video_id[0]}&key={YOUTUBE_API_KEY}')
                json = response.json()
                title = json['items'][0]['snippet']['title']
                video.title = title
                video.save()
                return redirect('detail_theme', pk)
            else:
                errors = form._errors.setdefault('url', ErrorList())
                errors.append('Please use a YouTube URL')

    return render(request, 'add_video.html', {'form':form, 'search_form':search_form, 'theme':theme})

@login_required
def VideoSearchView(request):
            search_form = SearchForm(request.GET)
            if search_form.is_valid():
                encoded_search_term = urllib.parse.quote(search_form.cleaned_data['search_term'])
                response = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&q={ encoded_search_term }&key={ YOUTUBE_API_KEY }')
                return JsonResponse(response.json())
            return JsonResponse({'error':'Not able to validate form'})

class VideoDeleteView(LoginRequiredMixin, DeleteView):
    model = Video
    template_name = 'delete_video.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        video = super(VideoDeleteView, self).get_object()
        if not video.theme.user == self.request.user:
            raise Http404
        return video
