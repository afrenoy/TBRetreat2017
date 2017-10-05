# Example: Get a file from a server

Say you want to get the [csv files provided as supplementary information](http://www.pnas.org/content/suppl/2017/08/09/1616744114.DCSupplemental) for the following, randomly chosen, paper:

[Genomic evidence reveals a radiation of placental mammals uninterrupted by the KPg boundary](http://www.pnas.org/content/114/35/E7282.abstract)

## wget

```bash
    wget www.pnas.org/content/suppl/2017/08/09/1616744114.DCSupplemental/pnas.1616744114.sd01.csv
```

As simple as that!

## curl

```bash
    curl www.pnas.org/content/suppl/2017/08/09/1616744114.DCSupplemental/pnas.1616744114.sd[01-10].csv -o 'data/#1.csv'
```

`[01-10]` defines a range parameter. `#1` designates this (the first) parameter.


## Use wget to get _all_ files

```bash
    wget -nd -r -P images/ -A jpg http://tb-paperplane.ethz.ch/
```
