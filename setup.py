from setuptools import setup, find_packages


setup(
    name='tangled.website',
    version='0.1.dev0',
    description='tangledframework.com',
    long_description=open('README.rst').read(),
    url='http://tangledframework.org/',
    author='Wyatt Baldwin',
    author_email='self@wyattbaldwin.com',
    packages=find_packages(),
    install_requires=(
        'tangled.auth>=0.1.dev0',
        'tangled.session>=0.1.dev0',
        'tangled.site>=0.1.dev0',
        'SQLAlchemy>=0.9.1',
    ),
    extras_require={
        'dev': ('coverage',),
    },
    classifiers=(
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ),
)
