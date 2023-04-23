from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    question = models.TextField()
    view = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        qsn = self.question
        qsn = qsn[:25]+"..." if len(qsn) > 25 else qsn
        return qsn