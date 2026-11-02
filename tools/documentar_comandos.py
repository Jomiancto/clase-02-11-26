"""Historial generado a partir de ejecuciones reales en Cmder."""
import json
from pathlib import Path
root=Path(__file__).resolve().parent.parent
records=[json.loads(line) for line in (root/'.local/comandos.jsonl').read_text(encoding='utf-8').splitlines()]
fence=chr(96)*3
text='''# Comandos Cmder — 2 de noviembre de 2026

Directorio de tareas: E:/cmder/clase-02-11-26.
Cada proceso verifica CMDER_ROOT y ConEmuPID. Despacho con Cmder.exe /START y
/X -NoSingle -run @archivo.task. Las fases usan cmd.exe /d /k, vendor/init.bat,
cd /d y tools/ejecutar.py. Los scripts exactos se incluyen abajo.
Logs completos locales: .local/*.log y .local/comandos.jsonl.
Las lecturas y ediciones mediante herramientas de archivos no son comandos de consola.
Una lectura inicial de la habilidad Windows se hizo mediante PowerShell;
Git, Django, MariaDB y la preparacion del editor se ejecutaron mediante Cmder.

## Errores y soluciones

- 03_diagnostico: UnicodeEncodeError al imprimir netstat con cp1252.
  Corregido tools/ejecutar.py a UTF-8 con sustitucion; repetido en 04_editor.
- 06_servidor: ModuleNotFoundError django; el hijo resolvia Python global.
  INICIAR_BACKEND.cmd usa ahora .venv/Scripts/python.exe explicitamente.
  Segundo arranque: 07_servidor en 8000.
- Bruno 6 en VS Code 1.88.1 no activa por crypto.subtle. Tres extensiones DB
  chocan. Se preparo un editor independiente actual con extensiones aisladas.

- 09_editor_actual: ZIP actual usa directorio de version; deteccion corregida.
- 10_editor_actual: nombre de extension Python Envs sin sufijo win32-x64; corregido.
- 12_verificacion: diff --check detecto linea vacia al final del historial; generador ajustado.
- 41_catalogo_tests: KeyError MIRROR antes de crear la base de pruebas al reemplazar TEST completo.
  Se corrigio tools/pruebas_catalogo.py para modificar solo TEST.NAME; 43_catalogo_tests paso 36 pruebas.

## Avance READ: resultados de comprobaciones

- Git previo limpio, origin exclusivo y commit inicial 9c34643.
- Cinco pruebas READ correctas sin crear base de pruebas; lista vacia simulada.
- check sin errores; makemigrations --check --dry-run sin cambios; migrate --check correcto.
- GET reales /clientes 200, /clientes/1 200 y /clientes/999999999 404.
- API anterior GET 200; CREATE invalido 400 y valido 201 con ORM create simulado.
- Hashes de todas las filas de negocio iguales antes y despues.
- Bruno ejecuto los tres GET y mostro 200/200/404.
- No se agregaron migraciones ni registros de prueba.

## Avance UPDATE y DELETE: resultados

- Quince pruebas READ/UPDATE/DELETE correctas, sin base de pruebas ni escrituras reales.
- POST temporales 2 y 3 en Bruno: 201; PATCH nombre y correo del temporal 2: 200.
- DELETE temporal 3 en Bruno: 204; DELETE inexistente: 404. MariaDB confirmo los cambios.
- Validaciones HTTP 400 y PATCH inexistente 404 correctos sin modificar filas ante errores.
- Se retiro tambien el temporal PATCH; hashes de todas las filas de negocio iguales al inicio.
- Cliente 1 y sus pedidos/items intactos; AUTO_INCREMENT avanzo por los temporales.
- Proteccion DELETE con pedidos: 409 comprobado con doble ORM; no se intento borrar ID 1.
- CREATE y READ y endpoints previos correctos antes y despues. Sin cambios de esquema.

## CRUD Categoria y Producto: comprobaciones

- Rama main limpia inicialmente, commit f267e04 y origin exclusivo. Respaldo privado previo.
- 36 pruebas correctas en MariaDB separada; base de pruebas creada solo si no existia y retirada al terminar.
- Diez operaciones principales enviadas en Bruno: POST 201, GET 200, PATCH 200 y DELETE 204 por entidad.
- Bruno 409 para Categoria con Producto y Producto con Item, usando solo relaciones temporales.
- Validaciones 400 y registros inexistentes 404 por HTTP real desde Cmder.
- Cliente temporal 4: CREATE/READ/UPDATE/DELETE correctos. Original ID 1 intacto.
- Todos los temporales retirados; filas de negocio originales completas iguales antes y despues.
- Modelos, serializers, migraciones y endpoints anteriores conservados.

## Comandos finalizados

'''
for i,r in enumerate(records,1):
    cmd=r['comando']
    purpose=('Revisar/preparar/publicar repositorio oficial; fuentes antiguas solo lectura.' if 'git ' in cmd else
             'Comprobar/instalar dependencias del entorno independiente.' if 'pip ' in cmd else
             'Inspeccionar migraciones sin modificar el esquema.' if 'migrat' in cmd else
             'Preparar o comprobar el componente indicado con resultado real registrado.')
    text+=f"### {i}. {r['fecha']}\n\nDirectorio: {r['directorio']}. ConEmuPID: {r['conemu_pid']}.\n\nObjetivo: {purpose}\n\n{fence}bat\n{cmd}\n{fence}\n\nResultado: codigo {r['codigo']}.\n\n"
    if r['codigo']!=0: text+='Error: consultar soluciones anteriores y log local de la fase.\n\n'
text+='''## Procesos activos y comando interrumpido

03_diagnostico ejecuto .venv/Scripts/python.exe .local/diagnostico.py;
no termino su registro por UnicodeEncodeError; la repeticion si esta registrada.

44_catalogo_servidor: cmd.exe /d /c INICIAR_BACKEND.cmd 8000 permanece ejecutandose.
31_ud_servidor se detuvo tras verificar su cadena hasta Cmder para cargar Categoria/Producto.
22_read_servidor se detuvo al agregar UPDATE/DELETE, verificando la cadena hasta su Cmder.
07_servidor fue detenido intencionalmente al agregar READ, despues de verificar
su cadena hasta el Cmder propio. No se detuvieron MariaDB ni procesos ajenos.
Ejecuta .venv/Scripts/python.exe manage.py runserver 127.0.0.1:8000 --noreload
mediante tools/ejecutar.py. No tiene codigo de salida final mientras sigue activo.
El iniciador ejecuta cd /d "%~dp0" y call .venv/Scripts/activate.bat.
Los check previos estan registrados y HTTP se verifico con tools/probar_create.py.

## Despacho de fases realmente ejecutadas

'''
for f in sorted((root/'.local').glob('*.cmd')):
    text+=f"Archivo local: .local/{f.name}\n\n{fence}bat\n{f.read_text(encoding='utf-8').strip()}\n{fence}\n\n"
(root/'COMANDOS_CMDER.md').write_text('\n'.join(line.rstrip() for line in text.splitlines()).rstrip()+'\n',encoding='utf-8',newline='\n')
print('Historial actualizado:',len(records),'comandos finalizados y servidor activo.')

# La regeneracion incluye cada comando finalizado hasta el instante anterior a esta ejecucion.
