#Sumologic
#Createacollector
resource "sumologic_collector" "collector" {
  name = "${var.resource_prefix}-${var.service}"
}

#CreateanHTTPsources
resource "sumologic_http_source" "sumo_source" {
  for_each     = var.microservices
  name         = each.value.name
  category     = "${var.program}/${terraform.workspace}/${var.app}/${each.value.name}"
  collector_id = sumologic_collector.collector.id
}