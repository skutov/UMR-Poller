# UMR-Poller

Python script to retrieve status info (e.g. LTE signal levels) from one or more Ubiquiti UMR routers and log alongside GPS data.

## Description

Script (will) allow configuraion by file to provide multiple routers to poll, the frequency of polling, and what data to be logged for analysis.

This is created as a tool to assist with troubleshooting LTE signal levels on moving platforms or to monitor across a large deployment of routers where historical logging is required.

## Getting Started

### Dependencies

* python3 and default system libraries

### Installing

* Clone repository into desired directory and `chmox +x UMR-Poller.py`
* Create config.yml and enter configuration details for target routers (see `config.yml.example`)

### Executing program

```
./UMR-Poller.py
```

## Help

Script has built in help.
```
./UMR-Poller.py --help
```

## Authors

[@Robb Gosset](https://github.com/skutov)

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the Mozilla Public License Version 2.0 License - see the LICENSE.md file for details

## Acknowledgments

* [Stack Overflow](https://stackoverflow.com/questions)
* [har2requests](https://pypi.org/project/har2requests/)
* [Python Template](https://gist.github.com/MstWntd/646429e25d8f5fa713792e716dcd9de1)
