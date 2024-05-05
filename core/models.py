from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Staff(models.Model):
    fullname = models.CharField(max_length=255, verbose_name='Ady')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Url', blank=True, null=True)
    profession = models.CharField(max_length=255, verbose_name='Wezipesi', null=True, blank=True)
    mail = models.EmailField(verbose_name="Pocta", null=True, blank=True)
    phone_number = models.CharField(max_length=100, verbose_name='Nomer telefon',blank=True, null=True)

    def __str__(self):
        return str(self.fullname)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fullname)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('staff', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Isgarler'
        verbose_name_plural = 'Isgarler'
        ordering = ['-id']


class GetIn(models.Model):
    person_id = models.ForeignKey(Staff, on_delete=models.PROTECT, verbose_name='Isgar',related_name='get_in')
    get_in_date = models.DateField(auto_now_add=True, verbose_name='Giren senesi')
    get_in_time = models.TimeField(auto_now_add=True, verbose_name='Giren wagty')
    in_work = models.BooleanField(default=False)


    def __str__(self):
        return str(self.person_id)

    class Meta:
        verbose_name = 'Giris wagty'
        verbose_name_plural = 'Giren wagtlary'
        ordering = ['-get_in_date']