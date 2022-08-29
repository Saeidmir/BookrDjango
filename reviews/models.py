from django.contrib import auth
from django.db import models

# Create your models here.
class Publisher(models.Model):
    """A company that publish books"""
    name = models.CharField(max_length=50, help_text="the name of the publisher")
    website = models.URLField(help_text="The publisher's website")
    email = models.EmailField(help_text="The publisher's email address")

    def __str__(self):
        return self.name

class Book(models.Model):
    """ A published book"""
    title = models.CharField(max_length=70, help_text="The title of the book")
    publication_date = models.DateField(verbose_name="Date the book published.")
    isbn = models.CharField(max_length=20, verbose_name="ISBN number of the book.")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    contributor = models.ManyToManyField('Contributor', through='BookContributor')

    def __str__(self):
        return self.title


class Contributor(models.Model):
    """A contribute to the book e.g. Author, Editor, Co-author"""
    first_names = models.CharField(max_length=50, help_text="The contributor's first name or names.")
    last_names = models.CharField(max_length=50 , help_text="the contributor's last name or names")
    email = models.EmailField(help_text="The email address of contributers")

    def __str__(self):
        return f"{self.first_names} - {self.last_names}"
class BookContributor(models.Model):
    class ContributorRole(models.TextChoices):
        AUTHOR = "Author", "AUTHOR"
        CO_AUTHOR = "Co_Author", "CO_AUTHOR"
        EDITOR = "Editor", "EDITOR"

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    role = models.CharField(verbose_name="The role this contributor had in this book.",
                            choices=ContributorRole.choices, max_length=20)

class Review(models.Model):
    """A review of person about books"""
    content = models.TextField(help_text="The review text.")
    rating = models.SmallIntegerField(help_text="The rating the reviewer has given.")
    date_created = models.DateTimeField(auto_now_add=True, help_text="The date and time the review was edited.")
    date_edited = models.DateTimeField(null=True, help_text="The date and time the review edited.")
    creator = models.ForeignKey(auth.get_user_model(),on_delete=models.CASCADE, help_text="the review creator or a person who create this review")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, help_text="The book that the review is for")



