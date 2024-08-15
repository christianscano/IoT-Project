from mongoengine import DynamicDocument, DateTimeField, FloatField, BooleanField, \
    EmbeddedDocument, SortedListField, EmbeddedDocumentField, StringField
from datetime import datetime
from bson import json_util
import json

TEMPERATURES_RETENTION = 4000
ALARM_RETENTION        = 500

class Temperatures(DynamicDocument):
    """
    A class to record temperature measurements of the server room
    in the MongoDB database.
    """
    timestamp = DateTimeField(required = True, default = datetime.now)
    value     = FloatField(required = True)
    
    meta = {
        'collection': 'temperatures', 
        'ordering'  : ['-timestamp'],
        'indexes'   : ['timestamp']
    }

    def to_dict(self):
        data = self.to_mongo().to_dict()
        data = json.loads(json_util.dumps(data))
        data = {'value': data['value'], 'timestamp': data['timestamp']['$date']}
        return data

    @classmethod
    def add_measure(cls, value):
        if cls.objects.count() >= TEMPERATURES_RETENTION:
            oldest_entry = cls.objects.order_by('timestamp').first()
            if oldest_entry:
                oldest_entry.delete()

        new_temp = cls(value = value)
        new_temp.save()
    
    @classmethod
    def get_last_measure(cls):
        last_measurement = cls.objects.first()
        if last_measurement:
            return last_measurement
        return None
    
    @classmethod
    def get_time_range(cls, start):
        delta = datetime.now() - start
        return cls.objects.filter(timestamp__gte = delta)


class AlarmStatus(EmbeddedDocument):
    timestamp  = DateTimeField(required = True, default = datetime.now)
    enabled    = BooleanField(required = True)

    meta = {
        'ordering': ['-timestamp'],
        'indexes' : ['timestamp']
    }

    def to_dict(self):
        data = self.to_mongo().to_dict()
        return json.loads(json_util.dumps(data))


class IntrusionSystem(DynamicDocument):
    """
    A classs to record the status of the detection alarm in the 
    MongoDB database.
    """
    name       = StringField(required=True, unique=True)
    enabled    = BooleanField(required=True)
    alarm_logs = SortedListField(
        EmbeddedDocumentField(AlarmStatus), 
        ordering = 'timestamp', 
        reverse  = True
    )
    
    meta = {'collection': 'intrusion_system'}

    def to_dict(self):
        data = self.to_mongo().to_dict()
        return json.loads(json_util.dumps(data))

    @classmethod
    def create_intrusion_system(cls, name = 'intrusion_system-0'):
        intr_sys = cls(name = name, enabled = False)
        intr_sys.save()

    @classmethod
    def update_status(cls, status, name = 'intrusion_system-0'):
        intr_sys = cls.objects(name = name).first()
        intr_sys.enabled = status
        intr_sys.save()
    
    @classmethod
    def get_last_status(cls, name = 'intrusion_system-0'):
        last_status = cls.objects(name = name).first()
        if last_status:
            return last_status.enabled
        return False
    
    @classmethod
    def get_intrusion_system(cls, name = 'intrusion_system-0'):
        return cls.objects(name = name).first()
    
    @classmethod
    def add_alarm_log(cls, status, name = 'intrusion_system-0'):
        intr_sys = cls.objects(name = name).first()

        if len(intr_sys.alarm_logs) > ALARM_RETENTION:
            intr_sys.alarm_logs.remove(intr_sys.alarm_logs[-1])

        intr_sys.alarm_logs.append(AlarmStatus(enabled = status))
        intr_sys.save()

    @classmethod
    def get_last_alarm_status(cls, name = 'intrusion_system-0'):
        intr_sys = cls.objects(name = name).first()

        if intr_sys.alarm_logs:
            return intr_sys.alarm_logs[0]
        return None