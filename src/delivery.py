import requests
import json
import logging
from datetime import datetime

class WhatsAppDelivery:
    def __init__(self, config_path='config/whatsapp.json'):
        self.logger = logging.getLogger(__name__)
        # Load WhatsApp configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.headers = {
            'Authorization': f"Bearer {self.config['api_token']}",
            'Content-Type': 'application/json'
        }
    
    def send_to_channel(self, content):
        """Send message to WhatsApp channel"""
        self.logger.info("Sending news update to WhatsApp channel")
        
        url = f"{self.config['api_url']}/messages"
        
        payload = {
            'messaging_product': 'whatsapp',
            'to': self.config['channel_id'],
            'type': 'text',
            'text': {
                'body': content
            }
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            self.logger.info(f"Message sent successfully: {response.status_code}")
            return True, response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to send message: {str(e)}")
            return False, str(e)
