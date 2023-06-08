# S7 Client

|           |                                                                             |
| --------- | --------------------------------------------------------------------------- |
| Name      | S7 Client                                                                  |
| Version   | v1.0.1                                                                      |
| DockerHub | [weevenetwork/s7-client](https://hub.docker.com/r/weevenetwork/s7-client) |
| Authors   | Paul Gaiduk                                                                 |

## Table of Contents

- [S7 Client](#s7-client)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Environment Variables](#environment-variables)
    - [Module Specific](#module-specific)
    - [Set by the weeve Agent on the edge-node](#set-by-the-weeve-agent-on-the-edge-node)
  - [Input](#input)
  - [Output](#output)

## Description

This module reads out the memory of a Siemens LOGO! controller at a specified interval and sends the read values labeled with the respective virtual memory addresses to the next module. The implementation is based on the [python-snap7](https://github.com/gijzelaerr/python-snap7) library.

## Environment Variables

### Module Specific

The following module configurations can be provided in a data service designer section on weeve platform:

| Environment Variables | type   | Description                                                                                                                                                                                                                                                                                             |
| --------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| LOGO_IP               | string | IP address at which the LOGO! controller can be reached                                                                                                                                                                                                                                                 |
| LOCAL_TSAP            | string | Local TSAP identifier                                                                                                                                                                                                                                                                                   |
| REMOTE_TSAP           | string | Remote TSAP identifier (of the LOGO! controller)                                                                                                                                                                                                                                                        |
| PORT                  | int    | Port number to reach the LOGO! controller                                                                                                                                                                                                                                                               |
| VM_ADDR               | string | Comma-separated list of VM addresses to read. The address identifier should start with "V" followed by a number, with an optional "W" (word) or "D" (double-word) between them. For example "VD3" will read the third double-word (4 bytes), "VW46" - the 46-th word (2 bytes) and "V10" the 10th byte. |
| POLL_INTERVAL         | int    | Poll interval in seconds                                                                                                                                                                                                                                                                                |

### Set by the weeve Agent on the edge-node

Other features required for establishing the inter-container communication between modules in a data service are set by weeve agent.

| Environment Variables | type   | Description                                                                                          |
| --------------------- | ------ | ---------------------------------------------------------------------------------------------------- |
| MODULE_NAME           | string | Name of the module                                                                                   |
| MODULE_TYPE           | string | Type of the module (Input, Processing, Output)                                                       |
| EGRESS_URLS           | string | HTTP ReST endpoint for the next module                                                               |
| LOG_LEVEL             | string | Allowed log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL. Refer to `logging` package documentation. |

## Input

-

## Output

Output of this module is a JSON with virtual addresses as lables followed by the bytes read from the LOGO! controller represented as integer numbers. Example:
```json
{
  "VD1": 71,
  "V6": 0
}
```
