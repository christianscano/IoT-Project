from mongoengine import DynamicDocument, DateTimeField, FloatField
from datetime import datetime
from bson import json_util
import json
import logging

MAX_TEMPERATURES = 500
#logger = logging.getLogger(__name__)

class Temperatures(DynamicDocument):
    timestamp = DateTimeField(required=True, default=datetime.now),
    value     = FloatField(required=True)

    meta = {
        'collection': 'temperatures', 
        'ordering'  : ['-timestamp'],
        'indexes'   : ['timestamp']
    }

    @classmethod
    def add_measure(cls, value):
        if cls.objects.count() >= MAX_TEMPERATURES:
            # Find the oldest entry and delete it
            oldest_entry = cls.objects.order_by('timestamp').first()
            if oldest_entry:
                oldest_entry.delete()

        # Add the new temperature entry
        new_temp = cls(value = value)
        new_temp.save()
    
    @classmethod
    def get_last_measure(cls):
        last_measurement = cls.objects.first()
        if last_measurement:
            return last_measurement
        return None
    
    def to_dict(self):
        data = self.to_mongo().to_dict()
        return json.loads(json_util.dumps(data))