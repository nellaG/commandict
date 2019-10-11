from setuptools import setup


install_requires = {
    'requests >= 2.22.0, < 2.23.0',
    'beautifulsoup4 >= 4.7.1, < 4.7.2',
}


setup(name='commandict',
      version='0.1.2',
      description='Use Daum dic via CLI',
      url='http://github.com/nellag/commandict',
      author='nellaG',
      author_email='seirios0107@gmail.com',
      license='MIT',
      packages=['commandict'],
      entry_points='''
        [console_scripts]
        cmd = commandict.get_result:main
        cmdct = commandict.get_result:main
        cmdic = commandict.get_result:main
      ''',
      install_requires=list(install_requires),
      zip_safe=False)
