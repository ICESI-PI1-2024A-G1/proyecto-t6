from django import forms

class CreateNewTask(forms.Form):
    
    tittle = forms.CharField(label='Titulo de la tarea', max_length=200)
    description = forms.CharField(label='Descripcion de la tarea', widget=forms.Textarea)