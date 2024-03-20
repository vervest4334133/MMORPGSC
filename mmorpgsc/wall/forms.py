from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Reply


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'name',
            'content',
            'category',
        ]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        content = cleaned_data.get("content")

        if name == content:
            raise ValidationError('Название и текст не должны совпадать')

        if content is not None and len(content) < 5:
            raise ValidationError({
                "content": "Содержание публикации не может быть менее 5 символов."
            })

        return cleaned_data


    def clean_name(self):
        name = self.cleaned_data["name"]
        if name[0].islower():
            raise ValidationError(
                "Название должно начинаться с заглавной буквы"
            )

        return name


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply_text',]
        widgets = {'reply_text': forms.Textarea(attrs={'rows': 3, 'cols': 70, 'placeholder': 'Введите текст отклика...'})}

    def clean(self):
        cleaned_data = super().clean()
        reply_text = cleaned_data.get("reply_text")
        if reply_text is not None and len(reply_text) < 5:
            raise ValidationError({
                "reply_text": "Содержание отклика не может быть менее 5 символов."
            })

        return cleaned_data
