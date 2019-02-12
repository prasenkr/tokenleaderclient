from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()


setup(name='tokenleaderclient',
      version='0.3',
      description='Client for token based authentication and role based access control',
      long_description=readme(),
      url='https://github.com/microservice-tsp-billing/tokenleader-client',
      author='Bhujay Kumar Bhatta',
      author_email='bhujay.bhatta@yahoo.com',
      license='MIT',
      packages=['tokenleaderclient'],
      install_requires=[
          'markdown',
          'PyJWT==1.7.0',
          'PyYAML==3.13',
      ],

      zip_safe=False)