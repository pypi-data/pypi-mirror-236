from setuptools import setup, find_packages
setup(name='provapipeline2023',
      version='0.1.1',
      description='Some Python package',
      author='Me',
      author_email='me@example.com',
      license='MIT',
      packages=["application", "database"],
      package_dir={
            "": ".",
            "application": "./application",
            "database": "./database",
      },
      zip_safe=False)

