import json

def cargar_datos(ruta):
	with open(ruta) as contenido:
		cursos = json.load(contenido)
		for curso in cursos:
			print("nombre: {}".format(curso.get('nombre')))
			print("slug: {}".format(curso.get('slug')))

ruta = "cursos.json"
cargar_datos(ruta)