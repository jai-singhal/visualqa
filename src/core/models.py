from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _


class VQAImage(models.Model):
    image = models.ImageField(_("Upload your image"), upload_to="images/", height_field=None, width_field=None, max_length=None)
    timestamp = models.DateTimeField(_(""), auto_now=False, auto_now_add=True)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE)


class Question(models.Model):
    question = models.CharField(_("Input your question"), max_length=100)
    answer = models.CharField(_("Answer of the question"), max_length=50)

    timestamp = models.DateTimeField(_(""), auto_now=False, auto_now_add=True)
    image = models.ForeignKey(VQAImage, verbose_name=_("image"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("question")
        verbose_name_plural = _("questions")

    def __str__(self):
        return self.question

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
