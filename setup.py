import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'vizent',
    packages = ['vizent'],
    package_data={'vizent': ['images/*.png']},
    include_package_data = True,
    version = '1.0.1',
    license='MIT',
    description = 'A library for creating scatterplots using visual entropy glyphs.',
    author = 'Lucy McLaughlin',
    author_email = 'lucy.mclaughlin@ncl.ac.uk',
    url = 'https://github.com/luyc12/vizent',
    keywords = ['visualization', 'plot', 'bivariate', 'glyphs', 'scatterplot', 'dataviz'],
    install_requires = ['matplotlib', 'numpy', 'scipy'],
    extras_require = {
        'background_map': ['cartopy'],
        'background_image': ['pillow']
    },
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: End Users/Desktop',
      'Intended Audience :: Science/Research',
      'Topic :: Scientific/Engineering :: Visualization',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3',
    ],
)