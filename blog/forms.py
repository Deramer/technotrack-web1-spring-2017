from django.forms import ModelForm, Textarea
from django import forms
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .models import Comment, CommentsLikes


class CommentForm(ModelForm):
    parent_id = forms.IntegerField(widget = forms.HiddenInput(), initial = -1)

    class Meta:
        model = Comment
        fields = ['text', 'parent_id',]
    
    def clean_parent_id(self):
        parent_id = self.cleaned_data['parent_id']
        try:
            if int(parent_id) < 0:
                raise ValidationError('Invalid parent_id, < 0')
        except:
            raise ValidationError('Invalid parent_id, not an int %(parent_id)s', params={'parent_id': parent_id})
        try:
            Comment.objects.get(id=int(parent_id))
        except ObjectDoesNotExist:
            raise ValidationError('No such parent in database, parent_id %(parent_id)s', params={'parent_id': parent_id})
        return parent_id

class CommentLikeForm(ModelForm):
    node_id = forms.IntegerField(widget = forms.HiddenInput(), initial = -1)
    like = forms.BooleanField(widget = forms.HiddenInput(), required = False)

    class Meta:
        model = CommentsLikes
        fields = ['node_id', 'like']

    def clean_node_id(self):
        node_id = self.cleaned_data['node_id']
        try:
            if int(node_id) < 0:
                raise ValidationError('Invalid node_id, < 0')
        except:
            raise ValidationError('Invalid node_id, not an int %(node_id)s', params={'node_id': node_id})
        try:
            Comment.objects.get(id=int(node_id))
        except ObjectDoesNotExist:
            raise ValidationError('No such node in database, node_id %(node_id)s', params={'node_id': node_id})
        return node_id
