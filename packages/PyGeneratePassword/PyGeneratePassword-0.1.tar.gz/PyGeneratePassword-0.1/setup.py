from setuptools import setup

with open('README.rst', 'r', encoding='utf-8') as f:
    ln = f.read()

setup(
    name="PyGeneratePassword",
    version="0.1",
    description="Generate Random password",
    long_description= ln,
    long_description_content_type='text/x-rst',
    license="MIT",
    author="Md. Ismiel Hossen Abir",
    packages=["PyGeneratePassword"],
    url="https://pypi.org/project/PyGeneratePassword/",
    install_requires=[]
    
)