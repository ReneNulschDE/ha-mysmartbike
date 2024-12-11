# MySmartBike (Mahle powered e-bikes) integration for Home-Assistant.

![HassFest tests](https://img.shields.io/github/actions/workflow/status/renenulschde/ha-mysmartbike/.github/workflows/hassfest.yaml?label=hassfest%20check) ![Validate with HACS](https://github.com/ReneNulschDE/ha-mysmartbike/workflows/Validate%20with%20HACS/badge.svg) ![](https://img.shields.io/github/downloads/renenulschde/ha-mysmartbike/total) ![](https://img.shields.io/github/downloads/renenulschde/ha-mysmartbike/latest/total)

MySmartBike (Mahle powered e-bikes) platform as a Custom Component for Home Assistant.

IMPORTANT:

- Please login once in the MySmartBike IOS or Android app before you install this component. Make sure you connected your bike(s) in the app

- Tested countries: DE

- Tested bikes:
  - Schindelhauer Arthur IX
  - Orbea Vibe

## Features:

- Connect to MySmartBike Cloud and collect registered devices
- Create sensors and device tracker for the devices

## Installation

### HACS

- The integration is available via HACS (https://hacs.xyz/docs/use/)
  - Search for "MySmartBike"
- Restart HA, Refresh your HA Browser window

### Manual installation

- This is a Home Assistant custom component (not an Add-in).
- Download the folder custom_component and copy it into your Home-Assistant config folder.
- [How to install a custom component?](https://www.google.com/search?q=how+to+install+custom+components+home+assistant)
- Restart HA, Refresh your HA Browser window

## Configuration

Use the "Add Integration" in Home Assistant and select "MySmartBike" and follow the following steps:

1. Put in your MySmartBike email address and password in the component setup.

## Device Tracker

- Device Tracker with GPS data (last location reported)

## Sensors

- State of charge (Percent, 0-100)
- Odometer (in meters) - Conversation is WIP

## Diagnostic Sensors

[Diagnostic sensors](https://www.home-assistant.io/blog/2021/11/03/release-202111/#entity-categorization) are hidden by default, check the devices page to see the current values

- None

## Services

- None

## Switches

- None

## Logging

Set the logging to debug with the following settings in case of problems.

```
logger:
  default: warn
  logs:
    custom_components.mysmartbike: debug
```

## Open Items

- Let me know via the issue section

## Useful links

- [Forum post](https://community.home-assistant.io/t/mysmartbike-mahle-powered-e-bikes-integration-for-home-assistant/676740)

## Trademark Legal Notices

All product names, trademarks and registered trademarks in this
repository, are property of their respective owners and are used by this project for identification purposes only.

The use of these names, trademarks and brands appearing do not imply endorsement.
