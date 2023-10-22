from django.db import models


class Informations(models.Model):
    release_date = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    resume = models.TextField()
    category = models.CharField(max_length=255)
    manga_title = models.CharField(max_length=255, null=False, default="unknown")

    class Meta:
        verbose_name = 'Information'

    def __str__(self):
        return f"{self.author} - {self.release_date}"


class Pages(models.Model):

    informations = models.ForeignKey(Informations, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    chapters = models.JSONField()

    class Meta:
        verbose_name = 'Page'

    def __str__(self):
        return self.name

    @property
    def number_chapter(self):
        return len(self.chapters) - 1
