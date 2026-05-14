from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название категории")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL-адрес категории")
    spaces = models.ForeignKey('space.Space', on_delete=models.CASCADE, related_name='categories', verbose_name="Аптеки", blank=True, null=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name
    

class Manufacturer(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название производителя")
    description = models.TextField(blank=True, null=True, verbose_name="Описание производителя")
    country = models.CharField(max_length=255, blank=True, null=True, verbose_name="Страна производителя")
    spaces = models.ForeignKey('space.Space', on_delete=models.CASCADE, related_name='manufacturers', verbose_name="Аптеки", blank=True, null=True)


    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"

    def __str__(self):
        return self.name

class Recepts(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название лекарства")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='recepts', verbose_name="Категория", blank=True, null=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='recepts', verbose_name="Производитель", blank=True, null=True)
    image = models.ImageField(upload_to='medicines/', blank=True, null=True, verbose_name="Фото")
    is_prescription_required = models.BooleanField(default=False, verbose_name="По рецепту")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Справочник лекарств"
        verbose_name_plural = "Справочник лекарств"

    def __str__(self):
        return self.name

class Barcode(models.Model):
    recept = models.ForeignKey(Recepts, on_delete=models.CASCADE, related_name='barcodes', verbose_name="Лекарство")
    code = models.CharField(max_length=255, unique=True, verbose_name="Штрихкод")
    volume = models.CharField(max_length=255, blank=True, null=True, verbose_name="Объем")
    UNIT_CHOICES = (
        ('MG', 'мг'),
        ('ML', 'мл'),
    )
    unitmeas = models.CharField(verbose_name='единица измерения', max_length=10, choices=UNIT_CHOICES, blank=True, null=True)


    class Meta:
        verbose_name = "Штрихкoд"
        verbose_name_plural = "Штрихкоды"

    def __str__(self):
        return f"{self.code} для {self.recept.name}"