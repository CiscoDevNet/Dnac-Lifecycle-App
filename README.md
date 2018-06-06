# Device Lifecycle App


The App will enable the users to view the published Security Advisories and Hardware and Software End-of-Life
information of the devices in DNA Centre. If the user has DNACaaP ServiceNow package installed in their cluster,
the app automatically generates tickets for the security advisories and hardware end-of-life with ServiceNow.

The users can use the information to secure their network against vulnerabilities and upgrade their network by
replacing the end-of-life devices.


## APIs used

DNAC Api – Get Inventory Devices & Get device count
            /api/v1/network-device/
            /api/v1/network-device/count
CAA Apis – Get PSIRT, Hardware and Software EoL
            /asi/api/csoq/lifecycle
DNACaaP Api - Post to ITSM Service now
            /api/dnacaap/v1/dnacaap/core/dna/events/{}/event

## Requirements.


The script requires the following packages/libraries to be installed.

    Python 3.4+ -- https://www.python.org/downloads/
    xlsxwriter 1.0.4 -- http://xlsxwriter.readthedocs.io/getting_started.html


## Getting Started



For help run:

```
main.py -h

```
        usage: main.py [-h] [-i IPADDRESS] [-u UNAME] {lifecycle}

        positional arguments:
          {lifecycle}           command = "lifecycle" for security advisories,
                                hardware end-of-life and software end-of-life

        optional arguments:
          -h, --help            show this help message and exit
          -i IPADDRESS, --ipaddress IPADDRESS
                                DNA Center cluster ip address
          -u UNAME, --uname UNAME
                                DNA Center login username




For running the lifecycle application:


```
main.py -i <cluster ipaddress> -u <uname> lifecycle

```


## Documentation For Authorization


The application will require the following credentials information to retrieve lifecycle data.
    DNAC Cluster credentails (Username and Password)
    CCO credentials (Username and Password)


## Author

AR

