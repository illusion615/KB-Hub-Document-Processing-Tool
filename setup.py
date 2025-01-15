from setuptools import setup, find_packages

setup(
    name='document-processing-app',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A document processing application that converts PDF, Word, and PPT files into images and integrates with Microsoft Power Platform Dataverse.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'Flask',
        'Pillow',
        'python-docx',
        'PyPDF2',
        'python-pptx',
        'requests',
        'azure-identity',
        'azure-data-tables'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)