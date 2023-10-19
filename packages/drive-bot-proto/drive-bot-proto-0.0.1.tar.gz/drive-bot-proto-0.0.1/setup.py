from setuptools import setup


setup(name='drive-bot-proto',
      version='0.0.1',
      description='GRPC client for drive-bot-proto',
      author='Pavel Anokhin',
      author_email='p.a.anokhin@gmail.com',
      packages=['drive-bot-proto'],
      package_data={
          'drive-bot-proto': ['*.pyi', 'py.typed'],
      },
      include_package_data=True,
)