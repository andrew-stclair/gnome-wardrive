"""
Data Manager
Handles storage, management, and export of wardriving data
"""

import json
import csv
import xml.etree.ElementTree as ET
import time
from datetime import datetime
import gpxpy
import gpxpy.gpx

class DataManager:
    """Manages wardriving data collection and export"""
    
    def __init__(self):
        # Data storage
        self.networks = {}  # BSSID -> network data
        self.locations = []  # Location history
        self.current_location = None
        
        # Statistics
        self.scan_start_time = None
        self.total_networks = 0
        
    def add_network(self, network_data):
        """Add or update network data"""
        bssid = network_data.get('bssid')
        if not bssid:
            return
            
        # Add current location to network data
        if self.current_location:
            network_data.update({
                'latitude': self.current_location['latitude'],
                'longitude': self.current_location['longitude'],
                'accuracy': self.current_location['accuracy']
            })
            
        # Update or add network
        if bssid in self.networks:
            # Update existing network (better signal, more recent timestamp)
            existing = self.networks[bssid]
            if (network_data.get('signal_strength', -100) > 
                existing.get('signal_strength', -100)):
                # Keep the better signal strength data
                existing.update(network_data)
            existing['last_seen'] = network_data.get('timestamp', time.time())
        else:
            # New network
            self.networks[bssid] = network_data
            self.total_networks += 1
            
    def update_location(self, latitude, longitude, accuracy):
        """Update current location"""
        location_data = {
            'latitude': latitude,
            'longitude': longitude,
            'accuracy': accuracy,
            'timestamp': time.time()
        }
        
        self.current_location = location_data
        self.locations.append(location_data)
        
    def get_network_count(self):
        """Get total number of unique networks"""
        return len(self.networks)
        
    def get_networks_list(self):
        """Get list of all networks"""
        return list(self.networks.values())
        
    def export_data(self, file_path, format_type):
        """Export data in specified format"""
        try:
            if format_type == 'csv':
                return self.export_csv(file_path)
            elif format_type == 'kml':
                return self.export_kml(file_path)
            elif format_type == 'gpx':
                return self.export_gpx(file_path)
            else:
                return False
        except Exception as e:
            print(f"Export error: {e}")
            return False
            
    def export_csv(self, file_path):
        """Export data to CSV format"""
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'SSID', 'BSSID', 'Security', 'Signal_Strength', 'Frequency', 
                'Channel', 'Latitude', 'Longitude', 'Accuracy', 'Timestamp',
                'Device_Interface', 'First_Seen', 'Last_Seen'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for network in self.networks.values():
                writer.writerow({
                    'SSID': network.get('ssid', ''),
                    'BSSID': network.get('bssid', ''),
                    'Security': network.get('security', ''),
                    'Signal_Strength': network.get('signal_strength', ''),
                    'Frequency': network.get('frequency', ''),
                    'Channel': network.get('channel', ''),
                    'Latitude': network.get('latitude', ''),
                    'Longitude': network.get('longitude', ''),
                    'Accuracy': network.get('accuracy', ''),
                    'Timestamp': datetime.fromtimestamp(
                        network.get('timestamp', 0)).isoformat(),
                    'Device_Interface': network.get('device_interface', ''),
                    'First_Seen': datetime.fromtimestamp(
                        network.get('timestamp', 0)).isoformat(),
                    'Last_Seen': datetime.fromtimestamp(
                        network.get('last_seen', 0)).isoformat(),
                })
                
        return True
        
    def export_kml(self, file_path):
        """Export data to KML format for Google Earth"""
        # Create KML structure
        kml = ET.Element('kml', xmlns='http://www.opengis.net/kml/2.2')
        document = ET.SubElement(kml, 'Document')
        
        # Add document info
        ET.SubElement(document, 'name').text = 'WiFi Wardriving Data'
        ET.SubElement(document, 'description').text = f'WiFi networks found during wardriving session. Total networks: {len(self.networks)}'
        
        # Add styles for different security types
        self.add_kml_styles(document)
        
        # Add network placemarks
        for network in self.networks.values():
            if 'latitude' not in network or 'longitude' not in network:
                continue
                
            placemark = ET.SubElement(document, 'Placemark')
            ET.SubElement(placemark, 'name').text = network.get('ssid', 'Hidden Network')
            
            # Description with network details
            description = f"""
            <![CDATA[
            <b>SSID:</b> {network.get('ssid', 'Hidden')}<br/>
            <b>BSSID:</b> {network.get('bssid', 'Unknown')}<br/>
            <b>Security:</b> {network.get('security', 'Unknown')}<br/>
            <b>Signal Strength:</b> {network.get('signal_strength', 'Unknown')} dBm<br/>
            <b>Frequency:</b> {network.get('frequency', 'Unknown')} MHz<br/>
            <b>Channel:</b> {network.get('channel', 'Unknown')}<br/>
            <b>First Seen:</b> {datetime.fromtimestamp(network.get('timestamp', 0)).strftime('%Y-%m-%d %H:%M:%S')}<br/>
            <b>Accuracy:</b> ±{network.get('accuracy', 'Unknown')}m
            ]]>
            """
            ET.SubElement(placemark, 'description').text = description
            
            # Style based on security
            security = network.get('security', 'Unknown')
            if security == 'Open':
                ET.SubElement(placemark, 'styleUrl').text = '#open_style'
            elif security in ['WEP']:
                ET.SubElement(placemark, 'styleUrl').text = '#wep_style'
            elif security in ['WPA', 'WPA2', 'WPA3']:
                ET.SubElement(placemark, 'styleUrl').text = '#wpa_style'
            else:
                ET.SubElement(placemark, 'styleUrl').text = '#unknown_style'
                
            # Point coordinates
            point = ET.SubElement(placemark, 'Point')
            coordinates = f"{network['longitude']},{network['latitude']},0"
            ET.SubElement(point, 'coordinates').text = coordinates
            
        # Write KML file
        tree = ET.ElementTree(kml)
        tree.write(file_path, encoding='utf-8', xml_declaration=True)
        
        return True
        
    def add_kml_styles(self, document):
        """Add KML styles for different security types"""
        # Open networks (red)
        style = ET.SubElement(document, 'Style', id='open_style')
        icon_style = ET.SubElement(style, 'IconStyle')
        ET.SubElement(icon_style, 'color').text = 'ff0000ff'  # Red
        icon = ET.SubElement(icon_style, 'Icon')
        ET.SubElement(icon, 'href').text = 'http://maps.google.com/mapfiles/kml/pushpin/red-pushpin.png'
        
        # WEP networks (orange)
        style = ET.SubElement(document, 'Style', id='wep_style')
        icon_style = ET.SubElement(style, 'IconStyle')
        ET.SubElement(icon_style, 'color').text = 'ff0080ff'  # Orange
        icon = ET.SubElement(icon_style, 'Icon')
        ET.SubElement(icon, 'href').text = 'http://maps.google.com/mapfiles/kml/pushpin/orange-pushpin.png'
        
        # WPA/WPA2/WPA3 networks (green)
        style = ET.SubElement(document, 'Style', id='wpa_style')
        icon_style = ET.SubElement(style, 'IconStyle')
        ET.SubElement(icon_style, 'color').text = 'ff00ff00'  # Green
        icon = ET.SubElement(icon_style, 'Icon')
        ET.SubElement(icon, 'href').text = 'http://maps.google.com/mapfiles/kml/pushpin/grn-pushpin.png'
        
        # Unknown security (yellow)
        style = ET.SubElement(document, 'Style', id='unknown_style')
        icon_style = ET.SubElement(style, 'IconStyle')
        ET.SubElement(icon_style, 'color').text = 'ff00ffff'  # Yellow
        icon = ET.SubElement(icon_style, 'Icon')
        ET.SubElement(icon, 'href').text = 'http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png'
        
    def export_gpx(self, file_path):
        """Export data to GPX format"""
        # Create GPX object
        gpx = gpxpy.gpx.GPX()
        gpx.name = 'WiFi Wardriving Session'
        gpx.description = f'WiFi networks found during wardriving. Total: {len(self.networks)}'
        
        # Add networks as waypoints
        for network in self.networks.values():
            if 'latitude' not in network or 'longitude' not in network:
                continue
                
            waypoint = gpxpy.gpx.GPXWaypoint(
                latitude=network['latitude'],
                longitude=network['longitude'],
                name=network.get('ssid', 'Hidden Network')
            )
            
            # Add description
            waypoint.description = (
                f"BSSID: {network.get('bssid', 'Unknown')}, "
                f"Security: {network.get('security', 'Unknown')}, "
                f"Signal: {network.get('signal_strength', 'Unknown')} dBm"
            )
            
            # Add timestamp
            if 'timestamp' in network:
                waypoint.time = datetime.fromtimestamp(network['timestamp'])
                
            gpx.waypoints.append(waypoint)
            
        # Add track from location history if available
        if self.locations:
            track = gpxpy.gpx.GPXTrack()
            track.name = 'Wardriving Route'
            
            segment = gpxpy.gpx.GPXTrackSegment()
            
            for location in self.locations:
                point = gpxpy.gpx.GPXTrackPoint(
                    latitude=location['latitude'],
                    longitude=location['longitude'],
                    time=datetime.fromtimestamp(location['timestamp'])
                )
                segment.points.append(point)
                
            track.segments.append(segment)
            gpx.tracks.append(track)
            
        # Write GPX file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(gpx.to_xml())
            
        return True
        
    def clear_data(self):
        """Clear all collected data"""
        self.networks.clear()
        self.locations.clear()
        self.current_location = None
        self.total_networks = 0
        
    def get_statistics(self):
        """Get scanning statistics"""
        return {
            'total_networks': len(self.networks),
            'open_networks': len([n for n in self.networks.values() if n.get('security') == 'Open']),
            'wep_networks': len([n for n in self.networks.values() if n.get('security') == 'WEP']),
            'wpa_networks': len([n for n in self.networks.values() if n.get('security', '').startswith('WPA')]),
            'locations_recorded': len(self.locations),
            'scan_duration': time.time() - self.scan_start_time if self.scan_start_time else 0
        }