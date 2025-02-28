from django.db import models
from datetime import datetime
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField


# Create your models here.

class Categories(models.TextChoices):
    WORLD = 'world'   
    Technology = 'technology'
    TRAVEL = 'travel'
    
        
class Post(models.Model):
    title = models.CharField(max_length=50)
    slug  = models.SlugField()
    category = models.CharField(max_length=50, choices=Categories.choices, default=Categories.WORLD)
    thumbnail = models.ImageField(upload_to='photos/%Y/%m/%d/')
    excerpt = models.CharField(max_length=150)
    month = models.CharField(max_length=3)
    day = models.CharField(max_length=2)
    contents =  RichTextField()
    featured = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=datetime.now, blank=True)

   
    def save(self, *args, **kwargs):
        original_slug = slugify(self.title)
        queryset = Post.objects.all().filter(slug__iexact=original_slug).count()

        count = 1
        slug = original_slug
        while(queryset):
            slug = original_slug + '-' + str(count)
            count += 1
            queryset = Post.objects.all().filter(slug__iexact=slug).count()

        self.slug = slug

        if self.featured:
            try:
                temp = Post.objects.get(featured=True)
                if self != temp:
                    temp.featured = False
                    temp.save()
            except Post.DoesNotExist:
                pass
        
        super(Post, self).save(*args, **kwargs)


       
    def __str__(self):
        return self.title