from setuptools import setup, find_packages


setup(
    name='newlicensepkg',
    version='1.0',
    license='JAM',
    author="suryateja",
    author_email='suryateja.d@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/3PPMSTest/newlicensepkg',
    keywords='newlicensepkg',
    install_requires=[
          'scikit-learn',
      ],

)
