## Notes on Configuration of Private Locations:

- Initial configuration for private locations needs to be done through the Newrelic UI.
- UI configuration will generate the required keys needed to connect to Newrelic.
- Once the configurations are available the private location should be defined as a service on an internal EC2 instance.


## Requirements:

The private location requires keys that will be created when the new location is defined in the Newrelic UI.

## Running the Private Location in Docker:

The private location can be run in docker using the following command:

```
docker run \
  --name Private_Location \
  -e PRIVATE_LOCATION_KEY=< KEY VALUE > \
  -d --restart unless-stopped \
  -v /var/run/docker.sock:/var/run/docker.sock:rw \
  newrelic/synthetics-job-manager
```

## Running the Private Location as a Service:

To enable and run the private location as a systemd service the foolowing service files must be created using the provided templates. These will need to be edited to include connection info that is defined when creating a new location in the Newrelic UI:

```
/etc/systemd/system/newrelic-private-location.service
/etc/systemd/system/newrelic.private
```

To enable the service the following commands should be run:

```
systemctl daemon-reload
systemctl enable newrelic-private-location.service
systemctl start newrelic-private-location.service
```

Verify the service is running:

```
systemctl status newrelic-private-location.service
```

The service will start a docker container that will connect back to Newrelic, this should be verified to ensure it is running:

```
docker ps
```

Once these items have been verified the private location should be shown as available in the Newrelic UI.