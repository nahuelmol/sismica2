## con segyio
Pueden visualizarse imagenes 2D (lines)
* iline y xline no estan disponibles (None) (solo aparecen en las representaciones volumetricas 3D)
* pueden graficar una linea usando xr, transponiedo el array e invirtiendo lo yaxis

## con segysak
Pueden visualizarse archivos 3D por secciones

## un archivo estructurado en 3D
* puedo obtener una seccón de la imagen sismica..
![data](./imagen.png) 

* se elige un inline y un xline especificos
* se convierte con xr
* se grafica como una sección 2D

## Los filtros
Se aplican simplemente:
* extrayendo las trazas
* filtrando cada una
* reorganizando la martriz para formar la imagen sismica post filtrado

## objetivos
* realizar la correción NMO y DMO
* aplicar filtro f-k

##recursos
https://data.openei.org/submissions/3794
