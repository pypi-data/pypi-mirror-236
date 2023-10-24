import setuptools

setuptools.setup(
	name='donate',
	version='1.2.1',
	author='Redpiar',
	author_email='Regeonwix@gmail.com',
	description='library for donations',
	packages=['donate'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	install_requires=['requests'],
	python_requires='>=3.6',
)