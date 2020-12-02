import sys, getopt
import os
import configparser
import re
import shutil
import subprocess
import sys
import csv


def error_y_sal(mensaje,informa=False):
	if informa:
		print("\r\n\r\n",
			"----------------------------------------------------------------------|\r\n",
			"Script realizado por Emilio Rodríguez con fines didáticos             |\r\n",
			"para la asignatura L10N del Grado de Traducción e Interpretación      |\r\n",
			"de la USAL                                                            |\r\n",
			"Usa/necesita el programa pak_mingw64.exe                              |\r\n",
			"----------------------------------------------------------------------|\r\n")
	print(mensaje)
	sys.exit(2)

def main(argv):
	inputfile = ""
	exepak=""
	configfile=""
	try:
		opts, args = getopt.getopt(argv,"c:i:e:",["ifile=","exepak="])
	except getopt.GetoptError:
		error_y_sal("Uso: csv2pak.py -i <fileTarget.csv> -c <name@csv2pak.ini> [-e <path to pak_mingw64.exe>]",True)
	if len(opts) == 0 or len(opts) > 3:
		error_y_sal("\rUso:csv2pak.py -i <fileTarget.csv> -c <name@csv2pak.ini> [-e <path to"+
	"pak_mingw64.exe>]",True)
	#captura argumentos
	for opt, arg in opts:
		if opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-e", "--exepak"):
			exepak=arg
		elif opt in ("-c", "--config"):
			configfile=arg
	if inputfile=='':
		error_y_sal("csv2pak.py -i <fileTarget.csv> -c <name@csv2pak.ini> [-e <path to pak_mingw64.exe>]"+
			"\n\r¡El argumento -i <fileTarget.csv> es necesario!")
	if configfile=='':
		error_y_sal("csv2pak.py -i <fileTarget.csv> -c <name@csv2pak.ini> [-e <path to pak_mingw64.exe>]"+
			"\n¡El argumento -c <name@csv2pak.ini> es necesario!")
	if os.path.exists(inputfile):
		if os.path.isdir(inputfile):
			error_y_sal("El argumento tras -i debía de ser un fichero, no un directorio: "+inputfile)
		elif os.path.isfile(inputfile):
			inputfile=os.path.abspath(inputfile)
	else:
		error_y_sal("¡Fichero "+inputfile+ " no encontrado!")
	if os.path.exists(configfile):
		if os.path.isdir(configfile):
			error_y_sal("El argumento tras -c debía de ser un fichero, no un directorio: "+configfile)
		elif os.path.isfile(configfile):
			configfile=os.path.abspath(configfile)
	else:
		error_y_sal("¡Fichero "+configfile+" no encontrado!")
	#está el fichero -e pak_ming64.exe???
	if exepak=='':
		exepak='.'
	if os.path.exists(exepak):
		if os.path.isdir(exepak):
			if not os.path.exists(exepak+"/"+"pak_mingw64.exe"):
				error_y_sal("¡Fichero 'pak_mingw64.exe' no encontrado!")
			else:
				exepak=exepak+"/"+"pak_mingw64.exe"
		elif os.path.isfile(exepak):
			if(os.path.basename(exepak) not in ["pak_mingw64","pak_mingw64.exe"]):
				error_y_sal("Se esperaba el nombre del programa pak_mingw64 en el argumento -e!!! \n\rEl nombre escrito"+" ha sido "+ os.path.basename(exepak))
	else:
		error_y_sal("¡Ruta indicada tras el argumento -e "+exepak+ " no encontrada!")
	rutaming,nameming=os.path.split(os.path.abspath(exepak))
	carpetanewpak=csv2pak(configfile, inputfile)
	pathCSV=os.path.dirname(inputfile)
	name,_=os.path.splitext(os.path.basename(inputfile))
	#El nuevo fichero .pak será el nombre del CSV sin la extensión. En la misma carpeta.
	empaqueta(rutaming+"/"+nameming,carpetanewpak,pathCSV+"/"+name+".pak")

class MiCSV(csv.Dialect):
	delimiter = ","
	quoting = csv.QUOTE_MINIMAL
	quotechar = '"'
	lineterminator = "\n"
	escapechar='\\'


def csv2pak(fileconfig, filecsv):
	#abre el fichero de configuración ".ini" para la conversión
	#de vuelta.
	config=configparser.ConfigParser(interpolation=None)
	if not os.path.exists(fileconfig):
		error_y_sal("No se encuentra el fichero "+fileconfig+"\n",
			"El proceso NO ha finalizado con éxito")
	try:
		config.read(fileconfig)
	except:
		error_y_sal("Error al abrir el fichero de configuración: "+ fileconfig+
			"\n\rNo ha podido realizarse la creación del fichero"+ "'.pak' para obtener la versión traducida")
	secciones=config.sections()
	#print(secciones)
	if "l10nFTD@csv2pak" not in secciones:
		error_y_sal("Sección [l10nFTD@csv2pak] no encontrada en fichero "+fileconfig+
			"\n\rNo ha podido realizarse la creación del fichero .pak para obtener la traducción en destino")
	configuracion=config[secciones[0]]
	if "pathNewPak" not in configuracion:
		error_y_sal("No encontrada la variable 'pathNewPak' en el fichero de configuración "+fileconfig+
			"\n\rNo ha podido realizarse la creación del fichero", ".pak para obtener la traducción en destino")
	else:
		pathnewpak=configuracion['pathNewPak']
	#abrimos el fichero CSV
	mi_csv=MiCSV()
	if not os.path.isdir(pathnewpak):
		error_y_sal("No encontrada la carpeta "+ pathnewpak+ " referenciada en el fichero de configuracion "+ fileconfig+"\n\r¡El proceso no ha podido completarse!")
	try:
		# Pasamos del CSV traducido a ficheros en pathnewpak
		with open(filecsv, newline="", encoding='utf-8') as csvfile:
			reader = csv.reader(csvfile, mi_csv)
			for row in reader:
				try:
					f=open(pathnewpak+'/'+row[0],'w',encoding='utf-8')
					f.write(row[1])
					f.close()
				except:
					error_y_sal("Error al escribir el fichero "+pathnewpak+"/"+row[0]+
		"\n\r¡El proceso no ha podido completarse!")
	except:
		error_y_sal("Error al abrir el fichero "+filecsv+"\n\r¡El proceso no ha podido completarse!")

	return pathnewpak


def empaqueta(mingw,carpetapak,newpak):
	index_ini=os.path.abspath(carpetapak+"/pak_index.ini")
	newpak=os.path.abspath(newpak)
	#print("comando: ",mingw," -p ",index_ini," ",newpak)
	try:
		subprocess.run([mingw,"-p",index_ini,newpak],check=True)
		print("¡Fichero "+ newpak+ " generado!\n",
			"\r¡Proceso finalizado con éxito!")
	except:
		error_y_sal("!Error en el proceso de creación del fichero .pak en destino!")



if __name__ == "__main__":
	main(sys.argv[1:])
