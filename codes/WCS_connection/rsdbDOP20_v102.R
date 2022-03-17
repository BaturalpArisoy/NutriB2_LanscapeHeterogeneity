### R code for: 
#               1) WCS connection of Remote Sensing Database by Environmental Informatics at Marburg University
#               2) Automatically downloading images of selected plots in any of the three Biodiversity Exploratories

# This version of code is read only and can not be used as long as the user doesn't have necessary credentials for RSDB connection

##############################################################################################################################

#Configuration for:
# 1) Directory of exported GEOTIFF images (avoid backslash)
myDIR <- ('C:/Users/batur/OneDrive/Desktop/plots/DOP20s')

# 2) Select gpkg file:
#   a) Go and download raw from: 
#     "https://github.com/BaturalpArisoy/NutriB2_LanscapeHeterogeneity/blob/407ef79b830599a5dedc04456883b9c8bf3911c1/vectorData/plot.gpkg"
#     (Indirect access from R interface, downloads a corrupted, unreadable geo-package. Please download it directly.)
#   b) Set the directory of downloaded file below (avoid backslash)
#   [Data Source(Magdon, 2021)]
shape <- readOGR('C:/Users/batur/OneDrive/Desktop/plot.gpkg')

# 3) Study radius for each plot in meters
radius = 500



###########################################################################
#Install packages by uncommenting

#install.packages('sp')                       #Pebesma et al., 2021
#install.packages('raster')                   #PHijmans et al., 2022
#install.packages('rgdal')                    #Bivand et al., 2021 (Note that this packages will retire by the end of 2023!)
#install.packages('mapview')                  #Appelhans et al., 2021
#install.packages('geosphere')                #Hijmans et al., 2021
#install.packages('sf')                       #Pebesma et al., 2022
#install.packages('rgeos')                    #Bivand et al., 2021

#if(!require("remotes")) install.packages("remotes")                          #Woellauer et al., 2022
#remotes::install_github("environmentalinformatics-marburg/rsdb/r-package")
###########################################################################

#Call installed libraries
library(sp)
library(raster)
library(rgdal)
library(RSDB)
library(mapview)
library(geosphere)
library(sf)
library(rgeos)

#Access to documentation of RSDB library and raster database class (Author: Woellauer)
??RSDB
?RSDB::RasterDB

#Connection to RSDB services (userpwd = "*user_name:password")
remotesensing <- RSDB::RemoteSensing$new(url = "https://vhrz1078.hrz.uni-marburg.de:8201", 
                                         userpwd = "****************:*******************", ssl_verifypeer = FALSE)


##########################################################################################
#Subset of plots

#This code selects all AEG plots! Feel free to change it to either "HEG" or "SEG".
#sAEG <- shape[grep("AEG", shape$ep),] 

#Do not run if the code above is selected. Otherwise, select desired plots.
sAEG <- shape[shape$ep == "AEG12" | shape$ep == "AEG05",]
head(sAEG@data)
length(sAEG)
##########################################################################################

#Calling layers of raster database
rasterdbs <- remotesensing$rasterdbs

#Access to DOP20 satellite imagery data set
rasterdb <- remotesensing$rasterdb(name = rasterdbs$name[1])

#Start timing for the loop
start.time <- Sys.time()

#Loop for selected plots
for(i in 1:nrow(sAEG)) {
  
  #Iterate over attribute table
  p <- sAEG[i,]
  
  #Calculate centroid of the plot
  centr <- gCentroid(p, byid = TRUE)
  #Calculate latitude & longitude of centroid
  geom(centr)
  coords <- geom(centr)
  
  xcoord <- coords[1,'x']
  ycoord <- coords[1,'y']
  plotNo <- p@data$ep
  
  
  #Get BBOX extent of the plot by three parameters: 1) X coordinate, 2) Y coordinate of the weather station, 3) given radius in meters
  ext <- RSDB::extent_radius(xcoord, ycoord, radius)
  
  #Get metadata of DOP20 dataset 
  
  #result_name <- rasterdb$name
  #result_bands <- rasterdb$bands
  #result_timestamps <- rasterdb$timestamps
  #result_pixel_size <- rasterdb$pixel_size
  #result_extent <- rasterdb$extent
  #result_geo_code <- rasterdb$geo_code
  #result_proj4 <- rasterdb$proj4
  #result_description <- rasterdb$description
  
  #Get subset of DOP20 layer by specifying the bandwidth [RGB(1,2,3)] and extent
  r <- rasterdb$raster(ext = ext, band = c(1:3))
  
  
  #Visualize the raster in viewer, no RGB view (Author: Appelhans)
  #mapview::mapview(r, homebutton = FALSE)
  
  #Label for saved geoTiff image
  saveName <- paste(plotNo, '.tif')
  
  
  ###############################################################################################
  #Writing the RGB raster (please refer to .tif file extensions)
  
  # Write to an integer binary file
  #rf <- writeRaster(r, filename=file.path(myDIR, "allint.grd"), datatype='INT4S', overwrite=TRUE)
  
  # Make a brick and save multi-layer file
  #b <- brick(r, sqrt(r))
  #bf <- writeRaster(b, filename=file.path(myDIR, "multi.grd"), bandorder='BIL', overwrite=TRUE)
  
  # Write to a new geotiff file (depends on rgdal)
  
  if (require(rgdal)) {
    rf <- writeRaster(r, filename=file.path(myDIR, saveName), format="GTiff", overwrite=TRUE)
  }
  ###############################################################################################
  
  
  #Track the progress of loop
  cat(i, plotNo, xcoord, ycoord, "\n")
}

end.time <- Sys.time()
time.taken <- end.time - start.time

cat(" *************","\n", "\n", "Process done!", "\n", "\n", "*************", "\n", "\n")

time.taken


