# Operadores Puntuales 
## Filtro Negativo 

## Función de Potencia Gamma
Para modificar el contraste de una imagen 
Entre mas chico es gamma, más blanca es la img
A medida que lo aumentamos se va haciendo más negra. En el histograma se ve que las barras quedan más del lado del 0

## Umbralización
Para pasarla a binaria. Es dificil elegir el umbral 
Conviene ecualizar

## Ecualización
 

# Noise 
## Rayleigh 
```json
"Epsilon" >= 0.4
```
- Empieza a oscurecer la imagen porque el intervalo para normalizar da mayor a 255 
Si el epsilon es menor no normaliza  
```json
"Epsilon" = 0.2
"ruido" = 10%
```
- Con la mediana lo saque todo pero no queda tan definida
- Con la mediana ponderada lo saque casi todo 
- Gauss no pudo
- Media no pudo

## Gauss 

## Exponencial 

## Salt & Pepper 

# Dominio Espacial 

Para eliminar ruido o suavizar la img (borronear)

## Máscara de la Media 
```json
"noise_perc": 0.1
"mask_size" 
```
- Saca el Salt & Pepper
- Puede crear nuevas intensidades de grises que no
aparecían en la imagen.

## Máscara de la Mediana 
Saca un poco de Salt & Pepper pero no tanto como la Media
Preserva borders

## Máscara de la Mediana Ponderada 
En qué es buena? 
Saca un poco de Salt & Pepper pero no tanto como la Media

## Máscara de Gauss 
 
 
## Máscara Pasaaltos/Bordes
- Realce de Bordes

