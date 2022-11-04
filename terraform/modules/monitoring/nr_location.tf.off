# Newrelic - private location

resource "newrelic_synthetics_private_location" "internal_location" {
 account_Id                = ${newrelic_account_id}
 description               = "private location for ${app}"
 name                      = "${app}-internal"
 verified_script_execution = true
}