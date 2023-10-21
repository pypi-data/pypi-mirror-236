from setuptools import *
# import pdf_docx_pic.check as c
# 失败的功能
# 
# c.check()

a = open(".\\README.md", mode='r', encoding = 'UTF-8').read()

setup(
    name = "pdp1",
    version = "1.0.18448.20194.2",
    py_modules = [
        './pdp1/'],
    packages = find_packages(),
    python_requires = ">=3.9, <=3.13",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Framework :: Jupyter :: JupyterLab :: 4",
        "Framework :: Django :: 4",
        "Framework :: Django :: 4.2",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Framework :: Jupyter :: JupyterLab :: Extensions :: Mime Renderers",
        "Operating System :: Microsoft :: Windows :: Windows 8",
        "Operating System :: Microsoft :: Windows :: Windows 8.1",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
        "Operating System :: POSIX",
        "Natural Language :: Chinese (Simplified)",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Typing :: Typed",
    ],
    install_requires = [
        "ttkbootstrap>=1.9.0, !=1.10.0, <1.15",
        "pdf2docx!=0.5.3, <1.0", 
        "docx2pdf!=0.1.2, !=0.1.6, !=0.1.7, >=0.1, <1", 
        "PyMuPDF!=1.23.2, >=1.23.1, <1.30", 
        "Pillow>=9, !=9.5.0, <11", 
        "wheel>=0.40.1, !=0.41.1, <1",
    ],
    long_description = a
)
