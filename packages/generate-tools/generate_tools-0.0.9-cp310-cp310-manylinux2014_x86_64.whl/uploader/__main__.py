import os
import shutil

# os.system('rm -rf ' + tempFile)

def upPypi():
    from generate import __version__ as version

    pythonVersion = [ '38', '39', '310' ]
    tempFile = 'dist/generate_tools-{}-cp311-cp311-manylinux2014_x86_64.whl'.format(version)
    outFile = 'dist/generate_tools-{}-cp{}-cp{}-manylinux2014_x86_64.whl'
    os.system('python setup.py bdist_wheel --plat-name manylinux2014_x86_64')
    for ver in pythonVersion:
        shutil.copy(tempFile, outFile.format(version, ver, ver))
    os.system('python -m twine check dist/*')
    os.system('python -m twine upload dist/*')


if __name__ == '__main__':
    upPypi()