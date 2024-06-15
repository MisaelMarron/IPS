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
        return f"{self.NomObra}"
    
    #protocolo de insersion
    def clean(self):
        errors = {}
        # validar el nombre obra
        if not self.NomObra:
            errors['NomObra'] = ValidationError("Se debe colocar Nombre de obra")
        # validar el nombre contratista
        if not self.NomCon:
            errors['NomCon'] = ValidationError("Se debe colocar Nombre de contratista")
        # validar horas minimas
        if self.HorMin is None:
            errors['HorMin'] = ValidationError("Se debe colocar Horas mínimas")
        elif self.HorMin < 0:
            errors['HorMin'] = ValidationError("El valor de Horas mínimas debe ser positivo")
        # mandar error
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
# modelo unidad
class UNIDAD(models.Model):
    CodUni = models.CharField(max_length=60, primary_key=True)
    NomUni = models.CharField(max_length=60)
    ModUni = models.CharField(max_length=60)
    PreHor = models.DecimalField(max_digits=10, decimal_places=2)
    HorUni = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.NomUni}"
    
    #protocolo de insersion
    def clean(self):
        errors = {}
        # validar el nombre de unidad
        if not self.NomUni:
            errors['NomUni'] = ValidationError("Se debe colocar Nombre de unidad")
        # validar el modelo de unidad
        if not self.ModUni:
            errors['ModUni'] = ValidationError("Se debe colocar Modelo de unidad")
        # validar el precio hora
        if self.PreHor is None:
            errors['PreHor'] = ValidationError("Se debe colocar Precio hora")
        elif self.PreHor < 0:
            errors['PreHor'] = ValidationError("El valor de Precio hora debe ser positivo")
        # validar el horometro inicial
        if self.HorUni is None:
            errors['HorUni'] = ValidationError("Se debe colocar Horometro unidad")
        elif self.HorUni < 0:
            errors['HorUni'] = ValidationError("El valor de Horometro unidad debe ser positivo")
        # mandar error
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
# modelo labor conectado con Unidad y Usuario
class LABOR(models.Model):
    CodLab = models.AutoField(primary_key=True)
    CodUsu = models.ForeignKey(User, on_delete=models.CASCADE, db_column='CodUsu') 
    CodUni = models.ForeignKey(UNIDAD, on_delete=models.CASCADE, db_column='CodUni')
    LabDes = models.CharField(max_length=60)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['CodUsu', 'CodUni'], name='unique_codusu_coduni')
        ]
    
    def __str__(self):
        return f"{self.CodUsu.username} - {self.CodUni.NomUni}"

#modelo trabajo
class TRABAJO(models.Model):
    CodTra = models.AutoField(primary_key=True)
    CodLab = models.ForeignKey(LABOR, on_delete=models.CASCADE, db_column='CodLab')
    CodObra = models.ForeignKey(OBRA, on_delete=models.CASCADE, db_column='CodObra')
    FecIni = models.DateField()
    FecFin = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['CodLab', 'CodObra'], name='unique_CodLab_CodObra')
        ]

    def __str__(self):
        return f"{self.CodLab.CodUsu.username} - {self.CodObra.NomObra}"

    #protocolo de insersion
    def clean(self):
        errors = {}
        # validar el fecha inicial
        if self.FecIni is None:
            errors['FecIni'] = ValidationError("Se debe colocar Fecha de inicial")
        # validar el fecha final
        elif self.FecFin is None:
            errors['FecFin'] = ValidationError("Se debe colocar Fecha final")
        # contrato minimo de 90 dias y diferencia de fechas
        elif (self.FecFin - self.FecIni).days <= 90:
            errors['FecFin'] = ValidationError("El contrato debe tener 90 dias minimos")
        # mandar error
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

# modelo registro 
class REGISTRO(models.Model):
    CodReg = models.AutoField(primary_key=True)
    CodTra = models.ForeignKey(TRABAJO, on_delete=models.CASCADE, db_column='CodTra')
    FecTra = models.DateField()
    Turno = models.CharField(max_length=5,)
    EstMaq = models.CharField(max_length=10)
    HorIni = models.DecimalField(max_digits=10, decimal_places=2,) 
    HorFin = models.DecimalField(max_digits=10, decimal_places=2)
    fecCre = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['FecTra', 'CodTra'], name='unique_FecTra_CodTra')
        ]
    
    def __str__(self):
        return f"{self.CodTra.CodLab.CodUsu.username} - {self.FecTra}"
    
    #protocolo de insersion
    def clean(self):
        errors = {}
        # validar el Horometro inicial
        if self.HorIni is None:
            errors['HorIni'] = ValidationError("Se debe colocar Horometro inicial")
        elif self.HorIni < 0:
            errors['HorIni'] = ValidationError("El valor de Horometro inicial debe ser positivo")
        # validar el Horometro final
        if self.HorFin is None:
            errors['HorFin'] = ValidationError("Se debe colocar Horometro final")
        elif self.HorFin < 0:
            errors['HorFin'] = ValidationError("El valor de Horometro final debe ser positivo")
        # Diferencia Horometro 
        if self.HorIni is not None and self.HorFin is not None:
            if self.HorFin <= self.HorIni:
                errors['HorFin'] = ValidationError("Horometro final debe ser mayor a horometro inicial") 
        # Validar Codigo trabajo
        if self.CodTra_id is None: #raro aun se usa el id (tomar en cuenta)
            errors['CodTra'] = ValidationError("Debe colocar Codigo de trabajo")
        else:
            try:
                self.CodTra.refresh_from_db()
                # validacion de horas 
                # Validar Fecha de trabajo 
                if self.FecTra is None:
                    errors['FecTra'] = ValidationError("Se debe colocar Fecha de trabajo")
                else:
                    ran_inf = (self.FecTra - self.CodTra.FecIni).days
                    ran_sup = (self.CodTra.FecFin - self.FecTra).days
                    if ran_inf < 0 or ran_sup < 0:
                        errors['FecTra'] = ValidationError("Fecha de trabajo  no está dentro del rango del trabajo asociado")

            except TRABAJO.DoesNotExist:
                errors['CodTra'] = ValidationError("El trabajo asociado no existe en la base de datos")
            
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
