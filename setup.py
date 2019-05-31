from setuptools import setup

setup(name='german_recipe_crawler',
    version='0.0.1',
    description='Crawl german recipe pages',
    license='MIT',
    long_description=open("README.md").read(),
    author='Magdalena Deschner',
    author_email='mdeschner@hotmail.de',
    test_suite = 'tests',
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
    ],
)