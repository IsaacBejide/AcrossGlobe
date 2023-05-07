from datetime import datetime
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin, HitCount
from ckeditor_uploader.fields import RichTextUploadingField  # import this
from django.utils.translation import gettext_lazy as _
from django.conf.locale.en import formats as en_formats


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
#     image = models.ImageField(upload_to="profile_pics", blank=True, null=True)
#     bio = models.TextField(_('bio'), blank=True, null=True)
#     phone_no = models.IntegerField(_('phone_no'), blank=True, null=True)
#     facebook = models.CharField(_('facebook'), max_length=300, blank=True, null=True)
#     instagram = models.CharField(_('instagram'), max_length=300, blank=True, null=True)
#     linkedin = models.CharField(_('linkedin'), max_length=300, blank=True, null=True)

#     def __str__(self):
#         return str(self.user)


class TypeCategories(models.Model):
    type = models.CharField(_('type'), max_length=100, blank=True, null=True)

    def __str__(self):
        return self.type


class BlogPostCategories(models.Model):
    objects = None
    type = models.ForeignKey(TypeCategories, default=1, on_delete=models.CASCADE)
    category_title = models.CharField(_('category_title'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=130, blank=True)

    def __str__(self):
        return str(self.category_title) + " Category Title: " + self.category_title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_title)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    title = models.CharField(_('title'), max_length=255)
    category = models.ForeignKey(BlogPostCategories, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(_('slug'), max_length=130, blank=True)
    content = RichTextUploadingField(null=True, blank=True, config_name="default", external_plugin_resources=[
        ('youtube', '/static/shareledge/ckeditor-plugins/youtube/youtube/', 'plugin.js',)])  # models.TextField()
    # content=RichTextUploadingField(_('content'), null=True, blank=True) # add this
    image = models.ImageField(upload_to="profile_pics/%Y/%m/%d/", blank=True, null=True)
    dateTime = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    #likes = models.IntegerField(default=0)
    #dislikes = models.IntegerField(default=0)

    viewers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='viewed_posts', editable=False)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='posts_liked', blank=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    

    def __str__(self):
        return str(self.author) + " Blog Title: " + self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + "-" + str(datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f")))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('MyBlog:blogs_comment', kwargs={'slug': self.slug})

    def number_of_likes(self):
        return self.viewers.count()

    def get_id(self):
        return self.id


class FileUploads(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    file = models.FileField(upload_to="profile_pics/%Y/%m/%d/", blank=True, null=True)
    # uploaded_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    content = RichTextField(_('content'))
    # content = models.TextField()
    # parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    dateTime = models.DateTimeField(default=now)

    def __str__(self):
        return self.user.username + " Comment: " + str(self.content)

    # uploaded_at = models.DateTimeField(auto_now_add=True)
    # @property
    # def children(self):
    #     return Comment.objects.filter(parent_comment=self).reverse()

    # @property
    # def is_parent(self):
    #     if self.parent_comment is None:
    #         return True
    #     return False  


class CommentFileUploads(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    file = models.FileField(upload_to="profile_pics/%Y/%m/%d/", blank=True, null=True)


class ReplyComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    replier_name = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_content = RichTextField(_('reply_content'), )
    replied_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "'{}' replied with '{}' to '{}'".format(self.replier_name, self.reply_content, self.reply_comment)


####################### User follow system ###########################

# class Contact(models.Model):
#     user_from = models.ForeignKey('auth.User', related_name='rel_from_set', on_delete=models.CASCADE)
#     user_to = models.ForeignKey('auth.User', related_name='rel_to_set', on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True, db_index=True)

#     class Meta:
#         ordering = ('-created',)

#     def __str__(self):
#         return f'{self.user_from} follows {self.user_to}'


# # Add following field to User dynamically
# user_model = get_user_model()
# user_model.add_to_class('following', models.ManyToManyField('self', through=Contact, related_name='followers', symmetrical=False))

######################################################################


####################### Advertisement Module ###########################

class Advertisement(models.Model):
    category = models.ForeignKey(BlogPostCategories, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="advert_pics/%Y/%m/%d/", blank=True, null=True)
    urllink = models.CharField(_('urllink'), max_length=356)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    advertiser = models.CharField(_('advertiser'), max_length=356)
    expiration_date = models.DateTimeField(auto_now_add=False, db_index=True)


######################################################################

# #from django.contrib.auth import get_user_model

# class Comment(models.Model):
#     CommentPost = models.ForeignKey(Blog , on_delete=models.CASCADE)
#     author = models.ForeignKey(get_user_model() , on_delete=models.CASCADE)
#     content = models.TextField()
#     date_posted = models.DateTimeField(auto_now_add=True)
#     parent = models.ForeignKey('self' , null=True , blank=True , on_delete=models.CASCADE , related_name='replies')

#     class Meta:
#         ordering=['-date_posted']

#     def __str__(self):
#         return str(self.author) + ' comment ' + str(self.content)

#     @property
#     def children(self):
#         return Comment.objects.filter(parent=self).reverse()

#     @property
#     def is_parent(self):
#         if self.parent is None:
#             return True
#         return False    



# === Codes to migrate models into database === #
# python manage.py makemigrations
# python manage.py migrate
