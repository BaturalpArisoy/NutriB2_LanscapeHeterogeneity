#!/usr/bin/env python
# coding: utf-8

# # **Automatization Process for LHI**

# **This code is designed to create systematic process for the automatization of Landscape Heterogeneity Index calculation**<br><br>
# **Baturalp Arisoy, TUM Msc Geodesy and Geoinformation, 2022**<br>**NutriB2**

# ![nutrib2.png](attachment:nutrib2.png)

# ## Import ArcPy

# In[ ]:


import os
import arcpy
from arcgis.gis import GIS

import pandas as pd
#import rasterio as rio
from arcpy.ia import *

import numpy as np
import math
from math import e


import time
start_time = time.time()


# In[ ]:


## Setting up environement

arcpy.env.workspace = r'D:\\Master\\Alb\\notebook' # Feel free to change this but never change syntaxes!
#current_directory = arcpy.env.workspace = r'D:\\Master\\Alb\\notebook' 
#os.chdir(current_directory)
print('Default Workspace of Python Code text file: ' + os.getcwd())
print('Current Workspace for geoprocesing: ' + arcpy.env.workspace)

arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = True
#environments = arcpy.ListEnvironments()

# Sort the environment names
#environments.sort()

#for environment in environments:
    # Format and print each environment and its current setting.
    # (The environments are accessed by key from arcpy.env.)
#    print("{0:<30}: {1}".format(environment, arcpy.env[environment]))


# ## Loading data

# Only select your plot no<br>If the plot number is between 1-9, always enter it with 0<br><br>**E.g.**<br> **AEG01 - Correct**<br> **AEG1 - Incorrect**

# In[ ]:


# GET PLOT NO
#getPlot = 'AEG01'

getPlot = ['HEG01', 'HEG13']

textList = [] 

textPath = arcpy.env.workspace + r'\\report.txt' 



for ep in getPlot:


    if ep[3] == '0':


        def remove(string, i): 

            # Characters before the i-th indexed
            # is stored in a variable a
            a = string[ : i] 

            # Characters after the nth indexed
            # is stored in a variable b
            b = string[i + 1: ]

            # Returning string after removing
            # nth indexed character.
            return a + b

        # Driver Code
        if __name__ == '__main__':

            string = ep

            # Remove nth index element
            i = 3

            # Print the new string
            # print(remove(string, i))





        getNewPlot = remove(string, i)
    else:
        getNewPlot = ep


    print(ep)    
    print(getNewPlot)




    input_rasterLayer = r'.\\DOP20s\\{}.tif'.format(ep)
    print(input_rasterLayer)
    ###
    where_clause = "Name = '{}'".format(ep) ##### check this one always getNewPlot
    print(where_clause)
    ###

    plotNo = "{}".format(ep)
    print(plotNo)

    classification_output = r".\\SVM\\classificationout{}.tif".format(ep)
    print(classification_output)

    outPolygons = r".\\output\\outploygon{}.shp".format(ep)
    print(outPolygons)

    output_feature_class = r".\\output\\outfeature{}.shp".format(ep)
    print(output_feature_class)

    out_raster = r".\\output\\outraster{}.tif".format(ep)
    print(out_raster)
    
    
    #input_stationLayer = r'.\\vector\\weatherStations.shp'  #only for Alb
    
    input_stationLayer = r'.\\vector\\allStations.shp'
    
    
    
    # ALB
