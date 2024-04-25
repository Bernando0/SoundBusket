from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Song

from .models import Song

def index(request):
    allSongs = Song.objects.all().order_by('-last_updated')
    return render(request, template_name="music/index.html", context={"allSongs" : allSongs})


def search_songs(request): 
    template_path = 'music/search_result.html'
    
    search_query = request.GET.get('search', None)

    if search_query: 
        search_result = Song.objects.filter(
            Q(songName__icontains=search_query) | 
            Q(album__albumName__icontains=search_query) | 
            Q(album__artist__artistName__icontains=search_query)
        ).distinct()
    else: 
        search_result = Song.objects.all()
        
    context = {'search_result' : search_result, 'search_query' : search_query}
    return render(request, template_path, context)


# Create a new song
def create_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('songs_list')
    else:
        form = SongForm()
    return render(request, 'music/song_form.html', {'form': form})

# Read all songs
def songs_list(request):
    songs = Song.objects.all()
    return render(request, 'music/songs_list.html', {'songs': songs})

# Read a specific song
def song_detail(request, pk):
    song = get_object_or_404(Song, pk=pk)
    return render(request, 'music/song_detail.html', {'song': song})

# Update a song
def update_song(request, pk):
    song = get_object_or_404(Song, pk=pk)
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES, instance=song)
        if form.is_valid():
            form.save()
            return redirect('songs_list')
    else:
        form = SongForm(instance=song)
    return render(request, 'music/song_form.html', {'form': form})

# Delete a song
def delete_song(request, pk):
    song = get_object_or_404(Song, pk=pk)
    if request.method == 'POST':
        song.delete()
        return redirect('songs_list')
    return render(request, 'music/song_confirm_delete.html', {'song': song})
