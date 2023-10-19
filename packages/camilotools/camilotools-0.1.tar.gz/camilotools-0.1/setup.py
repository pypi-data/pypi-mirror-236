from setuptools import setup, find_packages

setup(
    name='camilotools',
    version='0.1',
    packages=find_packages(),
    description='Ferramentas simples para envio de email, validação de email entre outros',
    long_description=open('README.md').read(),
    author='Camilo Costa de Carvalho',
    author_email='camilo.costa1993@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='tools, email-tools, email-validation',
    install_requires=['loguru'],
)
