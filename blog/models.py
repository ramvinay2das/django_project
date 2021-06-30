from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Posts(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
        
    #instead of this function you can write in view a attribute of postCreateView , "success_url" and set it to what ever specific url you want
    def get_absolute_url(self):
        # reverse will redirect the link to view and view will take care of redirect(class based view we are talking about)
        return reverse('post-detail' , kwargs={'pk':self.pk})