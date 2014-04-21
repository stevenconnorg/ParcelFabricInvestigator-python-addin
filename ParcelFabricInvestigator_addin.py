'''
Title: ParcelFabricInvestigator_addin
Author: Stephanie Wendel
Created: 1/13/2014
Update: 4/21/2014
Version: 1.4.1

Description: Provides a toolbar of buttons to use in ArcGIS Desktop that
investigate potential data issues with the Parcel Fabric.

'''

import arcpy
import pythonaddins
import os

# Global Variables
parcelFabric = None
parcelFabricLayer = None
SR = None
mxd = arcpy.mapping.MapDocument("Current")
df = arcpy.mapping.ListDataFrames(mxd)[0]


class Attributes(object):
    """Implementation for ParcelFabricInvestigator_addin.Attributes (Button)
    This tool is not implemented."""
    def __init__(self):
        self.enabled = False
        self.checked = False
    def onClick(self):
        pass

class DupPoints(object):
    """Implementation for ParcelFabricInvestigator_addin.DupPoints (Button)
    Finds where there are duplicated points within the Points layer of the
    fabric"""
    def __init__(self):
        self.enabled = False
        self.checked = False
    def onClick(self):
        workspace, PFname = os.path.split(parcelFabric)
        ParcelPoints = "FabricInvestigation\\Points"
        DuplicatePointsTable = os.path.join("in_memory", PFname + "_IdenticalPoints")
        arcpy.FindIdentical_management(ParcelPoints, DuplicatePointsTable ,"X;Y",
                                       "#","0","ONLY_DUPLICATES")
        arcpy.AddJoin_management(ParcelPoints, "OBJECTID", DuplicatePointsTable,
                                 "IN_FID", "KEEP_COMMON")
        saveDuplicates = pythonaddins.SaveDialog("Save Duplicate Points")
        arcpy.CopyFeatures_management(ParcelPoints, saveDuplicates)
        newPath, newLayer = os.path.split(saveDuplicates)
        arcpy.mapping.MoveLayer(df, arcpy.mapping.ListLayers(mxd,
                                                            "FabricInvestigation")[0],
                                                             arcpy.mapping.ListLayers(mxd, newLayer)[0],
                                                             "BEFORE")
        DupPoints.checked = False

class Lines(object):
    """Implementation for ParcelFabricInvestigator_addin.Lines (Button)
    This too is not implemented."""
    def __init__(self):
        self.enabled = False
        self.checked = False
    def onClick(self):
        pass

class Parcel(object):
    """Implementation for ParcelFabricInvestigator_addin.Parcel (Button)
    This tool looks at the Check Fabric text file and finds problematic parcels.
    It selects those parcels and allows the user to export them."""
    def __init__(self):
        self.enabled = False
        self.checked = False
    def onClick(self):
        message1 = "Have you saved a text file report from the Check Fabric tool for the setup fabric?\n\n If yes, click OK and navigate to the location.\n\n If not, click Cancel. Please run the Check Fabric tool by right clicking on the parcel fabric. Next save the report as a text file."
        box1 = pythonaddins.MessageBox(message1, "Find Check Fabric Text File", 1)
        if box1 == 'OK':
            textFile = pythonaddins.OpenDialog("Find Check Fabric Text File")
            #print textFile
            F1 = open(textFile, 'rb')
            parcelId1 = []
            for line in F1:
                if "Parcel with ID =" in line:
                    pID = line[17:-28]
                    parcelId1.append(pID)
            pfl = arcpy.mapping.ListLayers(mxd, "*Parcels")
            for layer in pfl:
                if layer.name == "Tax Parcels":
                    polygons = "FabricInvestigation\\Tax Parcels"
                elif layer.name == "Parcels":
                    polygons = "FabricInvestigation\\Parcels"
                else:
                    # Adding a message box here will cause tool to fail due to
                    # the looping of the layers when it finds layers not
                    # containing the Parcels or Tax Parcels.
                    pass
            for ID in parcelId1:
                if ID == parcelId1[0]:
                    where = '"OBJECTID" =' + str(ID)
                else:
                    where = where + 'OR "OBJECTID" = ' + str(ID)

            arcpy.SelectLayerByAttribute_management(polygons, "NEW_SELECTION",
                                                    where)

            box3 = pythonaddins.MessageBox("Done selecting bad parcels. Click Yes if you would like to save as a feature class. Click No to return to map.",
                                           "Finished Process", 4)
            if box3 == "Yes":
                newFC = pythonaddins.SaveDialog("Save Bad Parcels")
                if newFC != "Cancel":
                    arcpy.CopyFeatures_management(polygons, newFC)
            else:
                pass
        newPath, newLayer = os.path.split(newFC)
        arcpy.mapping.MoveLayer(df, arcpy.mapping.ListLayers(mxd,
                                "FabricInvestigation")[0],
                                arcpy.mapping.ListLayers(mxd, newLayer)[0],
                                "BEFORE")
        Parcel.checked = False

class ParcelFabricSetup(object):
    """Implementation for ParcelFabricInvestigator_addin.ParcelFabricSetup (Button)
    This setups a parcel fabric to be used in the tools and adds the layer to the
    map."""
    def __init__(self):
        self.enabled = True
        self.checked = True
    def onClick(self):
        global parcelFabric, parcelFabricLayer, SR
        box = pythonaddins.MessageBox("Navigate to the Parcel Fabric you wish to investigate.",
                                      "Select Parcel Fabric", 0)
        parcelFabric = pythonaddins.OpenDialog("Find Parcel Fabric")
        parcelFabricLayer = arcpy.MakeParcelFabricLayer_fabric(parcelFabric,
                                                               "FabricInvestigation")
        SR = arcpy.Describe(parcelFabric).spatialReference
        Parcel.enabled = True
        Parcel.checked = True
        DupPoints.enabled = True
        DupPoints.checked = True
        Point.enabled = True
        Point.checked = True
        ParcelFabricSetup.checked = False
        ParcelLineGaps.enabled = True
        ParcelLineGaps.checked = True
        # To add
