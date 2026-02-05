from django.db import models

class Metodologia(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        managed = False  # Esto le dice a Django: "No toques la tabla, ya existe en SQL"
        db_table = 'metodologia'
    
    def __str__(self):
        return self.nombre

class Fase(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    # Django detecta que 'metodologia_id' en SQL es la llave foránea a 'Metodologia'
    metodologia = models.ForeignKey(Metodologia, on_delete=models.CASCADE, db_column='metodologia_id')

    class Meta:
        managed = False
        db_table = 'fase'

class Tarea(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=100, blank=True, null=True)
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE, db_column='fase_id')

    class Meta:
        managed = False
        db_table = 'tarea'
