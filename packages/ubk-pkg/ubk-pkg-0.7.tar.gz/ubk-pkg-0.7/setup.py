from setuptools import setup, find_packages


setup(
    name='ubk-pkg',
    version='0.7',
    license='MIT',
    author="paytechuz",
    author_email='paytechuz@gmail.com',
    packages=find_packages('lib'),
    package_dir={'': 'lib'},
    url='https://github.com/paytechuz/ubk-pkg',
    keywords='account2card universal-bank ubk-pkg',
    install_requires=[
        'requests==2.*',
        'dataclasses==0.*',
      ],
)
