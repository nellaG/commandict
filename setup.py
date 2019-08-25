from setuptools import setup

setup(name='commandict',
      version='0.1.0',
      description='Use Daum dic via CLI',
      url='http://github.com/nellag/commandict',
      author='nellaG',
      author_email='seirios0107@gmail.com',
      license='MIT',
      packages=['commandict'],
      entry_points='''
        [console_scripts]
        cmdct = commandict.get_result:main
        cmd = commandict.get_result:main
    ''',
      zip_safe=False)
