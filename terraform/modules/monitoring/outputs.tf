#output "frontend_source_url" {
#  value       = regex(".*/(.*)", sumologic_http_source.frontend_source.url)[0]
#  description = "frontend source url"
#}
#output "backend_source_url" {
#  value       = regex(".*/(.*)", sumologic_http_source.backend_source.url)[0]
#  description = "backend source url"
#}
#output "files_source_url" {
#  value       = regex(".*/(.*)", sumologic_http_source.files_source.url)[0]
#  description = "files source url"
#}

output "sumo_source_urls" {
  value       = {for k, v in sumologic_http_source.sumo_source: k => regex(".*/(.*)", sumologic_http_source.backend_source.url)[0]}
  description = "map of name, source url for sumo collectors"
}