# StrIEM

🚀 A powerful open-source SIEM and security data pipeline management toolkit

## Overview

StrIEM is an open-source SIEM system that leverages modern data engineering tools and open standards to provide security monitoring capabilities, data processing / normalization, and data routing.

StrIEM combines and builds on:
- [Vector](https://vector.dev)
- [Sigma](https://sigmahq.io)
- [OCSF](https://ocsf.io)

### Key Features

- 🔄 **Vector-powered Data Pipelines**: Uses [Vector](https://vector.dev) by Datadog for robust log collection and processing
- 🛡️ **Sigma Rules Integration**: Detection engine using industry-standard [Sigma](https://sigmahq.io) rules
- 📋 **OCSF Normalization**: Events are transformed and normalized to [OCSF](https://ocsf.io) for consistent analysis, simplified querying, easier correlation across sources, and reduced storage complexity
- 💾 **Enterprise Storage Options**: Store security events in Parquet format, with support for local storage, Snowflake, AWS Security Lake, and various data lake solutions. Search, analyze & investigate with DuckDB, Apache Arrow, Snowflake SQL, AWS Athena & more

- 🔌 **Integrations**:
  - AWS CloudTrail
  - Google Cloud / Google Workspace
  - GitHub Enterprise
  - Okta
  - ...and anything else supported by [Vector](https://vector.dev/components/)

## Quick Start

1. Install the configuration utility:
    ```bash
    pip install striem-configure
    ```

    (or, from this repository, `pip install .`)

2. Generate your configuration, and follow the prompts:
    ```bash
    striem-configure
    ```

3. Launch StrIEM:
    ```bash
    docker-compose up -d
    ```

## Configuration

The configuration utility will help you set up:

- Data sources and authentication
- Detection rules and alerts
- Storage configuration

The utility creates a directory containing `docker-config.yaml` and several subdirectories:
- `assets/schema`: OCSF parquet schema, generated from [crowdalert/ocsf-parquet](https://github.com/crowdalert/ocsf-parquet)
- `assets/detections`: Sigma detection rules. You will be prompted if you'd like to download the open source rules from [SigmaHQ](https://github.com/sigmahq/sigma), and you can add your own
- `assets/vrl`: [VRL transforms](https://vector.dev/docs/reference/vrl/) for normalizing data in to OCSF. Retrieved from [crowdalert/ocsf-vrl](http://github.com/crowdalert/ocsf-vrl)
- `config/striem.yaml`: configuration for StrIEM Store, if non-Vector sources have been configured
- `config/vector`: Directory containing Vector config files
- `config/vector/static`: Contains Vector configuration specific to StrIEM
- `data`: The output directory for post-processed & normalized data. Hive partitioned by date. This is where the Parquet database lives.

## Architecture

StrIEM consists of two major pieces:

- **Vector**: Handles log ingestion, transformation, and routing
- **StrIEM State**: A helper for the SIEM functions not currently supported by or outside the conceptual model of Vector: detections, correlations, enrichments, trigger actions (SOAR playbooks), and database generation (ie, Parquet). Also ingests data from sources not currently in Vector (eg, Okta)

striem-configure (this repository) generates a set of configuration files creating a security data pipeline with Vector. Each step of the pipeline follows a naming schema so you can add your own sources, transforms and sinks:

- `source-<source type>-<source id>`: The initial ingest point for data
- `logsource-<source type>-<source id>`: events will have a `%logsource` field added to metadata corresponding to the [Sigma Log Source](https://sigmahq.io/docs/basics/log-sources.html). StrIEM uses the `category`, `product` and `service` fields as filters if they are present, ignoring Sigma rules that do not apply to this log source
    
    Transforms should also add a `%source_id` metadata field equal to the source id for identitfication by downstream consumers matching on wildcards ( ie, Vector components configured with `inputs: [logsource-*]` )
- `ocsf-<source type>-<source id>`: events will be normalized to valid [OCSF](https://ocsf.io)

    Events from `ocsf-*` are then sent to StrIEM State to be written to Parquet files
- `actions-<action type>`: Events from this data stream are OCSF normalized data filtered by type, indicating some action

    For instance, a Vector sink configuration can consume `actions-alert` as it's `inputs` parameter to send all detection matches to it's target. A Vector configuration for writing alerts to the console might look like the following:

    ```yaml
    sinks:
        console-alerts:
        type: console
        encoding:
            codec: json
        inputs: ["actions-alert"]
    ```
## Contributing

We welcome contributions! Submit your PR's, Issues, Suggestions or Enhancements!

## License

Licensed under MPL-2.0. See LICENSE file for details.

---

Built with ❤️ by CrowdAlert, Inc.
