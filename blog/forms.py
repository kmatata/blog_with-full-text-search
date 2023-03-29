from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25,required=True,widget=forms.TextInput(attrs={"placeholder":"Recepient's Name","class":"bg-white input input-secondary w-full input-xs max-w-xs"}))
    email = forms.EmailField(required=False,widget=forms.EmailInput(attrs={"placeholder":"my-email","class":"input input-secondary input-xs w-full max-w-xs"}))
    to = forms.EmailField(required=True,widget=forms.EmailInput(attrs={"placeholder":"recepient@theiremail.com","class":"input input-secondary input-xs bg-white w-full max-w-xs"}))
    comments = forms.CharField(required=False,widget=forms.Textarea(attrs={"placeholder":"ANY COMMENTS?","class":"bg-white textarea textarea-xs textarea-bordered"}))

class CommentForm(forms.ModelForm):
    name = forms.CharField(max_length=80,required=True,widget=forms.TextInput(attrs={"placeholder":"username?","class":"bg-white input input-secondary w-full input-xs max-w-xs"}))
    email = forms.EmailField(required=False,widget=forms.EmailInput(attrs={"placeholder":"email","class":"bg-white input input-secondary input-xs w-full max-w-xs"}))
    body = forms.CharField(required=False,widget=forms.Textarea(attrs={"placeholder":"comment","class":"max-h-1.5 w-full bg-white textarea textarea-xs textarea-bordered"}))
    class Meta:
        model = Comment
        fields = ('name','email','body',)

class SearchForm(forms.Form):
    query = forms.CharField(required=True,widget=forms.TextInput(attrs={"placeholder":"search?","class":"bg-white input input-secondary w-full input-xs max-w-xs"}))