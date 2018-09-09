from google.cloud import datastore    
from datetime import datetime
import logging
import json

client = datastore.Client(project='beatrizyguillem')

def add_entity(kind='Test', **kwargs):
    """Add entity to the DB

    """
    key = client.key(kind)
    boot_e = datastore.Entity(key=key)
    boot_e.update(kwargs)
    client.put(boot_e)


class Invited:
    def __init__(self, name, email='', telef='',
                 comp1='', comp2='', comp3='', comp4='',
                 kids=0, intol=None, dance=False):
        self.name = name
        self.email = email
        self.telef = telef
        self.comp1 = comp1
        self.comp2 = comp2
        self.comp3 = comp3
        self.comp4 = comp4
        self.kids = kids
        self.intol = intol
        self.dance = dance
        self.when = datetime.now().isoformat()


    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'telef': self.telef,
            'comp1': self.comp1,
            'comp2': self.comp2,
            'comp3': self.comp3,
            'comp4': self.comp4,
            'kids': self.kids,
            'intol': json.dumps(self.intol),
            'when': self.when,
            'dance': self.dance}
        
    
    @staticmethod
    def query_name(name):
        query = client.query(kind='Invited')
        query.add_filter('name', '=', name)
        return list(query.fetch())
        

    def put(self):
        if not self.query_name(self.name):
            add_entity(kind='Invited', **self.to_dict())
        else:
            raise ValueError('Invited already in database')
        

if __name__ == '__main__':
    add_entity(kind='Test', name='test', field='content')
