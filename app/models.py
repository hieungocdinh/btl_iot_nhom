from django.db import models

class TrashCan(models.Model):
    position = models.CharField(max_length=255)

class TrashCompartment(models.Model):
    id_trash_can = models.ForeignKey(TrashCan, on_delete=models.CASCADE)
    empty_count = models.IntegerField(default=0)
    label = models.CharField(max_length=255)
    max_quantity = models.IntegerField(default=20)

    class Meta:
        unique_together = ('id_trash_can', 'label')

class Trash(models.Model):
    id_trash_can = models.ForeignKey(TrashCan, on_delete=models.CASCADE)
    id_trash_compartment = models.ForeignKey(TrashCompartment, on_delete=models.CASCADE)
    trash_img_url = models.URLField()  
    trash_img_public_id = models.CharField(max_length=255)  
    date = models.DateTimeField()
    quantity = models.IntegerField()  
