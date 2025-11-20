# TODO: Instana APM Synthetic Data Generator v1.4.0 - Exhaustive API Coverage

## Overview
Implement the remaining ~40% of Instana API surfaces to achieve 100% coverage, focusing on Infrastructure, Application enhancements, Global/Infra Alerts, Events, Host Agent, and User Management.

## Phase 1: Infrastructure Generators (Week 1)
- [ ] Add gen_infrastructure_entity() to generators.py
- [ ] Create scripts/generate_infrastructure_entities.py
- [ ] Add gen_infrastructure_metrics() to generators.py
- [ ] Create scripts/generate_infrastructure_metrics.py
- [ ] Add gen_infra_topology() to generators.py
- [ ] Create scripts/generate_infra_topology.py

## Phase 2: Application Enhancements (Week 2)
- [ ] Add gen_application_metrics() to generators.py
- [ ] Create scripts/generate_application_metrics.py
- [ ] Add gen_application_traces() to generators.py
- [ ] Create scripts/generate_application_traces.py
- [ ] Add gen_app_topology() to generators.py
- [ ] Create scripts/generate_app_topology.py
- [ ] Add gen_app_settings() to generators.py
- [ ] Create scripts/generate_app_settings.py

## Phase 3: Alert & Event Systems (Week 3)
- [ ] Add gen_global_alert_config() to generators.py
- [ ] Create scripts/generate_global_alert_configs.py
- [ ] Add gen_infra_alert_config() to generators.py
- [ ] Create scripts/generate_infra_alert_configs.py
- [ ] Add gen_event_settings() to generators.py
- [ ] Create scripts/generate_event_settings.py
- [ ] Add gen_host_agent_status() to generators.py
- [ ] Create scripts/generate_host_agent_status.py
- [ ] Add gen_events() to generators.py
- [ ] Create scripts/generate_events.py

## Phase 4: User Management & Integration (Week 4)
- [ ] Add gen_user_roles() to generators.py
- [ ] Create scripts/generate_user_roles.py
- [ ] Add gen_api_tokens() to generators.py
- [ ] Create scripts/generate_api_tokens.py
- [ ] Add gen_access_catalogs() to generators.py
- [ ] Create scripts/generate_access_catalogs.py
- [ ] Update scripts/generate_instana_all.py to include all new scripts

## Phase 5: Validation & Testing (Week 5)
- [ ] Add validation functions to validate_all.py for new data types
- [ ] Ensure cross-file consistency (infra metrics vs entities, traces vs services, etc.)
- [ ] Update TODO.md to mark v1.4.0 as completed
- [ ] Update README_INSTANA.md with new capabilities
- [ ] Update CHANGELOG.md with v1.4.0 features
- [ ] Test dashboard/alerting integration with new data types

## Success Criteria
- [ ] All new scripts generate valid JSONL files in data/instana/
- [ ] validate_all.py passes for all new data types
- [ ] 100% Instana API surface coverage achieved
- [ ] Performance < 10s for full generation
- [ ] Memory usage < 500MB

## Notes
- Follow existing patterns in generators.py and scripts/
- Ensure realistic data distributions and correlations
- Maintain backward compatibility with existing data
