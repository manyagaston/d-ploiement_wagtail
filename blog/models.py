from django import forms
from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel,MultiFieldPanel
from modelcluster.fields import ParentalManyToManyField
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from wagtail.snippets.models import register_snippet
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class BlogIndexPage(Page):
    intro = models.CharField(max_length=255, blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('image'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context


class BlogPage(Page):
    parent_page_types = ['blog.BlogIndexPage']
    subpage_types = []

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField()
    body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], use_json_field=True)
    categories = ParentalManyToManyField("blog.BlogCategory", blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",)

    content_panels = Page.content_panels + [
        FieldPanel('body',heading="Corps de l'article"),
        FieldPanel('image',heading="Image de l'article"),
        FieldPanel('date',heading="Date du publication"),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple, heading="Choisir une catgorie")
            ],
            heading="Catégories"
        ),
        FieldPanel('author',heading="Auteur de l'article"),
    ]

    def __str__(self):
        return self.title

    
    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'


@register_snippet
class BlogCategory(models.Model):

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text='A slug to identify posts by this category',
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name