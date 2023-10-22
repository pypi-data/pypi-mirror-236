import os
import json
import random
import zipfile
#===================================================================================================================

class UserAgent:

    ATTRIBUTESMAP = {
        'hardware_types': [],
        'software_types': [],
        'software_names': [],
        'software_engines': [],
        'popularity_types': [],
        'operating_system': []}

#===================================================================================================================
   
    def __init__(self, limit=None, *args, **kwargs):

        self.user_agents = []
        for attribute, values in self.ATTRIBUTESMAP.items():
            setattr(self, attribute, kwargs.get(attribute, [v.lower() for v in values]))

        for user_agent in self.load_user_agents():        
            if limit is not None and len(self.user_agents) >= limit:
                break
            if self.hardware_types and user_agent['hardware_types'].lower() not in self.hardware_types:
                continue
            if self.software_types and user_agent['software_types'].lower() not in self.software_types:
                continue
            if self.software_names and user_agent['software_names'].lower() not in self.software_names:
                continue
            if self.software_engines and user_agent['software_engines'].lower() not in self.software_engines:
                continue
            if self.popularity_types and user_agent['popularity_types'].lower() not in self.popularity_types:
                continue
            if self.operating_system and user_agent['operating_system'].lower() not in self.operating_system:
                continue

            self.user_agents.append(user_agent)

#===================================================================================================================

    def load_user_agents(self):
        osem_path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(osem_path, 'data/user_agents.zip')
        with zipfile.ZipFile(file_path) as zipped_user_agents:
            with zipped_user_agents.open('user_agents.jl') as user_agents:
                for user_agent in user_agents:
                    if hasattr(user_agent, 'decode'):
                        user_agent = user_agent.decode()

                    yield json.loads(user_agent)

#===================================================================================================================
    
    def get_user_agents(self):
        return self.user_agents

#===================================================================================================================

    def get_user_agent(self):
        try:
            return random.choice(self.user_agents)['user_agent']
        except Exception:
            return None

#===================================================================================================================
