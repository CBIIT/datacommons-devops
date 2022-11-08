resource "aws_secretsmanager_secret" "secrets" {
  name = "bento/${var.app}/${terraform.workspace}"

}

resource "aws_secretsmanager_secret_version" "secrets_values" {
  secret_id     = aws_secretsmanager_secret.secrets.id
  secret_string = <<EOF
    {
	  "neo4j_user": "${var.neo4j_user}",
	  "neo4j_password": "${var.neo4j_password}",
	  "neo4j_ip": "${var.neo4j_ip}",
	  "mysql_user": "${var.mysql_user}",
	  "mysql_password": "${var.mysql_password}",
	  "mysql_database": "${var.mysql_database}",
	  "mysql_host": "${var.mysql_host}",
	  "es_host": "${var.es_host}",
	  "cookie_secret": "${var.cookie_secret}",
	  "indexd_url": "${var.indexd_url}",
	  "sumo_collector_endpoint": "${var.sumo_collector_endpoint}",
	  "sumo_collector_token_frontend": "${var.sumo_collector_token_frontend}",
	  "sumo_collector_token_backend": "${var.sumo_collector_token_backend}",
	  "sumo_collector_token_files": "${var.sumo_collector_token_files}",
	  "sumo_collector_token_users": "${var.sumo_collector_token_users}",
	  "sumo_collector_token_auth": "${var.sumo_collector_token_auth}"
	}
EOF
}