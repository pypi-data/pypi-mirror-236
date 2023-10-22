<p align="center">
    RANDOM USER AGENTS © 2023
</p>

<p align="center">
   <a href="https://telegram.dog/clinton_abraham"><img src="https://img.shields.io/badge/𝑪𝒍𝒊𝒏𝒕𝒐𝒏 𝑨𝒃𝒓𝒂𝒉𝒂𝒎-30302f?style=flat&logo=telegram" alt="telegram badge"/></a>
   <a href="https://telegram.dog/Space_x_bots"><img src="https://img.shields.io/badge/Sᴘᴀᴄᴇ ✗ ʙᴏᴛꜱ-30302f?style=flat&logo=telegram" alt="telegram badge"/></a>
   <a href="https://telegram.dog/sources_codes"><img src="https://img.shields.io/badge/Sᴏᴜʀᴄᴇ ᴄᴏᴅᴇꜱ-30302f?style=flat&logo=telegram" alt="telegram badge"/></a>
</p>


Random User Agents is a python library that provides list of user agents,
from a collection of more than 326,000+ user agents, based on filters.


## INSTALLATION

You can install random useragent by running the following command:

```bash
  pip install uxagent
```


## USAGE

```python

from UXAGENT.uxagent import UserAgent
from UXAGENT.filters import SoftwareName
from UXAGENT.filters import OperatingSystem

software = [ SoftwareName.APP024.value ]

osystems = [ OperatingSystem.COD001.value, OperatingSystem.COD002.value ]

rotators = UserAgent(limit=100, operating_system=osystems, software_names=software)

# GET RANDOM USER AGENT
user_agent = rotators.get_user_agent()
print(user_agent)

# GET LIST OF USER AGENTS
user_agents = rotators.get_user_agents()
print(user_agents)

```


All filters are available > [Click here](https://github.com/Clinton-Abraham/TEMPLATES/tree/V1.0/NOTE02/readme.md)


## LICENSE

The MIT License. Please see [License File](https://github.com/Clinton-Abraham/USER-X-AGENT/blob/V1.0/LICENSE) for more information.


## USER AGENTS SOURCE

Special thanks to [whatismybrowser](https://developers.whatismybrowser.com/) for providing real user agents.
