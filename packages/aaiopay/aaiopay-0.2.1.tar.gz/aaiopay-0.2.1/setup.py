from setuptools import setup, find_packages


def requirements():
	requirements_list = list()
	with open('requirements.txt') as pc_requirements:
		for install in pc_requirements:
			requirements_list.append(
				install.strip()
			)
	return requirements_list


with open("README.md", "r", encoding="utf-8") as desc_long:
	description_long = desc_long.read()


setup(
	name='aaiopay',
	version='0.2.1',
	description='Asynchronous module for working with the aaio API',
	long_description=description_long,
	packages=find_packages(),
	long_description_content_type='text/markdown',
	author='VoXDoX',
	author_email='1voxdox1@gmail.com',
	keywords=['aaio', 'aaio api', 'AaioAsync', 'aaio'],
	zip_safe=False,
	install_requires=requirements(),
	project_urls={
		"TG Channel": "https://t.me/AsyncModules",
		"Github": "https://github.com/VoXDoX/async-payok",
	},
	python_requires=">=3.7"
)
