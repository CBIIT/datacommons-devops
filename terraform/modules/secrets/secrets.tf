resource "aws_secretsmanager_secret" "secrets" {
  for_each    = var.secret_values
  name        = each.value.secretKey
  description = ""
}

resource "aws_secretsmanager_secret_version" "secrets_value" {
  for_each      = var.secret_values
  secret_id     = aws_secretsmanager_secret.secrets[each.key].id
  secret_string = jsonencode(each.value.secretValue)
}
