from django.shortcuts import render
from django.http import HttpResponse
import openai
from .forms import songSearchForm
from .musixmatch import musicmatch
#TODO add to env
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.contrib.auth.models import User
from gptlyrics.settings import OPEN_AI_KEY, MM_KEY, sp_client_id, sp_client_secret
from .spotipyFuuncs import SpotipyConnection
# TODO https://stackoverflow.com/questions/14647723/django-forms-if-not-valid-show-form-with-error-message
def openAISearch(artist,song):
    mm = musicmatch(MM_KEY)
    openai.api_key = OPEN_AI_KEY
    #TODO
    openai.organization = 'org-'
    lyrics = mm.song_search(song,artist)
    if lyrics:
        #TODO NEEED free trial or put money in there or something
        promptRating = f"Given the following lyrics from the song {song} by {artist}, please analyze the following lyrics wholeistically. please also give it a rating from 0-10 on its literary merit. Please do it in the following format: Song meaning: ..... Song rating: X/10. Song rating explanation: ....  . Here are the lyrics: {lyrics}."                
        ans = openai.Completion.create(model = 'text-davinci-003',prompt = promptRating,temperature = 0.3,max_tokens=2000,stop='/n/n/n')
        return ans.choices[0]['text']
        #return HttpResponse(ans.choices[0]['text'])
    return HttpResponse('invalid lyrics')

def home(request):
    form = songSearchForm(request.POST or None)
    
    if request.method == 'POST':
        openai.api_key = OPEN_AI_KEY
        mm = musicmatch(MM_KEY)
        if form.is_valid():
            song_name = form.cleaned_data['songName']
            song_artist = form.cleaned_data['songArtist']
            lyrics = mm.song_search(song_name,song_artist)
            if lyrics:
                #TODO NEEED free trial or put money in there or something
                promptRating = f"Given the following lyrics from the song {song_name} by {song_artist}, please analyze the following lyrics wholeistically. please also give it a rating from 0-10 on its literary merit. Please do it in the following format: Song meaning: ..... Song rating: X/10. Song rating explanation: ....  . Here are the lyrics: {lyrics}."                
                ans = openai.Completion.create(model = 'text-davinci-003',prompt = promptRating,temperature = 0.3,max_tokens=1000,stop='/n/n/n')
                return HttpResponse(ans.choices[0]['text'])
            return render(request,'main/home.html',{})
        return HttpResponse('what am i cooking 🔥')
    #TODO store an an envirment variable or something more safe
    openai.organization = 'org-'
    
    return render(request,'main/home.html',{})
    #return HttpResponse(OPEN_AI_KEY)
def search(request):
    query = request.GET.get('q', '')
    if query:
        sp = SpotipyConnection(client_id=sp_client_id, client_secret=sp_client_secret)
        #context = {'search': sp.searchbar(query)}
        context = {'search': sp.songSearch(query)}
        return render(request,'main/search.html',context=context)
    return render(request,'main/search.html',{})

def search_results(request):
    if request.method == 'POST':
        #TODO how do i get the context of what was clicked 
        songName = request.POST.get('songName')
        songArtist = request.POST.get('songArtist')
        context = openAISearch(artist=songArtist,song=songName)
        return HttpResponse('gang?')
        return render(request,'main/search_results.html',context=context)
def create_user():
    def login():
        sp_oauth = create_spotify_oauth()
        auth_url = sp_oauth.get_authorize_url()
        sp = spotipy.Spotify(auth_manager=sp_oauth)
        signed_in_user=sp.current_user()
        #TODO
        user = User.query.filter_by(spotify_user_id=signed_in_user['id']).first()
        #if user:
        #    login_user(user=user,remember=True)
        #else:
        #    new_user = User(spotify_user_id=signed_in_user['id'])
        #    db.session.add(new_user)
        #    db.session.commit()
        #    login_user(user=new_user,remember=True)

        #return redirect(auth_url)

def create_spotify_oauth():
    return SpotifyOAuth(
            client_id='',
            client_secret='',
            redirect_uri="http://127.0.0.1:8000/authorize",
            scope="user-top-read user-library-read")


