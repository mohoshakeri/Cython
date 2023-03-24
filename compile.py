import os
from typing import Iterable

def compile(project:str,exclude:Iterable):

    excludes = ['__init__','compile','compiler']
    excludes.extend(exclude)
    files = []

    for path, j, file_list in os.walk(os.getcwd()):
        for file_name in file_list:
            if file_name.endswith(".py") and file_name[:-3] not in excludes:
                json = {
                    "name": file_name[:-3],
                    "full_name": file_name,
                    "dir": path + "/" + file_name,
                    "path": path,
                }
                files.append(json)

    if not os.path.exists(os.getcwd() + '/compiler.py'):
        new = open("compiler.py", "x")
        new.close()

    for file in files:
        
        file_name = file['name']
        file_dir = file['dir']
        file_path = file['path']
        
        with open("compiler.py", "w") as compiler:
            compiler.writelines(
                [
                    "from distutils.core import setup\n",
                    "from distutils.extension import Extension\n",
                    "from Cython.Distutils import build_ext\n",
                    "\n",
                    f'ext_modules = [Extension("{file_name}",  ["{file_dir}"]),]\n',
                    f'setup(name = "{project}",cmdclass'
                    + ' = {"build_ext": build_ext},ext_modules = ext_modules)\n',
                ]
            )
            compiler.close()
        
        os.system("python3 compiler.py build_ext --inplace")
        os.remove(file_path + '/' + file_name + '.c')
        for path, j, file_list in os.walk(os.getcwd()):
            for f in file_list:
                if f.endswith('.so') and f != file_name + '.so' and f.startswith(file_name):
                    os.rename(path + '/' + f ,file_path + '/' + file_name + '.so')
                    os.remove(file_path + '/' + file_name + '.py')
    os.remove(os.getcwd() + '/compiler.py')