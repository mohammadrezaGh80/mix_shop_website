from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Comment, Question, Answer


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("title", "text", "suggestion", "star_rating", "is_anonymous")
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control'}),
            "text": forms.Textarea(attrs={'class': 'form-control', 'placeholder': _('Write for us...')}),
        }
        labels = {
            "star_rating": _("Give rating"),
        }


class QuestionForm(forms.ModelForm):
    error_messages = {
        "invalid_text": _("Your text must have at least %(min_characters)s characters.")
    }

    class Meta:
        model = Question
        fields = ("text", )
        widgets = {
            "text": forms.Textarea(attrs={'class': 'form-control'})
        }

    def clean_text(self):
        text = self.cleaned_data.get("text")
        min_characters = 7
        if len(text) < min_characters:
            raise ValidationError(
                self.error_messages["invalid_text"],
                code="invalid_text",
                params={"min_characters": min_characters}
            )
        return text


class AnswerForm(QuestionForm):
    class Meta:
        model = Answer
        fields = ("text",)
        widgets = {
            "text": forms.Textarea(attrs={'class': 'form-control'})
        }
