from setuptools import setup, find_packages

setup(
    name='Kraggen',
    version='0.1',
    description='A django cms project',
    long_description=open('README').read(),
    author='Maxime Barbier',
    author_email='maxime.barbier1991@gmail.com',
    url='https://github.com/Krozark/Kraggne/tree/master',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 0 ',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    install_requires = [
        "django-generic-flatblocks",
        "django-frontadmin",
        "django-mptt",
    ],
    zip_safe=False,
)
