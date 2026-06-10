# CSDM 5 CMDB sample data for a typical Japanese enterprise

This sample models a mid-sized Japanese manufacturer and distributor, **Contoso Japan Manufacturing Co., Ltd. (コンテック日本製造株式会社)**, using the CSDM 5 concepts documented in this repository.

## Repository findings used for this sample

- CSDM is the model to follow when setting up ServiceNow products and applications; CSDM standards help ensure CIs and relationships live in the correct CMDB tables.
- Design & Planning contains non-operational records such as Business Capability `[cmdb_ci_business_capability]`, Business Application `[cmdb_ci_business_app]`, and Information Object `[cmdb_ci_information_object]`.
- In CSDM 5, a Service Instance was called an Application Service before CSDM v5 and is stored in `[cmdb_ci_service_auto]`; discovered or manually created mapped application services use `[cmdb_ci_service_discovered]`.
- Service Delivery contains operational records such as Technology Management Service `[cmdb_ci_service_technical]`, Technology Management Offering `[service_offering]` with Service Classification = Technical Service, Dynamic CI Group `[cmdb_ci_query_based_service]`, and Service Instance `[cmdb_ci_service_auto]` with Service Classification = Application Service.
- Business services are stored in `[cmdb_ci_service_business]`, and business service offerings are `[service_offering]` records with Service Classification = Business Service.
- The important CSDM relationship between a Business Application and a Service Instance is **Consumes::Consumed by**. The CSDM data foundation dashboard explicitly flags app services missing business app relationships, business apps missing app service relationships, and app-service-to-business-app relationships that are not Consumed by.
- Service Instance to discovered component associations can be represented with Service Configuration Item Associations `[svc_ci_assoc]`.

## Excel workbook

The generated `.xlsx` file is intentionally not committed. To create a local Excel workbook for preview, run:

```bash
python3 samples/csdm5-japanese-enterprise-cmdb/generate_workbook.py
```

The generated workbook contains one worksheet for each CSV import file, with the header row frozen and filters enabled.

## Intended usage

These CSV files are intentionally small but realistic enough for demos, training, import-set exercises, and relationship discussions. They are not an official ServiceNow store application or an exhaustive production implementation.

Import in this order if you want to preserve references by the provided `u_key` values:

1. `01_foundation_core.csv`
2. `02_business_capabilities.csv`
3. `03_business_applications.csv`
4. `04_business_services.csv`
5. `05_technical_services.csv`
6. `06_service_offerings.csv`
7. `07_service_instances.csv`
8. `08_infrastructure_cis.csv`
9. `09_cmdb_rel_ci.csv`
10. `10_svc_ci_assoc.csv`

## Scenario design notes

The sample reflects patterns common in Japanese enterprises:

- Head office in Tokyo, western Japan hub in Osaka, manufacturing plant in Nagoya, and logistics center in Fukuoka.
- Mix of global SaaS, domestic SaaS, on-premises ERP/MES, and public cloud front-end systems.
- Production and non-production service instances, plus a DR instance for core ERP.
- Shared platform services such as network, identity, database, backup, and monitoring.
- Clear separation between business-facing services, technology management services, service offerings, service instances, and component CIs.

## Table and relationship coverage

| File | Main target table | Purpose |
| --- | --- | --- |
| `01_foundation_core.csv` | `core_company`, `cmn_location`, `cmn_department`, `sys_user_group` | Foundational reference data used by CIs and services. |
| `02_business_capabilities.csv` | `cmdb_ci_business_capability` | Capability model for sales, manufacturing, supply chain, finance, HR, and IT operations. |
| `03_business_applications.csv` | `cmdb_ci_business_app` | Logical application portfolio records aligned to capabilities. |
| `04_business_services.csv` | `cmdb_ci_service_business` | Business-facing services consumed by employees or business units. |
| `05_technical_services.csv` | `cmdb_ci_service_technical` | Provider-focused technology management services. |
| `06_service_offerings.csv` | `service_offering` | Business and technical service offering variants with support windows and SLAs. |
| `07_service_instances.csv` | `cmdb_ci_service_auto` / `cmdb_ci_service_discovered` | Operational service instances, formerly called application services. |
| `08_infrastructure_cis.csv` | `cmdb_ci_server`, `cmdb_ci_db_instance`, `cmdb_ci_appl`, `cmdb_ci_netgear`, `cmdb_ci_query_based_service` | Discoverable application, infrastructure, and dynamic group component CIs. |
| `09_cmdb_rel_ci.csv` | `cmdb_rel_ci` | CSDM relationships between capabilities, apps, services, offerings, service instances, and CIs. |
| `10_svc_ci_assoc.csv` | `svc_ci_assoc` | Service instance to component CI associations for operational mapping. |

## Relationship conventions in this sample

- `parent_u_key` and `child_u_key` point to the stable sample keys in the other CSVs.
- `type` uses the display value of the relationship type, such as `Consumes::Consumed by`.
- `sys_class_name` is included where the import target may be a parent table.
- `environment` uses values such as `Production`, `Development`, `Test`, and `DR` for demo readability.
