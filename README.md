

# MySmartBike - DEV in progress - NO WORKING Version yet
[![HassFest tests](https://github.com/renenulschde/ha-mysmartbike/workflows/Validate%20with%20hassfest/badge.svg)](https://developers.home-assistant.io/blog/2020/04/16/hassfest)![Validate with HACS](https://github.com/ReneNulschDE/ha-mysmartbike/workflows/Validate%20with%20HACS/badge.svg)


MySmartBike (Male powered e-bikes) platform as a Custom Component for Home Assistant.

IMPORTANT:

* Please login once in the MySmartBike IOS or Android app before you install this component. Make sure you connected your bike in the app 

* Tested Countries: DE

### Installation
* First: This is not a Home Assistant Add-On. It's a custom component.

* There is no way to install as the code is not completed yet

* [How to install a custom component?](https://www.google.com/search?q=how+to+install+custom+components+home+assistant) 
* [How to install HACS?](https://hacs.xyz/docs/installation/prerequisites)
### Configuration

Use the "Add Integration" in Home Assistant and select "MySmartBike".

Use your MySmartBike-login email address and your Password.

### Optional configuration values

See Options dialog in the Integration under Home-Assistant/Configuration/Integration.

```
Excluded Bikes: comma-separated list of VINs.
```

## Available components 
Depends on your own bike.


### Binary Sensors

* None

### Device Tracker
  
* WIP

### Locks

* None

### Sensors

* None

### Diagnostic Sensors 
[Diagnostic sensors](https://www.home-assistant.io/blog/2021/11/03/release-202111/#entity-categorization) are hidden by default, check the devices page to see the current values

* None

### Services

* None

### Switches

* None

### Logging

Set the logging to debug with the following settings in case of problems.

```
logger:
  default: warn
  logs:
    custom_components.mysmartbike: debug
```

### Open Items
* List is too long as we are on version 0.0.1

### Useful links

* [Forum post](WIP)
