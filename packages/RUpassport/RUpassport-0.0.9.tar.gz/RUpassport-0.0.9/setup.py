from setuptools import setup, find_packages

def readme():
    with open('README.md', 'r') as f:
        return f.read()



setup(
    name='RUpassport',
    version='0.0.9',
    author='@GusGus153',
    author_email='dimons2006@yandex.ru',
    description='Recognizes data from Russian passports and returns them',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/Filin153/RUpassport',
    packages=find_packages(),
    install_requires=["ultralytics==8.0.200", "easyocr==1.7.1", "opencv-python==4.8.1.78"],
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='ru rus RU RUS passport RUpassport recognition ',
    project_urls={
        'GitHub': 'https://github.com/Filin153/RUpassport'
    },
    python_requires='>=3.6',
    package_data={'': ['*.pt']},
)
