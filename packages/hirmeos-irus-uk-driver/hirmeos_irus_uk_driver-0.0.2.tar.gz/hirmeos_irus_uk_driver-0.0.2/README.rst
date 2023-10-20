==============
IRUS UK Driver
==============

Provide functionality to collect and normalise report data from IRUS-UK.

Refer to https://irus.jisc.ac.uk/r5/oapen/embed/api/#irus_ir for config options.

Release Notes:
==============

[0.0.2] - 2023-10-19
---------------------
Added
.....
    - Pydantic serializers/models to handle IRUS-UK response data
    - Provided functionality to return serialized data without explicitly
      using the Irus Client.

Changed
.......
    - Changed required options for fetching data


[0.0.1] - 2023-09-22
---------------------
Added
.......
    - Logic to initialise the webdriver
    - Log in to Google
    - Fetch a Google Play Books report
