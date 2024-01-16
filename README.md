# MySmartBike

[![HassFest tests](https://github.com/renenulschde/ha-mysmartbike/workflows/Validate%20with%20hassfest/badge.svg)](https://developers.home-assistant.io/blog/2020/04/16/hassfest)

MySmartBike (Male powered e-bikes) platform as a Custom Component for Home Assistant.

IMPORTANT:

- Please login once in the MySmartBike IOS or Android app before you install this component. Make sure you connected your bike(s) in the app

- Tested Countries: DE

### Features:

- Connect to MySmartBike Cloud and collect registered devices
- Create sensors and device tracker for the found devices

### Installation

- This is a Home Assistant custom component (not an Add-in).
- Download the folder custom_component and copy it into your Home-Assistant config folder.
- [How to install a custom component?](https://www.google.com/search?q=how+to+install+custom+components+home+assistant)
- Restart HA, Refresh your HA Browser window
- (or add the github repo Url to HACS...)

### Configuration

Use the "Add Integration" in Home Assistant and select "MySmartBike" and follow the following steps:

1. Put in your MySmartBike email address and password in the component setup.

### Sensors

- State of charge (Percent, 0-100)
- Odometer (in meters) - Conversation is WIP

### Diagnostic Sensors

[Diagnostic sensors](https://www.home-assistant.io/blog/2021/11/03/release-202111/#entity-categorization) are hidden by default, check the devices page to see the current values

- None

### Services

- None

### Switches

- None

### Logging

Set the logging to debug with the following settings in case of problems.

```
logger:
  default: warn
  logs:
    custom_components.mysmartbike: debug
```

### Open Items

- List is too long as we are on version 0.0.1

### Useful links

- [Forum post](WIP)
