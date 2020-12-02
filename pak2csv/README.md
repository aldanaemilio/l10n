# Localización de archivos PAK ".pak" 
## Práctica de Localización en el Grado de Traducción e Interpretación de la USAL

El formato PAK (".pak") es utilizado por algunas aplicaciones para contener el texto, en las diferentes lenguas a las que está traducido, de la interfaz del usuario. Por ejemplo, es el caso, en la actualidad, del navegador Chrome.

En GitHub el proyecto [chrome-pak-customizer](https://github.com/myfreeer/chrome-pak-customizer/releases) ofrece el programa pak_mingw64.exe (o pak_ming32.exe) que permite el desempaquetado y empaquetado de los archivos ".pak".

El resultado del desempaquetado de un fichero PAK es un conjunto considerable de ficheros. En realidad, tantos como mensajes de texto contenga la aplicación. Por ejemplo, en la versión que tengo actualmente instalada de Chrome (2/12/2020), el desempaquetado de la versión inglesa de USA ("en-US.pak"), genera 4946 ficheros que, como hemos indicado, cada uno contiene un mensaje concreto de la interfaz de usuario de Chrome.

Valiéndonos de este programa de empaquetado/desempaquetado de ficgheros PAK (pak_mingw64.exe) hemos creado dos pequeños scripts, con fines únicamente docentes, con el objetivo de aumentar el abanico de prácticas a realizar con nuestros ***estudiantes del Grado de Traducción e Interpretación de la USAL***:
1. ***pak2csv.py*** (que también ofrecemos en versión ejecutable de 64 bits para Windows, ***pak2csv.exe***) que reúne todos los archivos desempaquetados por pak_mingw64.exe en un solo fichero CSV (".csv"), que, por tanto, contendrá todos los mensajes de la aplicación.

2. ***csv2pak.py*** (y la versión ejecutable para Windows de 64 bits ***csv2pak.exe***) que recoje el fichero CSV  y genera el fichero PAK. 

En el proceso de *Localización* de una aplicación cuyos mensajes se distribuyan en formato PAK, se tratará, lógicamente, de enviar el CSV generado con **pak2csv.exe** a una herramienta de TAO para, tras la traducción a una nueva lengua, convertir el nuevo CSV en un nuevo fichero PAK, con la versión en destino usando, esta vez, **csv2pak.exe**

Se distribuye en este proyecto también el archivo **okf_table@csv2pak.fprm**, un filtro CSV para [Rainbow -Okapi Applications-](https://bintray.com/okapi/Distribution) adaptado para el CSV generado con nuestro script. Este filtro captura como etiquetas internas las diferentes partes del texto que no debe de traducirse de los diferentes mensajes de la aplicación.



