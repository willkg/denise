from setuptools import setup


setup(
    name='denise',
    version='1.0',
    description='Dennis-as-a-service website',
    author='Will Kahn-Greene',
    author_email='willkg@mozilla.com',
    url='',
    install_requires=[
        'Flask',
        'Flask-Script',
        'dennis',
        'requests'
    ]
)
