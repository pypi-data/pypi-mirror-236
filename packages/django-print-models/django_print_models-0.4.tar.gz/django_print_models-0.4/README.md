# `django_print_models`

A Django package that provides a management command to print trimmed down
models for easier sharing. Prints your models with *just* the field
definitions, trimming out other methods, properties, etc.

This is handy when you want to ask ChatGPT or fellow humans a question
where the context of your model field definitions is important (e.g. when
trying to build a complex query), but the rest of your crappy model
definition doesn't matter.

## Installation

1. `pip install django-print-models`
2. Add `django_print_models` to your `INSTALLED_APPS` in Django settings.

## Usage

```
python manage.py print_models <app_name> <model_name1> <model_name2> ...
```

## Example

Given the following model definitions:

```python
import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
```

`print_models` will print the following:

```
> python manage.py print_models polls Question Choice
class Question(models.Model):
    id = models.BigAutoField(null=False, blank=True, db_index=False)
    question_text = models.CharField(max_length=200, null=False, blank=False, db_index=False)
    pub_date = models.DateTimeField(null=False, blank=False, db_index=False)

class Choice(models.Model):
    id = models.BigAutoField(null=False, blank=True, db_index=False)
    question = models.ForeignKey("Question", null=False, blank=False, db_index=True)
    choice_text = models.CharField(max_length=200, null=False, blank=False, db_index=False)
    votes = models.IntegerField(null=False, blank=False, db_index=False)
```

Obviously in this simple example it would have been quite easy to just
copy/paste the relevant model definitions, but for larger, more complex
models this becomes tedious.
