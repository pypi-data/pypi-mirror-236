from setuptools import setup, find_packages

setup(
    name='KGIapi',
    version='0.2',
    description='My test project',
    author='Louis Hsu',
    author_email='Louis.Hsu@kgi.com',
    packages=find_packages(),
    package_data={
        'KGIapi': [
            './Package.dll',
            './PushClient.dll',
            './TradeCom.dll',
            './QuoteCom.dll',
        ]
    },
    install_requires=[
        'pythonnet'
    ]
)