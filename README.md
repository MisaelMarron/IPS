# Proyecto para IPS
## Estructura basica 
- paginaPrincipal --> Principal
- sistemaLogeo --> app donde se ubicara la base de datos

## Comandos de git 
- git branch --> ver rama actual
- git add . --> preparacion para el commit
- git commit -m "mensaje de cambio" --> cambios
- git push --> mandar cambios

## Base de datos 
### OBRA
- CodObra => Codigo de Obra         = Entero (Primary Key)
- NomObra => Nombre de la Obra      = Char (60)
- NomCon => Nombre del contratista  = Char (60)
- HorMin => Horas minimas           = Entero

### UNIDAD
- CodUni => Codigo de Unidad    = Entero (Primary Key)
- NomUni => Nombre de Unidad    = Char (60)
- ModUni => Modelo de Unidad    = Char (60)
- PreHor => Precio hora         = Decimales (2)
- HorUni => Horometro Unidad    = Decimales (2)

### LABOR
- CodLab => Codigo de labor         = Entero (Primary Key)
- CodUsu => Codigo de Usuario       = Entero (Unicidad 1) = USUARIO
- CodUni => Codigo de Unidad        = Entero (Unicidad 1) = UNIDAD
- LabDes => Descripcion de labor    = Char (60)

### TRABAJO
- CodTra => Codigo de labor     = Entero (Primary Key)
- CodLab => Codigo de labor     = Entero (Unicidad 1)
- CodObra => Codigo de Obra     = Entero (Unicidad 1)
- FecIni => Fecha inicio        = Date
- FecFin => Fecha final         = Date

### REGISTRO
- CodReg => Codigo de labor     = Entero (Primary Key)
- CodTra => Codigo de trabajo   = Entero (Unicidad 1)
- FecTra => Fecha de trabajo    = Date (Unicidad 1)
- Turno => Turno                = Char (5) = DIA / TARDE / NOCHE
- EstMaq => Estado maquina      = Char (10) = OPERATIVO / MALOGRADO 
- HorIni => Horometro inicial   = Decimales (2)
- HorFin => Horometro final     = Decimales (2)
- fecCre => Fecha de creacion   = Date

## Credenciales
- user: root, password: root1234