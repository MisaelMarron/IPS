from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# modelo obra
class OBRA(models.Model):
    CodObra = models.AutoField(primary_key=True)
    NomObra = models.CharField(max_length=60)
    NomCon = models.CharField(max_length=60)
    HorMin = models.IntegerField(null=False)

    def __str__(self):
        return f"nombre: {self.NomObra}"
    
    #protocolo de insersion
    def clean(self):
        if self.HorMin < 0:
            raise ValidationError("El valor de Horas solo puede ser positivo")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
# modelo unidad
class UNIDAD(models.Model):
    CodUni = models.AutoField(primary_key=True)
    NomUni = models.CharField(max_length=60)
    ModUni = models.CharField(max_length=60)
    PreHor = models.DecimalField(max_digits=10, decimal_places=2)
    HorUni = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"nombre: {self.NomUni}"
    
    #protocolo de insersion
    def clean(self):
        if self.PreHor < 0:
            raise ValidationError("El valor de Precio hora solo puede ser positivo")
        if self.HorUni < 0:
            raise ValidationError("El valor de Horometro solo puede ser positivo")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
# modelo labor conectado con Unidad y Usuario
class LABOR(models.Model):
    CodLab = models.AutoField(primary_key=True)
    CodUsu = models.ForeignKey(User, on_delete=models.CASCADE) 
    CodUni = models.ForeignKey(UNIDAD, on_delete=models.CASCADE)
    LabDes = models.CharField(max_length=60)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['CodUsu', 'CodUni'], name='unique_codusu_coduni')
        ]
    
    def __str__(self):
        return f"nombre usuario: {self.CodUsu.username},nombre unidad {self.CodUni.NomUni}"

#modelo trabajo
class TRABAJO(models.Model):
    CodTra = models.AutoField(primary_key=True)
    CodLab = models.ForeignKey(LABOR, on_delete=models.CASCADE)
    CodObra = models.ForeignKey(OBRA, on_delete=models.CASCADE)
    FecIni = models.DateField()
    FecFin = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['CodLab', 'CodObra'], name='unique_CodLab_CodObra')
        ]

    def __str__(self):
        return f"nombre usuario: {self.CodLab.CodUsu.username},nombre obra {self.CodObra.NomObra}"

# modelo registro 
class REGISTRO(models.Model):
    CodReg = models.AutoField(primary_key=True)
    CodTra = models.ForeignKey(TRABAJO, on_delete=models.CASCADE)
    FecTra = models.DateField()
    Turno = models.CharField(max_length=5,)
    EstMaq = models.CharField(max_length=10)
    HorIni = models.DecimalField(max_digits=10, decimal_places=2,) 
    HorFin = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['FecTra', 'CodTra'], name='unique_FecTra_CodTra')
        ]
    
    def __str__(self):
        return f"nombre usuario: {self.CodTra.CodLab.CodUsu.username}, fecha {self.FecTra}"
    
    #protocolo de insersion
    def clean(self):
        if self.HorIni < 0 or self.HorFin < 0:
            raise ValidationError("El valor de Horas solo puede ser positivo")
        if self.HorIni > self.HorFin:
            raise ValidationError('Horometro final debe ser mayor a horometro inicial')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
