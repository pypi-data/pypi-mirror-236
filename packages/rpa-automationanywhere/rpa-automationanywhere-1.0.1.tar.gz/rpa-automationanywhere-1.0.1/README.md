# RPA_AUTOMATIONANYWHERE
Python module delivers some actions to communicate with Automation Anywhere A360 API.
The module is compatibile with the Robocorp.

## Installation
To install the package run:

```
pip install rpa_automationanywhere
```

## Example
### Fetching credential
```
from rpa_automationanywhere.Vault import Vault
vault = Vault('http://controlroom.net', 'user name', 'password')
vault.get_credential('demo')
```
