# influx-bucket-mapper

## Motivation

If you have an InfluxDBv2 installation, but you want to use Chronograf
with it, you will need to create database retention policy mappings
(DBRPs) for each of those buckets; see:

https://docs.influxdata.com/influxdb/v2.2/query-data/influxql/#map-unmapped-buckets

This is irritating and, if you have many buckets, both time-consuming
and error-prone to do by hand.

## Bucketmapper

Therefore: [bucketmapper](./bucketmapper).  This is a Python 3 script
which queries the buckets in an organization, and creates any mappings
that don't yet exist.

The generated database will have the same name as the bucket.

It determines the bucket retention period and creates an appropriate
representation of that period in Influx Duration Literal syntax:

https://docs.influxdata.com/influxdb/v1.8/query_language/spec/#durations

### Bucketmapper Configuration

[bucketmapper](./bucketmapper) expects the same environment variables as
InfluxDBv2 or Chronograf:

- `INFLUXDB_TOKEN`
- `INFLUXDB_ORG`
- `INFLUXDB_URL`

Use the organization _name_ rather than its ID here.

The only third-party Python library required is
[aiohttp](https://docs.aiohttp.org/en/stable/).  That's captured in
[requirements.txt](requirements.txt).

## Docker container

We also supply a [Dockerfile](./Dockerfile), which builds a container
suitable for running as a Kubernetes CronJob (when supplied with the
appropriate environment variables).  The container can also be found in
[Packages](./pkgs/container/influx-bucket-mapper).

## License

The InfluxDB Bucket Mapper is licensed under the [MIT License](./LICENSE).


