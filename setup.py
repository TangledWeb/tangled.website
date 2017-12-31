from setuptools import setup


setup(
    name='tangled.website',
    version='1.0a1.dev0',
    description='tangledframework.org',
    long_description=open('README.rst').read(),
    url='https://tangledframework.org/',
    download_url='https://github.com/TangledWeb/tangled.website/tags',
    author='Wyatt Baldwin',
    author_email='self@wyattbaldwin.com',
    packages=[
        'tangled',
        'tangled.website',
    ],
    include_package_data=True,
    install_requires=[
        'tangled.auth>=0.1a3',
        'tangled.session>=0.1a3',
        'tangled.site>=1.0a5',
        'SQLAlchemy>=1.1.6',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
