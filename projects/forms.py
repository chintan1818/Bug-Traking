from django import forms
from projects.models import Project, Thread, Comment
from django.contrib.auth.models import User


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if kwargs.get('user') != None:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Project
        fields = ['name', 'description', 'tags', 'developers']
        widgets = {
            'description': forms.widgets.Textarea(attrs={'rows': 5}),
            'tags': forms.widgets.Textarea(attrs={'rows': 3}),
        }

    developers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(
            is_active=True, is_staff=False, is_superuser=False).all(),
        widget=forms.widgets.SelectMultiple
    )

    def save(self, commit=True):
        project = super().save(commit=False)
        tags = [tag.strip() for tag in project.tags.split(',')]
        project.tags = ','.join(tags)
        if not hasattr(project, 'manager'):
            project.manager = self.user
        project.save()

        # To save many to many field, we have to call save_m2m
        self.save_m2m()
        return project
