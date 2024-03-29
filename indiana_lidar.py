# -*- coding: utf-8 -*-
"""
/***************************************************************************
 IndianaLidar
                                 A QGIS plugin
 This plugin helps you access Indiana LiDAR data products.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2023-02-02
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Jinha Jung
        email                : jinha@purdue.edu
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsRasterLayer, QgsProject

# Initialize Qt resources from file resources.py
from .resources import *

# Import the code for the dialog
from .indiana_lidar_dialog import IndianaLidarDialog
import os.path


class IndianaLidar:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        locale_path = os.path.join(self.plugin_dir, "i18n", "IndianaLidar_{}.qm".format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr("&Indiana LiDAR")

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None
        self.county_names = [
            "adams",
            "allen",
            "bartholomew",
            "benton",
            "blackford",
            "boone",
            "brown",
            "carroll",
            "cass",
            "clark",
            "clay",
            "clinton",
            "crawford",
            "daviess",
            "dearborn",
            "decatur",
            "dekalb",
            "delaware",
            "dubois",
            "elkhart",
            "fayette",
            "floyd",
            "fountain",
            "franklin",
            "fulton",
            "gibson",
            "grant",
            "greene",
            "hamilton",
            "hancock",
            "harrison",
            "hendricks",
            "henry",
            "howard",
            "huntington",
            "jackson",
            "jasper",
            "jay",
            "jefferson",
            "jennings",
            "johnson",
            "knox",
            "kosciusko",
            "lagrange",
            "lake",
            "laporte",
            "lawrence",
            "madison",
            "marion",
            "marshall",
            "martin",
            "miami",
            "monroe",
            "montgomery",
            "morgan",
            "newton",
            "noble",
            "ohio",
            "orange",
            "owen",
            "parke",
            "perry",
            "pike",
            "porter",
            "posey",
            "pulaski",
            "putnam",
            "randolph",
            "ripley",
            "rush",
            "scott",
            "shelby",
            "spencer",
            "starke",
            "steuben",
            "stjoseph",
            "sullivan",
            "switzerland",
            "tippecanoe",
            "tipton",
            "union",
            "vanderburgh",
            "vermillion",
            "vigo",
            "wabash",
            "warren",
            "warrick",
            "washington",
            "wayne",
            "wells",
            "white",
            "whitley",
        ]
        self.dtm_dir = "https://lidar.digitalforestry.org/QL2_3DEP_LiDAR_IN_2017_2019/3DEP_County_DEM_Mosaics/cog/"
        self.l2_dir = "https://lidar.digitalforestry.org/QL2_3DEP_LiDAR_IN_2017_2019_l2/"
        self.dtm_dictionary = {
            "adams": "Adams_dem_2017_stple.tif",
            "allen": "Allen_dem_2017_stple.tif",
            "bartholomew": "Bartholomew_dem_2017_stple.tif",
            "benton": "Benton_Co_dem_2018_stplw.tif",
            "blackford": "Blackford_dem_2017_stple.tif",
            "boone": "Boone_Co_dem_2018_stplw.tif",
            "brown": "Brown_dem_2017_stple.tif",
            "carroll": "Carroll_Co_dem_2018_stplw.tif",
            "cass": "Cass_dem_2017_stple.tif",
            "clark": "Clark_Co_dem_2017_stple.tif",
            "clay": "Clay_Co_dem_2018_stplw.tif",
            "clinton": "Clinton_Co_dem_2018_stplw.tif",
            "crawford": "Crawford_Co_dem_2018_stplw.tif",
            "daviess": "Daviess_Co_dem_2018_stplw.tif",
            "dearborn": "Dearborn_dem_2017_stple.tif",
            "decatur": "Decatur_dem_2017_stple.tif",
            "dekalb": "DeKalb_dem_2017_stple.tif",
            "delaware": "Delaware_dem_2017_stple.tif",
            "dubois": "Dubois_Co_dem_2018_stplw.tif",
            "elkhart": "Elkhart_dem_2017_stple.tif",
            "fayette": "Fayette_dem_2017_stple.tif",
            "floyd": "Floyd_Co_dem_2017_stple.tif",
            "fountain": "Fountain_Co_dem_2018_stplw.tif",
            "franklin": "Franklin_dem_2017_stple.tif",
            "fulton": "Fulton_dem_2017_stple.tif",
            "gibson": "Gibson_Co_dem_2018_stplw.tif",
            "grant": "Grant_dem_2017_stple.tif",
            "greene": "Greene_Co_dem_2018_stplw.tif",
            "hamilton": "Hamilton_Co_dem_2016_stple.tif",
            "hancock": "Hancock_dem_2017_stple.tif",
            "harrison": "Harrison_Co_dem_2017_stple.tif",
            "hendricks": "Hendricks_Co_dem_2018_stplw.tif",
            "henry": "Henry_dem_2017_stple.tif",
            "howard": "Howard_dem_2017_stple.tif",
            "huntington": "Huntington_dem_2017_stple.tif",
            "jackson": "Jackson_Co_dem_2017_stple.tif",
            "jasper": "Jasper_Co_dem_2018_stplw.tif",
            "jay": "Jay_dem_2017_stple.tif",
            "jefferson": "Jefferson_Co_dem_2017_stple.tif",
            "jennings": "Jennings_Co_dem_2017_stple.tif",
            "johnson": "Johnson_dem_2017_stple.tif",
            "knox": "Knox_Co_dem_2018_stplw.tif",
            "kosciusko": "Kosciusko_dem_2017_stple.tif",
            "lagrange": "LaGrange_dem_2017_stple.tif",
            "lake": "Lake_Co_dem_2018_stplw.tif",
            "laporte": "LaPorte_Co_dem_2018_stplw.tif",
            "lawrence": "Lawrence_Co_dem_2018_stplw.tif",
            "madison": "Madison_dem_2017_stple.tif",
            "marion": "Marion_dem_2016_stple.tif",
            "marshall": "Marshall_dem_2017_stple.tif",
            "martin": "Martin_Co_dem_2018_stplw.tif",
            "miami": "Miami_dem_2017_stple.tif",
            "monroe": "Monroe_Co_dem_2018_stplw.tif",
            "montgomery": "Montgomery_Co_dem_2018_stplw.tif",
            "morgan": "Morgan_Co_dem_2018_stplw.tif",
            "newton": "Newton_Co_dem_2018_stplw.tif",
            "noble": "Noble_dem_2017_stple.tif",
            "ohio": "Ohio_dem_2017_stple.tif",
            "orange": "Orange_Co_dem_2018_stplw.tif",
            "owen": "Owen_Co_dem_2018_stplw.tif",
            "parke": "Parke_Co_dem_2018_stplw.tif",
            "perry": "Perry_Co_dem_2018_stplw.tif",
            "pike": "Pike_Co_dem_2018_stplw.tif",
            "porter": "Porter_Co_dem_2018_stplw.tif",
            "posey": "Posey_Co_dem_2020_stplw.tif",
            "pulaski": "Pulaski_Co_dem_2018_stplw.tif",
            "putnam": "Putnam_Co_dem_2018_stplw.tif",
            "randolph": "Randolph_dem_2017_stple.tif",
            "ripley": "Ripley_dem_2017_stple.tif",
            "rush": "Rush_dem_2017_stple.tif",
            "scott": "Scott_Co_dem_2017_stple.tif",
            "shelby": "Shelby_dem_2017_stple.tif",
            "spencer": "Spencer_Co_dem_2018_stplw.tif",
            "starke": "Starke_Co_dem_2018_stplw.tif",
            "steuben": "Steuben_dem_2017_stple.tif",
            "stjoseph": "StJoseph_dem_2017_stple.tif",
            "sullivan": "Sullivan_Co_dem_2018_stplw.tif",
            "switzerland": "Switzerland_Co_dem_2017_stple.tif",
            "tippecanoe": "Tippecanoe_Co_dem_2018_stplw.tif",
            "tipton": "Tipton_dem_2017_stple.tif",
            "union": "Union_dem_2017_stple.tif",
            "vanderburgh": "Vanderburgh_Co_dem_2020_stplw.tif",
            "vermillion": "Vermillion_Co_dem_2018_stplw.tif",
            "vigo": "Vigo_Co_dem_2018_stplw.tif",
            "wabash": "Wabash_dem_2017_stple.tif",
            "warren": "Warren_Co_dem_2018_stplw.tif",
            "warrick": "Warrick_Co_dem_2020_stplw.tif",
            "washington": "Washington_Co_dem_2017_stple.tif",
            "wayne": "Wayne_Co_dem_2017_stple.tif",
            "wells": "Wells_dem_2017_stple.tif",
            "white": "White_Co_dem_2018_stplw.tif",
            "whitley": "Whitley_dem_2017_stple.tif",
        }
        self.ndhm_dictionary = {
            "adams": "adams_ndhm_2017.tif",
            "allen": "allen_ndhm_2017.tif",
            "bartholomew": "bartholomew_ndhm_2017.tif",
            "benton": "benton_ndhm_2018.tif",
            "blackford": "blackford_ndhm_2017.tif",
            "boone": "boone_ndhm_2018.tif",
            "brown": "brown_ndhm_2017.tif",
            "carroll": "carroll_ndhm_2018.tif",
            "cass": "cass_ndhm_2017.tif",
            "clark": "clark_ndhm_2017.tif",
            "clay": "clay_ndhm_2018.tif",
            "clinton": "clinton_ndhm_2018.tif",
            "crawford": "crawford_ndhm_2018.tif",
            "daviess": "daviess_ndhm_2018.tif",
            "dearborn": "dearborn_ndhm_2017.tif",
            "decatur": "decatur_ndhm_2017.tif",
            "dekalb": "dekalb_ndhm_2017.tif",
            "delaware": "delaware_ndhm_2017.tif",
            "dubois": "dubois_ndhm_2018.tif",
            "elkhart": "elkhart_ndhm_2017.tif",
            "fayette": "fayette_ndhm_2017.tif",
            "floyd": "floyd_ndhm_2017.tif",
            "fountain": "fountain_ndhm_2018.tif",
            "franklin": "franklin_ndhm_2017.tif",
            "fulton": "fulton_ndhm_2017.tif",
            "gibson": "gibson_ndhm_2018.tif",
            "grant": "grant_ndhm_2017.tif",
            "greene": "greene_ndhm_2018.tif",
            "hamilton": "hamilton_ndhm_2016.tif",
            "hancock": "hancock_ndhm_2017.tif",
            "harrison": "harrison_ndhm_2017.tif",
            "hendricks": "hendricks_ndhm_2018.tif",
            "henry": "henry_ndhm_2017.tif",
            "howard": "howard_ndhm_2017.tif",
            "huntington": "huntington_ndhm_2017.tif",
            "jackson": "jackson_ndhm_2017.tif",
            "jasper": "jasper_ndhm_2018.tif",
            "jay": "jay_ndhm_2017.tif",
            "jefferson": "jefferson_ndhm_2017.tif",
            "jennings": "jennings_ndhm_2017.tif",
            "johnson": "johnson_ndhm_2017.tif",
            "knox": "knox_ndhm_2018.tif",
            "kosciusko": "kosciusko_ndhm_2017.tif",
            "lagrange": "lagrange_ndhm_2017.tif",
            "lake": "lake_ndhm_2018.tif",
            "laporte": "laporte_ndhm_2018.tif",
            "lawrence": "lawrence_ndhm_2018.tif",
            "madison": "madison_ndhm_2017.tif",
            "marion": "marion_ndhm_2016.tif",
            "marshall": "marshall_ndhm_2017.tif",
            "martin": "martin_ndhm_2018.tif",
            "miami": "miami_ndhm_2017.tif",
            "monroe": "monroe_ndhm_2018.tif",
            "montgomery": "montgomery_ndhm_2018.tif",
            "morgan": "morgan_ndhm_2018.tif",
            "newton": "newton_ndhm_2018.tif",
            "noble": "noble_ndhm_2017.tif",
            "ohio": "ohio_ndhm_2017.tif",
            "orange": "orange_ndhm_2018.tif",
            "owen": "owen_ndhm_2018.tif",
            "parke": "parke_ndhm_2018.tif",
            "perry": "perry_ndhm_2018.tif",
            "pike": "pike_ndhm_2018.tif",
            "porter": "porter_ndhm_2018.tif",
            "posey": "posey_ndhm_2020.tif",
            "pulaski": "pulaski_ndhm_2018.tif",
            "putnam": "putnam_ndhm_2018.tif",
            "randolph": "randolph_ndhm_2017.tif",
            "ripley": "ripley_ndhm_2017.tif",
            "rush": "rush_ndhm_2017.tif",
            "scott": "scott_ndhm_2017.tif",
            "shelby": "shelby_ndhm_2017.tif",
            "spencer": "spencer_ndhm_2018.tif",
            "starke": "starke_ndhm_2018.tif",
            "steuben": "steuben_ndhm_2017.tif",
            "stjoseph": "stjoseph_ndhm_2017.tif",
            "sullivan": "sullivan_ndhm_2018.tif",
            "switzerland": "switzerland_ndhm_2017.tif",
            "tippecanoe": "tippecanoe_ndhm_2018.tif",
            "tipton": "tipton_ndhm_2017.tif",
            "union": "union_ndhm_2017.tif",
            "vanderburgh": "vanderburgh_ndhm_2020.tif",
            "vermillion": "vermillion_ndhm_2018.tif",
            "vigo": "vigo_ndhm_2018.tif",
            "wabash": "wabash_ndhm_2017.tif",
            "warren": "warren_ndhm_2018.tif",
            "warrick": "warrick_ndhm_2020.tif",
            "washington": "washington_ndhm_2017.tif",
            "wayne": "wayne_ndhm_2017.tif",
            "wells": "wells_ndhm_2017.tif",
            "white": "white_ndhm_2018.tif",
            "whitley": "whitley_ndhm_2017.tif",
        }
        self.dsm_dictionary = {
            "adams": "adams_dsm_2017.tif",
            "allen": "allen_dsm_2017.tif",
            "bartholomew": "bartholomew_dsm_2017.tif",
            "benton": "benton_dsm_2018.tif",
            "blackford": "blackford_dsm_2017.tif",
            "boone": "boone_dsm_2018.tif",
            "brown": "brown_dsm_2017.tif",
            "carroll": "carroll_dsm_2018.tif",
            "cass": "cass_dsm_2017.tif",
            "clark": "clark_dsm_2017.tif",
            "clay": "clay_dsm_2018.tif",
            "clinton": "clinton_dsm_2018.tif",
            "crawford": "crawford_dsm_2018.tif",
            "daviess": "daviess_dsm_2018.tif",
            "dearborn": "dearborn_dsm_2017.tif",
            "decatur": "decatur_dsm_2017.tif",
            "dekalb": "dekalb_dsm_2017.tif",
            "delaware": "delaware_dsm_2017.tif",
            "dubois": "dubois_dsm_2018.tif",
            "elkhart": "elkhart_dsm_2017.tif",
            "fayette": "fayette_dsm_2017.tif",
            "floyd": "floyd_dsm_2017.tif",
            "fountain": "fountain_dsm_2018.tif",
            "franklin": "franklin_dsm_2017.tif",
            "fulton": "fulton_dsm_2017.tif",
            "gibson": "gibson_dsm_2018.tif",
            "grant": "grant_dsm_2017.tif",
            "greene": "greene_dsm_2018.tif",
            "hamilton": "hamilton_dsm_2016.tif",
            "hancock": "hancock_dsm_2017.tif",
            "harrison": "harrison_dsm_2017.tif",
            "hendricks": "hendricks_dsm_2018.tif",
            "henry": "henry_dsm_2017.tif",
            "howard": "howard_dsm_2017.tif",
            "huntington": "huntington_dsm_2017.tif",
            "jackson": "jackson_dsm_2017.tif",
            "jasper": "jasper_dsm_2018.tif",
            "jay": "jay_dsm_2017.tif",
            "jefferson": "jefferson_dsm_2017.tif",
            "jennings": "jennings_dsm_2017.tif",
            "johnson": "johnson_dsm_2017.tif",
            "knox": "knox_dsm_2018.tif",
            "kosciusko": "kosciusko_dsm_2017.tif",
            "lagrange": "lagrange_dsm_2017.tif",
            "lake": "lake_dsm_2018.tif",
            "laporte": "laporte_dsm_2018.tif",
            "lawrence": "lawrence_dsm_2018.tif",
            "madison": "madison_dsm_2017.tif",
            "marion": "marion_dsm_2016.tif",
            "marshall": "marshall_dsm_2017.tif",
            "martin": "martin_dsm_2018.tif",
            "miami": "miami_dsm_2017.tif",
            "monroe": "monroe_dsm_2018.tif",
            "montgomery": "montgomery_dsm_2018.tif",
            "morgan": "morgan_dsm_2018.tif",
            "newton": "newton_dsm_2018.tif",
            "noble": "noble_dsm_2017.tif",
            "ohio": "ohio_dsm_2017.tif",
            "orange": "orange_dsm_2018.tif",
            "owen": "owen_dsm_2018.tif",
            "parke": "parke_dsm_2018.tif",
            "perry": "perry_dsm_2018.tif",
            "pike": "pike_dsm_2018.tif",
            "porter": "porter_dsm_2018.tif",
            "posey": "posey_dsm_2020.tif",
            "pulaski": "pulaski_dsm_2018.tif",
            "putnam": "putnam_dsm_2018.tif",
            "randolph": "randolph_dsm_2017.tif",
            "ripley": "ripley_dsm_2017.tif",
            "rush": "rush_dsm_2017.tif",
            "scott": "scott_dsm_2017.tif",
            "shelby": "shelby_dsm_2017.tif",
            "spencer": "spencer_dsm_2018.tif",
            "starke": "starke_dsm_2018.tif",
            "steuben": "steuben_dsm_2017.tif",
            "stjoseph": "stjoseph_dsm_2017.tif",
            "sullivan": "sullivan_dsm_2018.tif",
            "switzerland": "switzerland_dsm_2017.tif",
            "tippecanoe": "tippecanoe_dsm_2018.tif",
            "tipton": "tipton_dsm_2017.tif",
            "union": "union_dsm_2017.tif",
            "vanderburgh": "vanderburgh_dsm_2020.tif",
            "vermillion": "vermillion_dsm_2018.tif",
            "vigo": "vigo_dsm_2018.tif",
            "wabash": "wabash_dsm_2017.tif",
            "warren": "warren_dsm_2018.tif",
            "warrick": "warrick_dsm_2020.tif",
            "washington": "washington_dsm_2017.tif",
            "wayne": "wayne_dsm_2017.tif",
            "wells": "wells_dsm_2017.tif",
            "white": "white_dsm_2018.tif",
            "whitley": "whitley_dsm_2017.tif",
        }
        
        self.dtm_hs_dictionary = {
            "adams": "adams_dtm_hs_2017.tif",
            "allen": "allen_dtm_hs_2017.tif",
            "bartholomew": "bartholomew_dtm_hs_2017.tif",
            "benton": "benton_dtm_hs_2018.tif",
            "blackford": "blackford_dtm_hs_2017.tif",
            "boone": "boone_dtm_hs_2018.tif",
            "brown": "brown_dtm_hs_2017.tif",
            "carroll": "carroll_dtm_hs_2018.tif",
            "cass": "cass_dtm_hs_2017.tif",
            "clark": "clark_dtm_hs_2017.tif",
            "clay": "clay_dtm_hs_2018.tif",
            "clinton": "clinton_dtm_hs_2018.tif",
            "crawford": "crawford_dtm_hs_2018.tif",
            "daviess": "daviess_dtm_hs_2018.tif",
            "dearborn": "dearborn_dtm_hs_2017.tif",
            "decatur": "decatur_dtm_hs_2017.tif",
            "dekalb": "dekalb_dtm_hs_2017.tif",
            "delaware": "delaware_dtm_hs_2017.tif",
            "dubois": "dubois_dtm_hs_2018.tif",
            "elkhart": "elkhart_dtm_hs_2017.tif",
            "fayette": "fayette_dtm_hs_2017.tif",
            "floyd": "floyd_dtm_hs_2017.tif",
            "fountain": "fountain_dtm_hs_2018.tif",
            "franklin": "franklin_dtm_hs_2017.tif",
            "fulton": "fulton_dtm_hs_2017.tif",
            "gibson": "gibson_dtm_hs_2018.tif",
            "grant": "grant_dtm_hs_2017.tif",
            "greene": "greene_dtm_hs_2018.tif",
            "hamilton": "hamilton_dtm_hs_2016.tif",
            "hancock": "hancock_dtm_hs_2017.tif",
            "harrison": "harrison_dtm_hs_2017.tif",
            "hendricks": "hendricks_dtm_hs_2018.tif",
            "henry": "henry_dtm_hs_2017.tif",
            "howard": "howard_dtm_hs_2017.tif",
            "huntington": "huntington_dtm_hs_2017.tif",
            "jackson": "jackson_dtm_hs_2017.tif",
            "jasper": "jasper_dtm_hs_2018.tif",
            "jay": "jay_dtm_hs_2017.tif",
            "jefferson": "jefferson_dtm_hs_2017.tif",
            "jennings": "jennings_dtm_hs_2017.tif",
            "johnson": "johnson_dtm_hs_2017.tif",
            "knox": "knox_dtm_hs_2018.tif",
            "kosciusko": "kosciusko_dtm_hs_2017.tif",
            "lagrange": "lagrange_dtm_hs_2017.tif",
            "lake": "lake_dtm_hs_2018.tif",
            "laporte": "laporte_dtm_hs_2018.tif",
            "lawrence": "lawrence_dtm_hs_2018.tif",
            "madison": "madison_dtm_hs_2017.tif",
            "marion": "marion_dtm_hs_2016.tif",
            "marshall": "marshall_dtm_hs_2017.tif",
            "martin": "martin_dtm_hs_2018.tif",
            "miami": "miami_dtm_hs_2017.tif",
            "monroe": "monroe_dtm_hs_2018.tif",
            "montgomery": "montgomery_dtm_hs_2018.tif",
            "morgan": "morgan_dtm_hs_2018.tif",
            "newton": "newton_dtm_hs_2018.tif",
            "noble": "noble_dtm_hs_2017.tif",
            "ohio": "ohio_dtm_hs_2017.tif",
            "orange": "orange_dtm_hs_2018.tif",
            "owen": "owen_dtm_hs_2018.tif",
            "parke": "parke_dtm_hs_2018.tif",
            "perry": "perry_dtm_hs_2018.tif",
            "pike": "pike_dtm_hs_2018.tif",
            "porter": "porter_dtm_hs_2018.tif",
            "posey": "posey_dtm_hs_2020.tif",
            "pulaski": "pulaski_dtm_hs_2018.tif",
            "putnam": "putnam_dtm_hs_2018.tif",
            "randolph": "randolph_dtm_hs_2017.tif",
            "ripley": "ripley_dtm_hs_2017.tif",
            "rush": "rush_dtm_hs_2017.tif",
            "scott": "scott_dtm_hs_2017.tif",
            "shelby": "shelby_dtm_hs_2017.tif",
            "spencer": "spencer_dtm_hs_2018.tif",
            "starke": "starke_dtm_hs_2018.tif",
            "steuben": "steuben_dtm_hs_2017.tif",
            "stjoseph": "stjoseph_dtm_hs_2017.tif",
            "sullivan": "sullivan_dtm_hs_2018.tif",
            "switzerland": "switzerland_dtm_hs_2017.tif",
            "tippecanoe": "tippecanoe_dtm_hs_2018.tif",
            "tipton": "tipton_dtm_hs_2017.tif",
            "union": "union_dtm_hs_2017.tif",
            "vanderburgh": "vanderburgh_dtm_hs_2020.tif",
            "vermillion": "vermillion_dtm_hs_2018.tif",
            "vigo": "vigo_dtm_hs_2018.tif",
            "wabash": "wabash_dtm_hs_2017.tif",
            "warren": "warren_dtm_hs_2018.tif",
            "warrick": "warrick_dtm_hs_2020.tif",
            "washington": "washington_dtm_hs_2017.tif",
            "wayne": "wayne_dtm_hs_2017.tif",
            "wells": "wells_dtm_hs_2017.tif",
            "white": "white_dtm_hs_2018.tif",
            "whitley": "whitley_dtm_hs_2017.tif",
        }

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate("IndianaLidar", message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None,
    ):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ":/plugins/indiana_lidar/icon.png"
        self.add_action(icon_path, text=self.tr("Indiana LiDAR"), callback=self.run, parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(self.tr("&Indiana LiDAR"), action)
            self.iface.removeToolBarIcon(action)

    def generate_cog_url(self):
        selected_data_product = self.dlg.comboBox_data_products.currentText()
        selected_county_name = self.dlg.comboBox_county.currentText()

        print(f"Selected data product = {selected_data_product}")
        print(f"Selected county = {selected_county_name}")

        if selected_data_product == "DTM":
            cog_url = self.dtm_dir + self.dtm_dictionary[selected_county_name]
        elif selected_data_product == "DSM":
            cog_url = self.l2_dir + selected_county_name + "/cog/" + self.dsm_dictionary[selected_county_name]
        elif selected_data_product == "NDHM":
            cog_url = self.l2_dir + selected_county_name + "/cog/" + self.ndhm_dictionary[selected_county_name]
        elif selected_data_product == "DTM Hillshade":
            cog_url = self.l2_dir + selected_county_name + "/cog/" + self.dtm_hs_dictionary[selected_county_name]
        self.dlg.textEdit_cog_url.setText(cog_url)

    def add_to_map(self):
        cog_url = self.dlg.textEdit_cog_url.toPlainText()
        selected_data_products = self.dlg.comboBox_data_products.currentText()
        selected_county_name = self.dlg.comboBox_county.currentText()
        rlayer = QgsRasterLayer(
            "/vsicurl/" + cog_url, "Indiana_" + selected_county_name + "_county_" + selected_data_products
        )
        if rlayer.isValid():
            QgsProject().instance().addMapLayer(rlayer)
        else:
            print("Not valid.")

        # Now zoom to the added layer
        self.iface.zoomToActiveLayer()
        self.iface.mapCanvas().refresh()

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = IndianaLidarDialog()
            # Initialize combo boxes
            self.dlg.comboBox_data_products.clear()
            self.dlg.comboBox_county.clear()
            self.dlg.comboBox_data_products.addItems(["DTM", "DSM", "NDHM", "DTM Hillshade"])
            self.dlg.comboBox_county.addItems(self.county_names)
            # Event handlers
            self.dlg.pushButton_add.clicked.connect(self.add_to_map)
            self.dlg.comboBox_county.currentIndexChanged.connect(self.generate_cog_url)
            self.dlg.comboBox_data_products.currentIndexChanged.connect(self.generate_cog_url)
            self.generate_cog_url()

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
