# CSV-Parakeet
![parakeet](https://user-images.githubusercontent.com/11004160/236465574-b17acf11-4bf5-46f9-9ab6-b01e5527d60b.jpeg)

[![Tests](https://github.com/A1fus/csv-parakeet/actions/workflows/tests.yaml/badge.svg)](https://github.com/A1fus/csv-parakeet/actions/workflows/tests.yaml)

A simple command line tool to convert csv files to parquet, and vice versa.

## Installation
Requirements:
- Python >=3.8

```bash
pip install --user csv-parakeet
```

## Usage
```bash
parakeet p2c /path/to/input.parquet /path/to/output.csv
parakeet c2p /path/to/input.csv /path/to/output.parquet
```

Noticed a bug? Raise an [issue](https://github.com/A1fus/csv-parakeet/issues/new).
