# Sumologic
# Create a collector
resource "sumologic_collector" "collector" {
  name = "${var.app}-${terraform.workspace}"
}

# Create an HTTP sources
resource "sumologic_http_source" "sumo_source" {
  for_each     = var.microservices
  name         = "${each.value.name}"
  category     = "${var.app}/${terraform.workspace}/${each.value.name}"
  collector_id = sumologic_collector.collector.id
}
