from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import pre_save
from django.conf import settings
from django.utils.text import slugify

class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(published_date__lte=timezone.now())

def upload_location(instance, filename):
    #filebase, extension = filename.split(".")
    #return "%s/%s.%s" %(instance.id, instance.id, extension)
    return "%s/%s" %(instance.id, filename)

class Post(models.Model):
    #author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True, height_field="height", width_field="width")
    height = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    text = models.TextField()
    draft = models.BooleanField(default=False)
    #publish = models.DateTimeField(default=timezone.now())
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    objects = PostManager()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self): #same as __unicode__; prints 'unicode' as title
        return self.title

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return (reverse("Blogger:detail", kwargs={"slug" : self.slug}))
        #return "/Blogger/%s/"%(self.id)

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_Post_Receiver(instance, sender, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance) 

pre_save.connect(pre_save_Post_Receiver, sender=Post)










