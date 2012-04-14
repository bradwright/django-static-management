from setuptools import setup

setup(
    name='django-static-management',
    version='1.3.0',
    url='https://github.com/bradleywright/django-static-management',
    license='BSD',
    author='Bradley Wright',
    author_email='brad@intranation.com',
    description='An easy way of managing static (CSS and JS) assets in Django projects, including build scripts.',
    long_description="",
    packages=['django_static_management'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'django==1.1'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
