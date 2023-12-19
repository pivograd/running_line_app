from django import forms

class GenerateTextForm(forms.Form):
    text = forms.CharField(label='Введите текст для генерации')