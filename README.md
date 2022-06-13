# influx-restart-mapper

## Restartmapper

Therefore: [restartmapper](./restartmapper).  This is a Python 3 script
which queries the buckets in an organization to find K8s applications,
and creates any restart buckets, tasks, and alerts for them that don't
yet exist.

### Restartmapper Configuration

[restartmapper](./restartmapper) expects the same environment variables as
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
[Packages](./pkgs/container/influx-restart-mapper).

## License

The InfluxDB Restart Mapper is licensed under the [MIT License](./LICENSE).


