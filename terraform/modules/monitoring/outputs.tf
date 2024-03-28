output "sumo_source_urls" {
  value       = { for k, v in sumologic_http_source.sumo_source : k => regex(".*/(.*)", sumologic_http_source.sumo_source[k].url) }
  description = "map of name, source url for sumo collectors"
}