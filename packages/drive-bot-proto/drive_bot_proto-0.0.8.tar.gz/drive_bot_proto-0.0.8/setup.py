from setuptools import setup


setup(
      name='drive_bot_proto',
      version='0.0.8',
      description='GRPC client for drive_bot_proto',
      author='Pavel Anokhin',
      author_email='p.a.anokhin@gmail.com',
      packages=['drive_bot_proto'],
      package_data={
          'drive_bot_proto': ['*.pyi', 'py.typed'],
      },
      include_package_data=True,
)