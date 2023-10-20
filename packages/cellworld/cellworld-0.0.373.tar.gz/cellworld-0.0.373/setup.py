from setuptools import setup

setup(name='cellworld',description='Maciver Lab computational biology research package',author='german espinosa',author_email='germanespinosa@gmail.com',packages=['cellworld'],install_requires=['numpy', 'scipy', 'matplotlib', 'json-cpp>=1.0.77', 'tcp-messages', 'networkx', 'cv'],data_files=[('files',['cellworld/files/mouse.png','cellworld/files/robot.png'])],package_data={'files':['cellworld/files/mouse.png','cellworld/files/robot.png']}, include_package_data=True,license='MIT',version='0.0.373',zip_safe=False)
