# Datadog monitoring scripts

## remove_slack_tags.py: hide the "Tags" section in Slack alerts

Datadog's Slack integration adds a **Tags** section (for example
`check_type:browser, project:cbioportal, tier:dev`) to every alert it posts.
That section is controlled by each Slack channel's display settings in the
Datadog Slack integration, not by the monitor message.

`remove_slack_tags.py` sets `display.tags = false` on each channel you list.
It keeps the channel's other settings (`message`, `notified`, `snapshot`,
`mute_buttons`) exactly as they are. It never changes the monitors or their
tags; we still use those tags for filtering and routing.

For each channel it:
1. Reads and prints the current settings (GET).
2. Sets only `tags` to `false`.
3. Saves the change (PATCH).
4. Reads the settings again and confirms that `tags = false` and nothing else changed.

It retries rate-limit (429) and server (5xx) errors with backoff. At the end
it prints how many channels were updated, already correct, or failed.

### Requirements

- Python 3 with `requests` (`pip install -r requirements.txt`)
- `DD_API_KEY`: a Datadog API key.
- `DD_APP_KEY`: a Datadog application key. **The user who owns this key
  needs the "Integrations Manage" permission (`integrations_manage`).**
  Without it the script fails with HTTP 403.
- `DD_SITE`: defaults to `ddog-gov.com` (Datadog for Government), so
  requests go to `https://api.ddog-gov.com`.
- `SLACK_ACCOUNT_NAME` or `--account`: the Slack account name as shown
  under Datadog → Integrations → Slack (ours is `Expand_Data_Commons`).

Never commit API or application keys. Export them in your shell or load
them from your secrets store.

### Channel list

Pass channels with `--channels <file>` (one per line), `--channel <name>`
(repeatable), or both. Each of these forms works:

```
ccdi-subprod-cbio
#ccdi-subprod-cbio
Expand_Data_Commons-ccdi-subprod-cbio
```

The last form is the `Slack_Channel` value from the CSV (the
`@slack-<account>-<channel>` handle without the `@slack-`).
[`channels.txt`](channels.txt) lists every valid alert channel in
`FNL-Monitoring-List-datadog.csv`. Lines starting with `# ` (hash and a
space) are comments.

### Usage

```bash
cd monitoring/scripts/datadog
export DD_API_KEY=...
export DD_APP_KEY=...
# export DD_SITE=ddog-gov.com   # default

# Preview: shows current and new settings, changes nothing
python3 remove_slack_tags.py --account Expand_Data_Commons --channels channels.txt --dry-run

# Apply
python3 remove_slack_tags.py --account Expand_Data_Commons --channels channels.txt

# A single channel
python3 remove_slack_tags.py --account Expand_Data_Commons --channel ccdi-subprod-cbio
```

The script exits with `0` when every channel ends with tags off, `1` if any
channel failed, and `2` for bad arguments or missing keys.

### Errors

| Status | Meaning | Fix |
|--------|---------|-----|
| 401 | Bad API or application key, or keys from a different site | Check `DD_API_KEY`, `DD_APP_KEY` and `DD_SITE` |
| 403 | The application key's user lacks Integrations Manage | Grant `integrations_manage`, or use another user's key |
| 404 | Unknown Slack account or channel | Check `--account` and the channel name under Datadog → Integrations → Slack |
| 429 | Rate limited | Retried automatically; re-run if it still fails |

### What it doesn't change

The "Triggered:" / "Recovered:" title and the "Display Failed Test Run"
button are always added by the Datadog Slack integration. Removing them
would require sending alerts through a Datadog Webhook to a Slack incoming
webhook instead.
