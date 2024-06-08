# -*- coding: utf-8 -*-
"""
/***************************************************************************
 wtyczkaoaDialog
                                 A QGIS plugin
 Wtyczka służy do przetwarzania i analizy danych geoprzestrzennych bezpośrednio w QGIS. Oferuje następujące funkcjonalności: Obliczanie różnicy wysokości oraz obliczanie pola powierzchni metodą Gaussa
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2024-06-08
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Oliwia Zubrzycka, Alicja Wiatr
        email                : 01179242@pw.edu.pl
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

import os
from math import atan2, sqrt, pi
from qgis.utils import iface

from qgis.PyQt import QtWidgets, uic
from qgis.core import QgsField, QgsFeature, QgsGeometry, QgsVectorLayer, QgsPointXY, QgsProject, QgsCoordinateReferenceSystem, QgsFields
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'wtyczkaoa_dialog_base.ui'))


class wtyczkaoaDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(wtyczkaoaDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.height_difference.clicked.connect(self.height_difference_function)
        self.count_points.clicked.connect(self.count_elements)
        self.display_coordinates.clicked.connect(self.coordinates_function)
        self.area.clicked.connect(self.area_function)
        self.clear_table.clicked.connect(self.clear_array_function)
        self.close_button.clicked.connect(self.clear_data_function)
        self.azimuth.clicked.connect(self.azimuth_function)
        self.segment_length.clicked.connect(self.segment_length_function)
        self.reset_all.clicked.connect(self.clear_data_function)
        self.save_file.clicked.connect(self.save_file_function)
        self.reverse_azimuth.clicked.connect(self.azimuth_function)
        self.load_file.clicked.connect(self.select_file_function)
        
    def show_error_message(self, error_message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setText(error_message)
        error_dialog.setWindowTitle("Error")
        error_dialog.exec_()

    def segment_length_function(self):
        num_elements = len(self.mMapLayerComboBox_layers.currentLayer().selectedFeatures())
        if num_elements == 2:
            selected_features = self.mMapLayerComboBox_layers.currentLayer().selectedFeatures() 
            points = [[feature.geometry().asPoint().x(), feature.geometry().asPoint().y()] for feature in selected_features]
            distance = sqrt((points[0][0] - points[1][0])**2 + (points[0][1] - points[1][1])**2)
            self.segment_length_result.setText(f'Distance between points (point id:1- id:2) is: {distance:.3f} [m]')
        else:
            self.show_error_message("Error: Incorrect number of points selected")
                
    def calculate_azimuth(self):
        num_elements = len(self.selected_features())
        if num_elements == 2:
            coords = self.extract_coordinates(self.selected_features())
            azimuth = atan2((coords[1][1] - coords[0][1]), (coords[1][0] - coords[0][0]))
            azimuth, reverse_azimuth = self.convert_azimuth_units(azimuth)
            self.azimuth_result.setText(f'Azimuth is (point id:1- id:2): {azimuth}')
            self.reverse_azimuth_result.setText(f'Reverse azimuth is (point id:2- id:1): {reverse_azimuth}')
        else:
            self.show_error_message("Error: Incorrect number of points selected")
            
    def azimuth_function(self):
        num_elements = len(self.mMapLayerComboBox_layers.currentLayer().selectedFeatures())
        if num_elements == 2:
            selected_features = self.mMapLayerComboBox_layers.currentLayer().selectedFeatures() 
            K=[]
            for element in selected_features:
                wsp = element.geometry().asPoint()
                X = wsp.x()
                Y = wsp.y()
                K.append([X, Y])
            Az = atan2((K[1][1]-K[0][1]), (K[1][0]-K[0][0]))
            if 'decimal_degrees' == self.unit_azimuth.currentText():
                Az =Az*180/pi
                if Az < 0:
                    Az += 360
                elif Az > 360:
                    Az -= 360
                self.azimuth_result.setText(f'Azimuth is (point id:1- id:2): {Az:.7f}[decimal_degrees]')
                Az_odw = Az+180
                if Az_odw < 0:
                    Az_odw += 360
                elif Az_odw > 360:
                    Az_odw -= 360
                self.reverse_azimuth_result.setText(f'Reverse azimuth is (point id:2- id:1): {Az_odw:.7f}[decimal_degrees]')
            elif 'grads' == self.unit_azimuth.currentText():
                Az =Az*200/pi
                if Az < 0:
                    Az += 400
                elif Az > 400:
                    Az -= 400
                self.azimuth_result.setText(f'Azimuth is (point id:1- id:2): {Az:.4f}[grads]')
                Az_odw = Az+200
                if Az_odw < 0:
                    Az_odw += 400
                elif Az_odw > 400:
                    Az_odw -= 400
                self.reverse_azimuth_result.setText(f'Reverse azimuth is (point id:2- id:1): {Az_odw:.4f}[grads]')
        else:
            self.show_error_message("Error: Incorrect number of points selected")

    def count_elements(self):
        num_elements = len(self.mMapLayerComboBox_layers.currentLayer().selectedFeatures())
        self.show_point_count.setText(str(num_elements))

    def coordinates_function(self):
        selected_features = self.mMapLayerComboBox_layers.currentLayer().selectedFeatures()
        coords = []
        point_id = 0
        for feature in selected_features:
            wsp = feature.geometry().asPoint()
            X = wsp.x()
            Y = wsp.y()
            coords.append([X, Y])
            point_id += 1
            self.coordinates.append(f'Coordinates of point {point_id}: X = {X:.3f}, Y = {Y:.3f}')

    def height_difference_function(self):
        num_elements = len(self.mMapLayerComboBox_layers.currentLayer().selectedFeatures())
        heights = []
        if num_elements == 2: 
            selected_layer = iface.activeLayer()
            selected_features = selected_layer.selectedFeatures()
            for feature in selected_features:
                heights.append(feature[2])
            height_difference = heights[1] - heights[0]
            self.height_difference_result.setText(f'Height difference is (point id:1- id:2): {height_difference:.3f}[m]')
        elif num_elements < 2:
            self.height_difference_result.setText("Error")
            self.show_error_message("Too few points selected")
        elif num_elements > 2:
            self.height_difference_result.setText("Error")
            self.show_error_message("Too many points selected") 


            
            
    def area_function(self):
        num_elements = len(self.mMapLayerComboBox_layers.currentLayer().selectedFeatures())
        if num_elements >= 3:
            selected_features = self.mMapLayerComboBox_layers.currentLayer().selectedFeatures()
            points = []
            for feature in selected_features:
                point = feature.geometry().asPoint()
                points.append([point.x(), point.y()])
            points = self.sort_points(points)
            area_sum = 0
            for i in range(len(points)):
                if i < len(points) - 1:
                    P = (points[i][0] * (points[i + 1][1] - points[i - 1][1]))
                    area_sum += P
            P = (points[-1][0] * (points[0][1] - points[-2][1]))
            area_sum += P
            area_sum = 0.5 * abs(area_sum)
        
            if 'square_meters' == self.area_unit.currentText():
                self.surface_area_result.setText(f'Surface area is: {area_sum:.3f} [m^2]')
            elif 'ares' == self.area_unit.currentText():
                area_sum = area_sum / 100
                self.surface_area_result.setText(f'Surface area is: {area_sum:.3f} [a]')
            elif 'hectares' == self.area_unit.currentText():
                area_sum = area_sum / 10000
                self.surface_area_result.setText(f'Surface area is: {area_sum:.5f} [ha]')
        
            if 'Yes' == self.polygon_selection.currentText():
                polygon_layer = QgsVectorLayer('Polygon?crs=EPSG:2180', 'calculated_polygon_area', 'memory')
                polygon_layer.startEditing()
                
                field = QgsField("Area", QVariant.Double)
                polygon_layer.addAttribute(field)
                
                polygon_geom = QgsGeometry.fromPolygonXY([[QgsPointXY(point[0], point[1]) for point in points]])
                polygon_area = polygon_geom.area()
                attributes = [polygon_area]
                
                feature = QgsFeature()
                feature.setGeometry(polygon_geom)
                feature.setAttributes(attributes)
                polygon_layer.addFeature(feature)
                
                polygon_layer.commitChanges()
                polygon_layer.updateExtents()
                QgsProject.instance().addMapLayer(polygon_layer)
            
        elif num_elements < 3:
            self.surface_area_result.setText("Error")
            self.show_error_message("Too few points selected")

            
    def clear_array_function(self):
        self.coordinates.clear()
        
    def clear_data_function(self):
        self.coordinates.clear()
        self.surface_area_result.clear()
        self.height_difference_result.clear()
        self.show_point_count.clear()
        self.reverse_azimuth_result.clear()
        self.azimuth_result.clear()
        self.segment_length_result.clear()
    
    
    def select_file_function(self):
        path = self.file_selection.filePath()
        coordinates = []
        with open(path, 'r') as file:
            for line in file:
                line = line.strip()
                separated = line.split(";")
                x = float(separated[0])
                y = float(separated[1])
                z = float(separated[2])
                coordinates.append([x, y, z])
        layer_name = 'Loaded points'
        crs = QgsCoordinateReferenceSystem('EPSG:2180')
        layer = QgsVectorLayer('Point?crs=' + crs.authid(), layer_name, 'memory')
        provider = layer.dataProvider()
        provider.addAttributes([QgsField('X', QVariant.Double),
                            QgsField('Y', QVariant.Double),
                            QgsField('Z', QVariant.Double)])
        layer.updateFields()
        features = []
        for coordinate in coordinates:
            point = QgsPointXY(coordinate[0], coordinate[1])
            feature = QgsFeature()
            feature.setGeometry(QgsGeometry.fromPointXY(point))
            feature.setAttributes([coordinate[0], coordinate[1], coordinate[2]])
            features.append(feature)
        provider.addFeatures(features)
        layer.updateExtents()
        QgsProject.instance().addMapLayer(layer)
        project = QgsProject.instance()
        layer_name = "Loaded points"
        while len(project.mapLayersByName(layer_name)) > 1:
            project.removeMapLayer(project.mapLayersByName(layer_name)[0])
        
    def save_file_function(self):
        with open("Result_File_Plugin_Alicja_Oliwia.txt", "w") as file:
            selected_features = self.mMapLayerComboBox_layers.currentLayer().selectedFeatures()
            num_points = len(selected_features)
            file.write(f'Number of selected points: {num_points}\n')
            coordinates = []
            iden = 0
            for feature in selected_features:
                wsp = feature.geometry().asPoint()
                X = wsp.x()
                Y = wsp.y()
                coordinates.append([X, Y])
                iden += 1
                file.write(f"Coordinates of point number {iden}: X = {X:.3f}, Y = {Y:.3f}\n")
        
            num_elements = len(self.mMapLayerComboBox_layers.currentLayer().selectedFeatures())
            if num_elements == 2:
                distance = self.segment_length_function()
                file.write(f'Distance between points (point id:1- id:2) is: {distance:.3f} [m] \n')
            elif num_elements < 2:
                file.write(f"Distance between points: Too few points selected\n ")
            elif num_elements > 2:
                file.write(f"Distance between points: Too many points selected\n")
        
            if num_elements >= 3:
                azimuth, reverse_azimuth = self.calculate_azimuth()
                if 'decimal degrees' == self.unit_azimuth.currentText():
                    azimuth_text = f'Azimuth is (point id:1- id:2): {azimuth:.7f}[decimal degrees]'
                    reverse_azimuth_text = f'Reverse azimuth is (point id:2- id:1): {reverse_azimuth:.7f}[decimal degrees]'
                elif 'grads' == self.unit_azimuth.currentText():
                    azimuth_text = f'Azimuth is (point id:1- id:2): {azimuth:.4f}[grads]'
                    reverse_azimuth_text = f'Reverse azimuth is (point id:2- id:1): {reverse_azimuth:.4f}[grads]'
                file.write(azimuth_text + '\n')
                file.write(reverse_azimuth_text + '\n')
                height_difference = self.height_difference_function()
                file.write(height_difference + '\n')
                area = self.area_surface_function()
                acres = area / 100
                hectares = area / 10000
                file.write(f'Surface area is: {area:.3f} [m]\n')
                file.write(f'Surface area is: {acres:.3f} [a]\n')
                file.write(f'Surface area is: {hectares:.3f} [ha]\n')
            else:
                file.write(f"Azimuth is: Too few points selected\n")
                file.write(f"Height difference: Too few points selected\n")
                file.write(f"Surface area is: Too few points selected\n")