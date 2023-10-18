from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='TelegramBotsCallbackData',
  version='1.0.2',
  author='Wintreist',
  author_email='wintreist1811@gmail.com',
  description='This is a library for storing a lot of information in callback data',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/Wintreist/TelegramBotsCallbackData',
  packages=find_packages(),
  install_requires=[],
  keywords='Telegram Callback',
  project_urls={
    'GitHub': 'https://github.com/Wintreist'
  },
  python_requires='>=3.6'
)