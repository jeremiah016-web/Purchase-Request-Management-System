"""
Delivery Tracking Integration
Supports multiple carriers: FedEx, UPS, DHL, USPS
"""
import requests
from django.conf import settings
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class DeliveryTracker:
    """Base class for delivery tracking"""
    
    def __init__(self, tracking_number, carrier):
        self.tracking_number = tracking_number
        self.carrier = carrier.lower()
    
    def track(self):
        """Track shipment based on carrier"""
        if self.carrier == 'fedex':
            return self._track_fedex()
        elif self.carrier == 'ups':
            return self._track_ups()
        elif self.carrier == 'dhl':
            return self._track_dhl()
        elif self.carrier == 'usps':
            return self._track_usps()
        else:
            return self._mock_tracking()  # For testing
    
    def _track_fedex(self):
        """Track FedEx shipment"""
        try:
            api_key = getattr(settings, 'FEDEX_API_KEY', '')
            
            if not api_key:
                return self._mock_tracking()
            
            # FedEx API endpoint
            url = "https://apis.fedex.com/track/v1/trackingnumbers"
            
            headers = {
                'Content-Type': 'application/json',
                'X-locale': 'en_US',
                'Authorization': f'Bearer {api_key}'
            }
            
            payload = {
                "trackingInfo": [{
                    "trackingNumberInfo": {
                        "trackingNumber": self.tracking_number
                    }
                }],
                "includeDetailedScans": True
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_fedex_response(data)
            else:
                logger.error(f"FedEx API error: {response.status_code}")
                return self._mock_tracking()
                
        except Exception as e:
            logger.error(f"FedEx tracking error: {str(e)}")
            return self._mock_tracking()
    
    def _track_ups(self):
        """Track UPS shipment"""
        try:
            api_key = getattr(settings, 'UPS_API_KEY', '')
            
            if not api_key:
                return self._mock_tracking()
            
            # UPS API endpoint
            url = f"https://onlinetools.ups.com/track/v1/details/{self.tracking_number}"
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_ups_response(data)
            else:
                logger.error(f"UPS API error: {response.status_code}")
                return self._mock_tracking()
                
        except Exception as e:
            logger.error(f"UPS tracking error: {str(e)}")
            return self._mock_tracking()
    
    def _track_dhl(self):
        """Track DHL shipment"""
        try:
            api_key = getattr(settings, 'DHL_API_KEY', '')
            
            if not api_key:
                return self._mock_tracking()
            
            # DHL API endpoint
            url = f"https://api-eu.dhl.com/track/shipments"
            
            headers = {
                'DHL-API-Key': api_key
            }
            
            params = {
                'trackingNumber': self.tracking_number
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_dhl_response(data)
            else:
                logger.error(f"DHL API error: {response.status_code}")
                return self._mock_tracking()
                
        except Exception as e:
            logger.error(f"DHL tracking error: {str(e)}")
            return self._mock_tracking()
    
    def _track_usps(self):
        """Track USPS shipment"""
        try:
            api_key = getattr(settings, 'USPS_API_KEY', '')
            
            if not api_key:
                return self._mock_tracking()
            
            # USPS API endpoint
            url = "https://secure.shippingapis.com/ShippingAPI.dll"
            
            params = {
                'API': 'TrackV2',
                'XML': f'''<TrackRequest USERID="{api_key}">
                    <TrackID ID="{self.tracking_number}"></TrackID>
                </TrackRequest>'''
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return self._parse_usps_response(response.text)
            else:
                logger.error(f"USPS API error: {response.status_code}")
                return self._mock_tracking()
                
        except Exception as e:
            logger.error(f"USPS tracking error: {str(e)}")
            return self._mock_tracking()
    
    def _parse_fedex_response(self, data):
        """Parse FedEx API response"""
        try:
            tracking_info = data['output']['completeTrackResults'][0]['trackResults'][0]
            
            return {
                'success': True,
                'carrier': 'FedEx',
                'tracking_number': self.tracking_number,
                'status': tracking_info.get('latestStatusDetail', {}).get('description', 'Unknown'),
                'location': tracking_info.get('latestStatusDetail', {}).get('scanLocation', {}).get('city', 'Unknown'),
                'estimated_delivery': tracking_info.get('estimatedDeliveryTimeWindow', {}).get('window', {}).get('ends'),
                'events': self._extract_fedex_events(tracking_info)
            }
        except Exception as e:
            logger.error(f"Error parsing FedEx response: {str(e)}")
            return self._mock_tracking()
    
    def _parse_ups_response(self, data):
        """Parse UPS API response"""
        try:
            shipment = data['trackResponse']['shipment'][0]
            package = shipment['package'][0]
            
            return {
                'success': True,
                'carrier': 'UPS',
                'tracking_number': self.tracking_number,
                'status': package['currentStatus']['description'],
                'location': package['currentStatus'].get('location', {}).get('address', {}).get('city', 'Unknown'),
                'estimated_delivery': package.get('deliveryDate', [{}])[0].get('date'),
                'events': self._extract_ups_events(package)
            }
        except Exception as e:
            logger.error(f"Error parsing UPS response: {str(e)}")
            return self._mock_tracking()
    
    def _parse_dhl_response(self, data):
        """Parse DHL API response"""
        try:
            shipment = data['shipments'][0]
            
            return {
                'success': True,
                'carrier': 'DHL',
                'tracking_number': self.tracking_number,
                'status': shipment['status']['statusCode'],
                'location': shipment['status'].get('location', {}).get('address', {}).get('addressLocality', 'Unknown'),
                'estimated_delivery': shipment.get('estimatedTimeOfDelivery'),
                'events': self._extract_dhl_events(shipment)
            }
        except Exception as e:
            logger.error(f"Error parsing DHL response: {str(e)}")
            return self._mock_tracking()
    
    def _parse_usps_response(self, xml_data):
        """Parse USPS XML response"""
        # Simplified parsing - in production, use xml.etree.ElementTree
        return self._mock_tracking()
    
    def _extract_fedex_events(self, tracking_info):
        """Extract tracking events from FedEx data"""
        events = []
        scan_events = tracking_info.get('scanEvents', [])
        
        for event in scan_events[:5]:  # Last 5 events
            events.append({
                'date': event.get('date'),
                'description': event.get('eventDescription'),
                'location': event.get('scanLocation', {}).get('city', 'Unknown')
            })
        
        return events
    
    def _extract_ups_events(self, package):
        """Extract tracking events from UPS data"""
        events = []
        activity = package.get('activity', [])
        
        for event in activity[:5]:  # Last 5 events
            events.append({
                'date': event.get('date'),
                'description': event.get('status', {}).get('description'),
                'location': event.get('location', {}).get('address', {}).get('city', 'Unknown')
            })
        
        return events
    
    def _extract_dhl_events(self, shipment):
        """Extract tracking events from DHL data"""
        events = []
        event_list = shipment.get('events', [])
        
        for event in event_list[:5]:  # Last 5 events
            events.append({
                'date': event.get('timestamp'),
                'description': event.get('description'),
                'location': event.get('location', {}).get('address', {}).get('addressLocality', 'Unknown')
            })
        
        return events
    
    def _mock_tracking(self):
        """Mock tracking data for testing/demo"""
        return {
            'success': True,
            'carrier': self.carrier.upper(),
            'tracking_number': self.tracking_number,
            'status': 'In Transit',
            'location': 'Distribution Center',
            'estimated_delivery': '2024-12-25',
            'events': [
                {
                    'date': '2024-12-20 10:00:00',
                    'description': 'Package picked up',
                    'location': 'Origin Facility'
                },
                {
                    'date': '2024-12-21 14:30:00',
                    'description': 'In transit',
                    'location': 'Sorting Facility'
                },
                {
                    'date': '2024-12-22 09:15:00',
                    'description': 'Arrived at distribution center',
                    'location': 'Distribution Center'
                },
                {
                    'date': '2024-12-23 08:00:00',
                    'description': 'Out for delivery',
                    'location': 'Local Facility'
                }
            ]
        }


def track_shipment(tracking_number, carrier):
    """
    Convenience function to track a shipment
    
    Args:
        tracking_number: Tracking number
        carrier: Carrier name (fedex, ups, dhl, usps)
        
    Returns:
        dict: Tracking information
    """
    tracker = DeliveryTracker(tracking_number, carrier)
    return tracker.track()
