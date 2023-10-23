from setuptools import setup, find_namespace_packages

setup(
    name='hello_world_kas',
    version='0.0.4',
    description='Very useful code',
    author='Andrii Kuriachyi',
    author_email='flyingcircus@example.com',
    license='MIT',
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['greeting=hello_world_kas.main:greeting']}
)