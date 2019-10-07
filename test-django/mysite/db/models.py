from django.db import models

class Textbook(models.Model):
    textbook_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.textbook_text