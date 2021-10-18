from django import forms
from projects.models import Project, Thread, Comment


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'tags', 'developers']
        widgets = {
            'description': forms.widgets.Textarea(attrs={'rows': 5}),
            'tags': forms.widgets.Textarea(attrs={'rows': 3}),
        }

    def save(self, commit=True):
        project = super().save(commit=False)
        tags = [tag.strip() for tag in project.tags.split(',')]
        project.tags = ','.join(tags)
        project.save()
        return project
