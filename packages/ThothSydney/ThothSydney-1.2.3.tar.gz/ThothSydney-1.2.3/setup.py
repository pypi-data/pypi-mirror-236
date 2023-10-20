from setuptools import setup, find_packages

setup(
    name='ThothSydney',
    version='1.2.3',
    author='ThothAI',
    author_email='thoth@thothai.onrender.com',
    description='A fork of sydney-py which includes a better response format and the ability to change the system instructions prompt.',
    long_description='A fork of sydney-py which includes a better response format and the ability to change the system instructions prompt. https://thothai.onrender.com/discord',
    packages=find_packages("src"),
    package_dir={"": "src"},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)