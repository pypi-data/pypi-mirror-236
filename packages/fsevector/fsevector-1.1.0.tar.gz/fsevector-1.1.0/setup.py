from setuptools import find_packages, setup

requires = [
    'uvloop >= 0.16.0',
    'tiktoken >= 0.4.0',
    'requests >= 2.4.2',
    'requests_toolbelt >= 0.3.0',
    'psycopg2-binary >= 2.9.7',
    'pyOpenSSL >= 19.1.0',
    'openai >= 0.28.0',
    'langchain >= 0.0.315',
]

setup(
    name='fsevector',
    version='1.1.0',
    packages=find_packages(exclude=['tests*']),
    url='https://gitlab.deepglint.com/chenbo/fsevector',
    license='Apache License 2.0',
    author='bchen',
    author_email='bochen@deepglint.com',
    description='Deepglint fse vectorstore',
    long_description_content_type='text/markdown',
    long_description=open('README.md', encoding='utf-8').read(),
    python_requires=">= 3.8",
    install_requires=requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    project_urls={
        'Documentation': 'https://gitlab.deepglint.com/chenbo/fsevector',
        'Source': 'https://gitlab.deepglint.com/chenbo/fsevector',
    },
)
