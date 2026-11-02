"""Lanza siempre Cmder/ConEmu; no ejecuta Django en otra terminal."""
from pathlib import Path
import subprocess
import sys
root = Path(__file__).resolve().parent.parent
port = sys.argv[1] if len(sys.argv)>1 else '8000'
if not port.isdigit() or not 1 <= int(port) <= 65535:
    raise SystemExit('Puerto invalido')
local = root / '.local'
local.mkdir(exist_ok=True)
script = local / 'servidor.cmd'
script.write_text('@echo off\ncall E:\\cmder\\vendor\\init.bat\ncd /d "'+str(root)+'"\ncall INICIAR_BACKEND.cmd '+port+'\n', encoding='utf-8')
task = local / 'servidor.task'
task.write_text('cmd.exe /d /k "'+str(script)+'"\n',encoding='utf-8')
subprocess.Popen([r'E:\cmder\Cmder.exe', '/START', str(root), '/X', '-NoSingle -run @'+str(task)],cwd=root)
print('Cmder abierto; el iniciador comprueba MariaDB y el puerto antes de arrancar.')
