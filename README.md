# ReportFeatureServiceAGOL-Python

## Features

The current version is 1.4.1.

* ParcelFabricInvestigator.esriaddin made up of:
	* README.txt   : Readme file for the addin.

	* makeaddin.py : A script that will create a .esriaddin file out of this project, suitable for sharing or deployment

	* config.xml   : The AddIn configuration file

	* Images/*     : all UI images for the project (icons, images for buttons, etc)

	* Install/*    : The Python project used for the implementation of the AddIn. The specific python script to be used as the root module is specified in config.xml.

* ParcelFabricInvestigator_addin.py which is the source code for the addin. Buttons include:
	* Attributes		- Not yet implemented.
	* DupPoints		- Finds where there are duplicated points within the Points layer of the fabric.
	* Lines			- Not yet implemented.
	* Parcels		- This tool looks at the Check Fabric text file and finds problematic parcels. It selects those parcels and allows the user to export them.
	* ParcelFabricSetup	- This setups a parcel fabric to be used in the tools and adds the layer to the map.
	* ParcelLineGaps	- This tool shows where there are gaps in the fabric between the lines and the Parcels.
	* Point			- This shows points that are not in their true locations in the display based on their x and y values.
	* Summary		- Not yet implemented.


## Instructions

Note: Please use a copy of production parcel fabric data for use in this tool. Author is not responsible for any corruption that may occur. This is a sample addin and can be modified as needed.

1. Fork and then clone the repo or download the files.
2. Install the add-in by double clicking on the esriaddin file. 
3. Start ArcMap. 
4. A toolbar should be present in the interface. If not check the Add-in Manager to make sure the add-in installed. Then look for the ParcelInvestigator toolbar.
5. Run and try the sample with your own parcel fabric copy.


## Requirements

* Your favorite Python editor to make modifications to the code.
* Python Add-in Wizard to make a new python addin which can be found [here](http://www.arcgis.com/home/item.html?id=5f3aefe77f6b4f61ad3e4c62f30bff3b).
* ArcGIS Desktop 10.2.x with a Standard or Advanced license
* A parcel fabric dataset (please make a copy before running tools on your fabric).


## Resources

* [ArcGIS Desktop 10.2 Help - ArcGIS Desktop Python add-ins](http://resources.arcgis.com/en/help/main/10.2/#/What_is_a_Python_add_in/014p00000025000000/)
* [ArcGIS Desktop 10.2 Help - What is a parcel fabric](http://resources.arcgis.com/en/help/main/10.2/index.html#/What_is_a_parcel_fabric/00wp0000002v000000/)


## Issues

This is not supported through Esri Support. If you find a bug or want to request a new feature, please let me know by submitting an issue on this page.

If submitting issues for this add-in, please test at version 10.2.x. This addin is not tested on ArcGIS 10.1 and issues will not be addressed for that version.


## Contributing


Anyone and everyone. I follow the Esri Github guidelines for contributing. Please see [guidelines for contributing](https://github.com/esri/contributing).


## Licensing

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at


   http://www.apache.org/licenses/LICENSE-2.0


Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


A copy of the license is available in the repository's [license.txt](https://github.com/swwendel/ParcelFabricInvestigator-python-addin/blob/master/license.txt) file.
