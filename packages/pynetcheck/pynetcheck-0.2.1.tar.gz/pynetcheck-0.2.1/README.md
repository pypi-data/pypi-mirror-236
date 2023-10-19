#  PyNetCheck

## Python Network Checker

This project provides examples to extend the IP Fabric platform with custom device testing.

*This project is still in development and more test cases and examples will be added at a later time.*

## Requirements

* `Configuration saved` task must be enabled in [IP Fabric Discovery Settings](https://docs.ipfabric.io/latest/IP_Fabric_Settings/Discovery_and_Snapshots/Discovery_Settings/disabled_discovery_tasks/).


## Installation

The project is available on PyPi and can be installed via pip:

```bash
pip install pynetcheck
cp sample.env .env  # TODO: Update .env with your IP Fabric URL and credentials
```

Finally edit the `.env` file to include your IP Fabric URL and credentials.

## Running

To run tests with builtin cases, use the following command:

```bash
pynetcheck
```

To run using a directory that stores a list of configuration files:

```bash
pynetcheck --config-dir /path/to/dir
```

To run against your own test cases:

```bash
>pynetcheck --tb=line --testpaths tests    
========================================================================================== test session starts ==========================================================================================
platform win32 -- Python 3.9.9, pytest-7.4.2, pluggy-1.3.0
rootdir: C:\Code\_EXAMPLES\config_vulnerability
configfile: pyproject.toml
plugins: anyio-4.0.0, depends-1.0.1, html-reporter-0.2.9
collected 357 items                                                                                                                                                                                      

tests\test_ssh.py FFFFFFFFFFFFFFFFFFF.FFF.FFF......FFF.FFFF.FFFFFFFFFFFFFFFFFFFFFFFF....F..........FF.F.....F.......FFFFF.F..FFFFF.FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF.FFFFFFFFFFFFFFF.FFFFFFFFFFFF.FF [ 49%]
FF.FFFFFFFFFFFFFFF.FFFFFFF.FFFFFFFFFFFFF.FFFFFFFFFFFFFFF.FFFFFFFFFFFFFFFFFFFFFF..FFFF..FFFFFFFF.FFFFF.FFFF.FF.F...F.F.FFFFFFFFF.FFFFF..FF.....FF.FFFFFFFFFFF.FFF......F....FFFFFFFFFF              [100%]
```

## Results

### HTML

Results are stored in the [pytest_html_report.html](example/pytest_html_report.html) which can be viewed in any browser.  

![img.png](example/pytest_html.png)

### Exporting

The `pytest-html-reporter` also provides the ability to export via CSV or Excel formats, example: [pytest.csv](example/pytest.csv).

Table modified to show only the relevant information:

| Suite                               | Test Case                                  | Status | Time (s) | Error Message                                               |
|-------------------------------------|--------------------------------------------|--------|----------|-------------------------------------------------------------|
| tests/cve_2023_20198/ios_xe_test.py | test_saved_config_consistency              | PASS   | 0.21     |                                                             |
| tests/cve_2023_20198/ios_xe_test.py | test_https_server_vulnerable[L77R12-LEAF6] | SKIP   | 0        |                                                             |
| tests/cve_2023_20198/ios_xe_test.py | test_https_server_vulnerable[L77R11-LEAF5] | FAIL   | 0        | E   AssertionError: Startup - HTTP secure-server Vulnerable |
| tests/cve_2023_20198/ios_xe_test.py | test_https_server_vulnerable[L67CSR16]     | SKIP   | 0        |                                                             |
| tests/cve_2023_20198/ios_xe_test.py | test_https_server_disabled[L77R12-LEAF6]   | PASS   | 0        |                                                             |
| tests/cve_2023_20198/ios_xe_test.py | test_https_server_disabled[L77R11-LEAF5]   | FAIL   | 0        | E   AssertionError: Startup - HTTP secure-server Enabled    |
| tests/cve_2023_20198/ios_xe_test.py | test_https_server_disabled[L67CSR16]       | PASS   | 0        |                                                             |
| tests/cve_2023_20198/ios_xe_test.py | test_http_server_vulnerable[L77R12-LEAF6]  | SKIP   | 0        |                                                             |
| tests/cve_2023_20198/ios_xe_test.py | test_http_server_vulnerable[L77R11-LEAF5]  | SKIP   | 0        |                                                             |
| tests/cve_2023_20198/ios_xe_test.py | test_http_server_vulnerable[L67CSR16]      | FAIL   | 0        | E   AssertionError: Running - HTTP server Vulnerable        |
| tests/cve_2023_20198/ios_xe_test.py | test_http_server_disabled[L77R12-LEAF6]    | PASS   | 0.13     |                                                             |
| tests/cve_2023_20198/ios_xe_test.py | test_http_server_disabled[L77R11-LEAF5]    | PASS   | 0.15     |                                                             |
| tests/cve_2023_20198/ios_xe_test.py | test_http_server_disabled[L67CSR16]        | FAIL   | 0.15     | E   AssertionError: Running - HTTP server Enabled           |

