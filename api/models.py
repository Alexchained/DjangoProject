from django.db import models
from django.contrib.auth.models import User
from .utils import sendTransaction
import hashlib
from .search import research



class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, null=True)
    content = models.TextField()
    hash = models.CharField(max_length=32, default=None, null=True)
    txId = models.CharField(max_length=66, default=None, null=True)
    unicode = models.CharField(max_length=36, default=None, null=True)

    def writeOnChain(self):
        self.hash = hashlib.sha256(self.content.encode('utf-8')).hexdigest()
        self.txId = sendTransaction(self.hash)
        self.unicode = research()
        self.save()

    def __str__(self):
        return f"{self.user} | {self.title}"


# Create your models here.
