from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Contact Book'
LONG_DESCRIPTION = 'A contact book with built-in bot to help you operate with your contacts'

setup(
    name="5_Stars_Contact_Book",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="<*****>",
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    keywords=['contact', 'book'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        'Topic :: Communications :: Telephony',
        "Programming Language :: Python :: 3",
    ]
)
