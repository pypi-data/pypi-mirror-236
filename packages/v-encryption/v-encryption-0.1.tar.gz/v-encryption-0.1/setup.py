from setuptools import setup, find_packages
 
setup(
    include_package_data=True,
	name="v-encryption",
	version="0.1",
	packages=find_packages(), # permet de récupérer tout les fichiers 
	description="",
	url="https://encryption.nexcord.pro/",
	author="V / Lou du Poitou",
	license="ISC",
	python_requires=">=3.9.7",
    py_modules=["requests"]
)