##        pfl = arcpy.mapping.ListLayers(mxd, "*Parcels")
##        for layer in pfl:
##            if layer.name == "Tax Parcels":
##                polygons = "FabricInvestigation\\Tax Parcels"
##            elif layer.name == "Parcels":
##                polygons = "FabricInvestigation\\Parcels"
##            else:
##                #Adding a message box here will cause tool to fail due to the looping of the layers and when if finds non Parcel layers.
##                pass

class ParcelLineGaps(object):
    """Implementation for ParcelFabricInvestigator_addin.ParcelLineGaps (Button)
    This tool shows where there are gaps in the fabric between the lines and the Parcels"""
    def __init__(self):
        self.enabled = False
        self.checked = False
    def onClick(self):
        box = pythonaddins.MessageBox("You are about to look for gaps. This process could take a long time depending on the size of the fabric. Please be patient with the interface until it shows a finished message.", \
                                      "Select Parcel Fabric", 1)
        if box == "OK":
            workspace, PFname = os.path.split(parcelFabric)
            topology = os.path.join(workspace, PFname + "_topology")
            if arcpy.Exists(topology):
                arcpy.Delete_management(topology)
            arcpy.CreateTopology_management(workspace, PFname + "_topology")
            pfl = arcpy.mapping.ListLayers(mxd, "*Parcels")
            for layer in pfl:
                if layer.name == "Tax Parcels":
                    polygons = "FabricInvestigation\\Tax Parcels"
                elif layer.name == "Parcels":
                    polygons = "FabricInvestigation\\Parcels"
                else:
                    # Adding a message box here will cause tool to fail due to
                    # the looping of the layers when it finds layers not
                    # containing the Parcels or Tax Parcels.
                    pass
            arcpy.AddFeatureClassToTopology_management(topology, polygons)
            arcpy.AddFeatureClassToTopology_management(topology,
                                                       "FabricInvestigation\\Lines")
            polygon_fc = os.path.join(workspace, PFname + "_Parcels")
            line_fc = os.path.join(workspace, PFname + "_Lines")
            arcpy.AddRuleToTopology_management(topology,
                                               "Boundary Must Be Covered By (Area-Line)",
                                               polygon_fc, "", line_fc)
            arcpy.ValidateTopology_management(topology)
            gdb, fds_name = os.path.split(workspace)
            arcpy.ExportTopologyErrors_management(topology, gdb, "Gaps")
            arcpy.mapping.MoveLayer(df, arcpy.mapping.ListLayers(mxd,
                                    "FabricInvestigation")[0],
                                    arcpy.mapping.ListLayers(mxd,
                                    "Gaps_line")[0], "BEFORE")
            arcpy.mapping.RemoveLayer(df, arcpy.mapping.ListLayers(mxd,
                                     "Gaps_point")[0])
            arcpy.mapping.RemoveLayer(df, arcpy.mapping.ListLayers(mxd,
                                     "Gaps_poly")[0])
            arcpy.mapping.RemoveLayer(df, arcpy.mapping.ListLayers(mxd,
                                     PFname + "_topology")[0])
            box2 = pythonaddins.MessageBox("Finished Processing Gaps. Please proceed.",
                                           "Finsihed Processing Gaps", 0)
            ParcelLineGaps.checked = False


class Point(object):
    """Implementation for ParcelFabricInvestigator_addin.Point (Button)
    This shows points that are not in their true locations in the display based
    on their x and y values."""
    def __init__(self):
        self.enabled = False
        self.checked = False
    def onClick(self):
        arcpy.MakeXYEventLayer_management("FabricInvestigation\\Points", "X", "Y",
                                          "TruePointLocations", SR)
        (arcpy.mapping.ListLayers(mxd, "TruePointLocations")[0]).visible = False
        arcpy.SelectLayerByLocation_management("FabricInvestigation\\Points",
                                               "ARE_IDENTICAL_TO",
                                               "TruePointLocations",
                                               selection_type="NEW_SELECTION")
        arcpy.SelectLayerByLocation_management("FabricInvestigation\\Points",
                                                selection_type="SWITCH_SELECTION")
        box = pythonaddins.MessageBox("Done selecting points that are in the wrong location. You will not see any selected points if there is a visible scale range set and you are not in that range. Click Yes if you would like to save as a feature class. Click No to return to map.",
                                      "Finished Process", 4)
        if box == "Yes":
            newFC = pythonaddins.SaveDialog("Save Bad Parcels")
            if newFC != "Cancel":
                arcpy.CopyFeatures_management("FabricInvestigation\\Points", newFC)
        else:
            pass
        newPath, newLayer = os.path.split(newFC)
        arcpy.mapping.MoveLayer(df, arcpy.mapping.ListLayers(mxd,
                                                            "FabricInvestigation")[0],
                                                             arcpy.mapping.ListLayers(mxd, newLayer)[0],
                                                             "BEFORE")
        Point.checked = False

class Summary(object):
    """Implementation for ParcelFabricInvestigator_addin.Summary (Button)
    This tool is not yet implemented"""
    def __init__(self):
        self.enabled = False
        self.checked = False
    def onClick(self):
        pass