#    input_OSMBuilding = r'.\\tuebingen-regbez-latest-free.shp\\gis_osm_buildings_a_free_1.shp'
#    input_OSMRailways = r'.\\tuebingen-regbez-latest-free.shp\\gis_osm_railways_free_1.shp'
#    input_OSMRoads = r'.\\tuebingen-regbez-latest-free.shp\\gis_osm_roads_free_1.shp'
#    input_OSMWaterways = r'.\\tuebingen-regbez-latest-free.shp\\gis_osm_waterways_free_1.shp'
    
    
     # Hainich
    input_OSMBuilding = r'.\\thueringen-latest-free.shp\\gis_osm_buildings_a_free_1.shp'
    input_OSMRailways = r'.\\thueringen-latest-free.shp\\gis_osm_railways_free_1.shp'
    input_OSMRoads = r'.\\thueringen-latest-free.shp\\gis_osm_roads_free_1.shp'
    input_OSMWaterways = r'.\\thueringen-latest-free.shp\\gis_osm_waterways_free_1.shp'
    
    

    ## Plot Buffer Area 

    input_plotNo = arcpy.SelectLayerByAttribute_management(input_stationLayer, "NEW_SELECTION", where_clause)
    input_stationData = arcpy.CopyFeatures_management(input_plotNo, "in_memory/stationData")

    plotBuffer = arcpy.Buffer_analysis(input_stationData, "in_memory/stationBuffer500", "500 Meters", "", 
                          "ROUND", "NONE", "", "GEODESIC")

    #arcpy.CopyFeatures_management(testoutput, ".\\output\\test.shp")
    print("Buffer success")

    ## Clip DOP20

    # Set local variables

    # Get extent
    desc = arcpy.Describe(plotBuffer)


    xmin = desc.extent.projectAs(arcpy.SpatialReference(32632)).XMin
    xmax = desc.extent.projectAs(arcpy.SpatialReference(32632)).XMax
    ymin = desc.extent.projectAs(arcpy.SpatialReference(32632)).YMin
    ymax = desc.extent.projectAs(arcpy.SpatialReference(32632)).YMax

    print(xmin, xmax, ymin, ymax)


    #rectangle = xmin, xmax, ymin, ymax
    rectangle = str(xmin) + ' ' + str(ymin) + ' ' + str(xmax) + ' ' + str(ymax)
    print(rectangle)

    #print(os.path.getsize(input_rasterLayer))

    rectangle = str(xmin) + ' ' + str(ymin) + ' ' + str(xmax) + ' ' + str(ymax)
    #out_raster = r".\\output\\clippedPlot.tif"

    # Execute Raster Clip
    clippedPlot = arcpy.management.Clip(input_rasterLayer, rectangle, out_raster, 
                          plotBuffer, '#', 'ClippingGeometry', '#')

    print('Clipping image successful')
    arcpy.AddMessage('Clipping image successful')

    ## **Support Vector Machine (SVM) Classification**

    ### Classification and export geoTIFF

    #**Process below can take some time, depending on GPU and CPU power**<br>**(but doesn't require high GPU VRAM memory)**

    # Set local variables

    insegras = clippedPlot
    indef_file = r".\\SVM\\ClassDefRGB.ecd"
    in_additional_raster = "#"

    # Execute 
    classifiedraster = ClassifyRaster(insegras, indef_file, in_additional_raster)

    #save output
    classifiedRaster = classifiedraster.save(arcpy.env.workspace + classification_output) #check classifiedRaster if it works
    #classifiedRaster = classifiedraster.save(classification_output) #check classifiedRaster if it works
    print("Done")

    ## **OSM data**

    ### Clipping

    # Set local variables
    clip_features = plotBuffer
    outputBuilding = r".\\output\\clippedBuilding.shp"
    outputRailways = r".\\output\\clippedRailways.shp"
    outputRoads = r".\\output\\clippedRoads.shp"
    outputWaterways = r".\\output\\clippedWaterways.shp"

    # Execute Clips
    arcpy.analysis.Clip(input_OSMBuilding, clip_features, outputBuilding)
    arcpy.analysis.Clip(input_OSMRailways, clip_features, outputRailways)
    arcpy.analysis.Clip(input_OSMRoads, clip_features, outputRoads)
    arcpy.analysis.Clip(input_OSMWaterways, clip_features, outputWaterways)

    print("Clipping done")
    arcpy.AddMessage("Clipping done")

    #**Info on empty output**

    def getCount(inputFC):
        #Evaluate if input has greater than 0 features

        if (arcpy.management.GetCount(inputFC)[0] == "0"):
            #arcpy.AddMessage("{} : empty output".format(inputFC))
            print("{} : empty output".format(inputFC))
            return False

        #If it does not have greater than 0 features it will have 0
        else:
            #arcpy.AddMessage("{} : successful output".format(inputFC))
            print("{} : successful output".format(inputFC))
            return True

    print("building:")
    getCount(outputBuilding)
    print("railway:")
    getCount(outputRailways)
    print("roads:")
    getCount(outputRoads)
    print("waterway:")
    getCount(outputWaterways)





    ### Buffer and table manipulation

    def addField(feature, classname):

        # Add Field
        arcpy.management.AddField(feature, field_name="Class_name", 
                                  field_type="TEXT", field_precision=None, 
                                  field_scale=None, field_length=20, field_alias="", 
                                  field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")

        # Calculate Field
        arcpy.management.CalculateField(feature, field="Class_name", 
                                        expression= "{}{}{}".format("'", classname,"'"), expression_type="PYTHON3", 
                                        code_block="", field_type="TEXT")


    def getBuffer(output):

        if getCount(output):
            print("{} : successful output".format(output))

            if output == outputBuilding:

                buffoutput = "buffBuilding"
                classname = "Building"

                intout = arcpy.cartography.AggregatePolygons(output, "in_memory/" + buffoutput, 
                                                             "35 Meters", "", "", 
                                                             "", "", "", 
                                                             "fclass")

                addField(intout, classname)

                mergeList.append(intout)

            if output == outputRailways:

                buffoutput = "buffRailways"
                classname = "Railway"

                intout = arcpy.Buffer_analysis(output, "in_memory/" + buffoutput, "2.5 Meters", "", 
                          "ROUND", "NONE", "", "PLANAR")

                addField(intout, classname)

                mergeList.append(intout)

            elif output == outputRoads:

                buffoutput = "buffRoads"
                classname = "Road"

                intout = arcpy.Buffer_analysis(output, "in_memory/" + buffoutput, "2.5 Meters", "", 
                          "ROUND", "NONE", "", "PLANAR")

                addField(intout, classname)

                mergeList.append(intout)

            elif output == outputWaterways:

                buffoutput = "buffWaterways"
                classname = "Waterway"

                intout = arcpy.Buffer_analysis(output, "in_memory/" + buffoutput, "2.5 Meters", "", 
                          "ROUND", "NONE", "", "PLANAR")

                addField(intout, classname)

                mergeList.append(intout)

            #print('Yes')
        elif not getCount(output):
            print("{} : empty output".format(output))
            #print("No")


    mergeList = []


    getBuffer(outputBuilding)
    getBuffer(outputRailways)
    getBuffer(outputRoads)
    getBuffer(outputWaterways)
    arcpy.management.Merge(mergeList, r".\\output\\mergedOSM.shp", "", "")
    print("done...")

    ### Erase OSM elements from Classified Image

    #**Classified image: Raster to Vector**

    arcpy.env.extent = rectangle

    # Set local variables

    inRaster = classification_output

    field = "Class_name"

    # Execute RasterToPolygon
    arcpy.RasterToPolygon_conversion(inRaster, outPolygons, "SIMPLIFY", field)


    arcpy.env.extent = "MAXOF"
    print("Done")

    #**Erase Processing**

    #vectorInput = r".\\output\\Classified_Aeg03.shp"
    vectorInput = outPolygons

    eraseElements = r".\\output\\mergedOSM.shp"
    eraseOutput = r".\\output\\erased.shp"
    arcpy.Erase_analysis(vectorInput, eraseElements, eraseOutput)

    print("Done")

    #eraseOutput = r".\\output\\erased2.shp" # DELETE later on

    arcpy.management.Merge([eraseOutput, r".\\output\\mergedOSM.shp"], r".\\output\\mergedFinal.shp", "", "")

    print("Done")

    #**Dissolve to make singleparts to multipart**<br>**This process can take a while**

    # Singlepart to multipart
    in_features = r".\\output\\mergedFinal.shp"
    #out_feature_class = r".\\output\\vectorClassification.shp"
    out_feature_class = output_feature_class

    dissolve_field = "Class_name"
    multi_part = "MULTI_PART"


    arcpy.management.Dissolve(in_features, out_feature_class, 
                              dissolve_field, "#", multi_part, "#")

    print("Done")

    ## **Statistics**

    ### Land Use Percentage&Proportion Calculation

    def addArea(fc):

        arcpy.AddField_management(fc, "Shape_area", "DOUBLE")
        arcpy.AddField_management(fc, "Area_perc", "DOUBLE")
        arcpy.AddField_management(fc, "proportion", "DOUBLE")

        summed_total = 0
        with arcpy.da.SearchCursor(fc, ["SHAPE@AREA", "Shape_area", "Area_perc"]) as cursor:
            for row in cursor:
                summed_total = summed_total + row[0]

        field_names = [f.name for f in arcpy.ListFields(fc)]
        print(field_names)

        with arcpy.da.SearchCursor(fc, ["SHAPE@AREA", "Shape_area", "Area_perc"]) as cursor:
            for row in cursor:
                #row[2] = 100*row[0]/summed_total
                a = 100*row[0]/summed_total
                print(a)


        # New version of UpdateCursor doesn't work in my personal computer; this is the old version
        cursor = arcpy.UpdateCursor(fc)
        geometryField = arcpy.Describe(fc).shapeFieldName
        for row in cursor:
            AreaValue = row.getValue(geometryField).area
            #a = row.getValue("SHAPE@AREA")
            a = AreaValue* 100 / summed_total
            b = AreaValue / summed_total
            row.setValue("Area_perc", a)
            row.setValue("proportion", b)
            cursor.updateRow(row)

        del cursor




    #fc = r".\\output\\vectorClassification.shp"  
    fc = output_feature_class
    addArea(fc)
    print("DONE!")

    ### SHDI Calculation

    #![formula.png](attachment:formula.png)

    #**where Pi = proportion of the landscape occupied by patch land cover type (class) i**


    ln = np.log


    #log10 = np.log10
    # a = ln(e*e)
    # b = log10(100)

    # print(a, ' ', b)

    # 0.076593, 0.369855, 0.086884, 0.016677, 0.140409, 0.309582

    # SHDI_test = -(0.076593 * ln(0.076593) + 0.369855 * ln(0.369855) + 0.086884 * ln(0.086884) + 
    #         0.016677 * ln(0.016677) + 0.140409 * ln(0.140409) + 0.309582 * ln(0.309582))

    # print(SHDI_test)


    SHDI_sum = []
    with arcpy.da.SearchCursor(fc, ["proportion"]) as cursor:
            for row in cursor:
                x = row[0] * ln(row[0])
                SHDI_sum.append(x)

    SHDI = sum(SHDI_sum) * -1
    print(plotNo + ':')
    print(SHDI)
    
    
    textList.append(ep)
    textList.append(SHDI)
    textList.append('---------')

    print(textList)


    

    with open(textPath, 'w') as f:
        for item in textList:
            f.write("%s\n" % item)


  
print("The code is over!")    


# In[ ]:


totaltime = time.time()- start_time

print(totaltime)

m, s = divmod(int(totaltime), 60)
h, m = divmod(m, 60)
print('{:d}:{:02d}:{:02d}'.format(h, m, s)) # Python 3
print(f'{h:d}:{m:02d}:{s:02d}') # Python 3.6+


sys.exit()


# THE CODE STOPS ABOVE
