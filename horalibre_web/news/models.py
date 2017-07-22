
# Python imports
from datetime import datetime

# Django imports
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
@python_2_unicode_compatible
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField("Texto", null=True, blank=True, max_length=5000)
    author = models.ForeignKey(User,  related_name='article_author',
                               on_delete=models.SET_NULL, null=True)
    is_draft = models.BooleanField(default=False)
    creation_date = models.DateField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.is_draft:
            draft = "(Es borrador)"
        else:
            draft = ""

        title = self.title

        if self.author is None:
            author = "Usuario eliminado"
        else:
            author = self.author.get_full_name()

        if (len(title) > 30):
            title = title[:30] + "[...]"
        return (str(self.creation_date.strftime('%d/%m/%y')) + " - Titulo:" + title + " - Autor:" + 
                author + " " + draft)

    def log_str(self):
        title = self.title
        creation_date = self.creation_date.strftime('%d/%m/%y')
        if (len(title) > 45):
            title = title[:45] + "[...]"
        return (str(creation_date) + ": " + title + " (id: " + str(self.id) + ")")

