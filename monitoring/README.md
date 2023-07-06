## Newrelic Monitoring Scripts
The Newrelic Monitoring Scripts are used to create new alert configurations far a project based on what has been entered into the csv spreadsheet in this folder. This will allow for consistent monitoring and alerting across FNL projects.

## Monitor Types
The scripts create two different types of alerts:

- Infrastructure alerts: these monitor metrics pulled from AWS resources and depend on newrelic integrations with the AWS account being monitored and Newrelic Fargate containers to collect the relevant metrics.

- Synthetic alerts: these monitor an application endpoint.

## Spreadsheet Fields
The CSV spreadsheet is read by the monitoring scripts and controls which monitors are created.

The fields in the spreadsheet are:

- Project_Name: A descriptive name of the project. Used to identify the project further than just its acronym.
- Project_Acronym: The acronym used for the project.
- Program: The program the project falls under (crdc or ccdi).
- Tier: The application tier being configured.
- Endpoint_Name: The endpoint type of the URL entered.
- URL: The endpoint URL being configured.
- Endpoint_Query: The query to pass to the endpoint, if relevant. This field only applies to scripted API monitors and is used with the API endpoint type.
- Private_Location: Whether to use the FNL private location as defined in Newrelic. This is required for lower tiers.
- Slack_Channel: The slack channel ID used for alerting. NOTE: this is not the channel name, it is the unique ID assigned to the channel.
- Monitored_Resources: A comma separated list of resources to be monitored in addition to the Synthetics URL monitors. The choices for these are:
     - alb
     - opensearch
     - fargate