from setuptools import setup, find_packages

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='JyPyUI',
    version='1.0.8',
    license='MIT License',
    author='Paulo Pelecer',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='ppelecer@gmail.com',
    keywords='jypyui',
    description=u'JyPyUI e uma Interface grafica Baseada no Pygame Focada no android ',
    packages=["JyPyUI"],
    install_requires=['requests','plyer','pygame','pyjnius','gtts'],)
