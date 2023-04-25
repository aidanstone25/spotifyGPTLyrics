from django import forms

class songSearchForm(forms.Form):
	songName = forms.CharField(label="songName", max_length=300)
	songArtist = forms.CharField(label="songArtist", max_length=300)

class search(forms.Form):
	songName = forms.CharField(label="songName", max_length=300)
