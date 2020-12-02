import sys, getopt
import os
import configparser
import re
import shutil
import subprocess
import sys

def error_y_sal(mensaje,informa=False):
	if informa:
		print("\n\n","\rScript realizado por Emilio Rodríguez con fines didáticos\n"
			"\rpara la asignatura L10N del Grado de Traducción e Interpretación\n",
			"\rde la USAL\n\n",
			"\rUsa/necesita el programa pak_mingw64.exe\n\n\r")
	print(mensaje)
	sys.exit(2)

def main(argv):
	inputfile = ""
	exepak=""
	newpak="/newPak@@"
	try:
		opts, args = getopt.getopt(argv,"i:e:",["ifile=","exepak="])
	except getopt.GetoptError:
		error_y_sal("Uso: pak2csv -i <file.pak> [-e <path to pak_mingw64.exe>]",True)
	if len(opts) == 0 or len(opts) > 2:
		error_y_sal("Uso: pak2csv -i <file.pak> [-e <path to pak_mingw64.exe>]",True)
	#captura argumentos
	for opt, arg in opts:
		if opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-e", "--exepak"):
				exepak=arg
	if inputfile=='':
		error_y_sal("Uso: pak2csv -i <file.pak> [-e <path to pak_mingw64.exe>]\n"+
			"\r¡El argumento -i <file.pak> es necesario!",False)
	if exepak == '':
		exepak ='.'
	#existe fichero -i <file.pak>
	if os.path.exists(inputfile):
		if os.path.isdir(inputfile):
			error_y_sal("El argumento tras -i debía de ser un fichero, no un directorio: "+inputfile,False)
		elif os.path.isfile(inputfile):
			rutapak,namepak=os.path.split(os.path.abspath(inputfile))
			nameNotExt,_=os.path.splitext(namepak)
	else:
		error_y_sal("¡Fichero "+inputfile+ " no encontrado!")
	#está el fichero -e pak_ming64.exe???
	
	if os.path.exists(exepak):
		if os.path.isdir(exepak):
			if not os.path.exists(exepak+"/"+"pak_mingw64.exe"):
				error_y_sal("File 'pak_mingw64.exe' not found")
			else:
				exepak=exepak+"/"+"pak_mingw64.exe"
		elif os.path.isfile(exepak):
			if(os.path.basename(exepak) not in ["pak_mingw64","pak_mingw64.exe"]):
				error_y_sal("Se esperaba el nombre del programa pak_mingw64 en el argumento -e!!! "+
					"El nombre escrito ha sido "+ os.path.basename(exepak))
	else:
		error_y_sal("Ruta indicada tras el argumento -e "+exepak+" no encontrada, !!!")
	rutaming,nameming=os.path.split(os.path.abspath(exepak))
	#print("Input file es: ", namepak, "y su path:", rutapak)
	#print("La ruta al programa ", nameming , "es ",rutaming)
	desempaqueta(rutaming+"/"+nameming,rutapak+"/"+namepak,rutapak+"/unpak_"+nameNotExt)
	pak2csv(rutapak+"/unpak_"+nameNotExt,rutapak,namepak,newpak)
	configuracion_csv2pak(rutapak+"/"+nameNotExt+"@csv2pak.ini",rutapak+"/unpak_"+nameNotExt+newpak,rutapak+"/"+namepak+".csv")

def desempaqueta(mingw,pakfile,carpetaunpak):
	try:
		subprocess.run([mingw,"-u",pakfile,carpetaunpak],check=True)
	except:
		error_y_sal("Error en el proceso de desempaquetado! Falló el programa " + mingw)

def pak2csv(rutaunpak, rutapak,namepak,newpak):
	
	#rutaUnpak: dónde se desempaquetó con pak_mingw64.exe
	#rutaPak: ahí dejamos los archivos .csv e .ini. 
	#newpak: carpeta dónde se alojaran los ficheros para el futuro .pak en el proceso de vuelta.
	#		 Se considera hija de "rutaPak"
	#Carga el parser para fichero INI
	config=configparser.ConfigParser()
	#El fichero pak_index.ini debe de estar presente!!!
	if not os.path.exists(rutaunpak+'/pak_index.ini'):
		error_y_sal("El proceso se ha detenido sin finalizar! No se ha generado el archivo CSV!"+
			" Se esperaba encontrar el archivo pak_index.ini en la carpeta "+rutaunpak)
	config.read(rutaunpak+'/pak_index.ini')
	#carga secciones del fichero INI y centrarse en Resource
	secciones=config.sections()
	numsecc=0
	for secc in secciones:
		if secc=='Resources':
			recursos=config[secciones[numsecc]]
		numsecc=+1
	try:
		os.mkdir(rutaunpak+newpak)
	except FileExistsError:
		pass
	#carga el texto que traducir de todos los ficheros "con texto" 
	#en una lista
	texto_csv=[]
	for r in recursos:
		file=recursos[r]
		f=open(rutaunpak+'/'+file,'r',encoding='utf-8')
		try:
			#reemplaza \n por texto "\n"
			txt=re.sub(r'\n','\\\\n',f.read())
			texto_csv.append('"'+recursos[r]+'","'+ txt +'"')
		#puede haber ficheros binarios...los copiamos a "newPak"
		except UnicodeDecodeError:
			shutil.copy(rutaunpak+"/"+file, rutaunpak+newpak+"/"+file)
		f.close()
	#copia también en la carpeta "newpak" el fichero "pak_index.ini"
	try:
		shutil.copy(rutaunpak+"/"+"pak_index.ini",rutaunpak+newpak+"/pak_index.ini")
	except:
		error_y_sal("El fichero pak_index.ini no ha podido ser copiado"+
			" de la carpeta "+rutaunpak+"\n\rEl proceso no se ha completado")
	#Este fichero
	
	
	#Escribe el fichero CSV
	try:
		f=open(rutapak+"/"+namepak+".csv","w",encoding="utf-8")
	except:
		error_y_sal("Error al crear el fichero CSV: "+rutapak+namepak+
			".csv. El programa no ha podido finalizar correctamente!!!!")
	for l in texto_csv:
		f.write(l+"\n")
	print("\rGenerado fichero: "+rutapak+"/"+namepak+".csv")
	f.close()
	
	
def configuracion_csv2pak(nameIni,rutanewpak,ficheroCSV):
	#Escribe la configuración del proceso para realizar la conversion posterior csv2pak
	try:
		f=open(nameIni,"w",encoding="utf-8")
		f.write("[l10nFTD@csv2pak]\n")
		f.write("pathNewPak="+rutanewpak+"\n")
		f.write("pathcsv="+ficheroCSV+"\n")
		f.close()
		print("\rGenerado fichero "+nameIni+
	" necesario para el proceso inverso: csv2pak.exe")
	except:
		error_y_sal("Error al guardar la configuración del proceso realizado\n"+
			"\r¡¡¡El archivo en"+nameIni+" no ha podido ser generado!!!")


if __name__ == "__main__":
	main(sys.argv[1:])
