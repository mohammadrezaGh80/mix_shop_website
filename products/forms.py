from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Comment


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
