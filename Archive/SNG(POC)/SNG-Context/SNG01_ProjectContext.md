# Project Context

## Application
- **Name:** UeLS-zentras On-call System (Pikettsystem 2)
- **Type:** Web Application
- **Domain:** Infrastructure / Alarm Management & On-call Duty Scheduling (Swiss Federal Roads / FEDRO)

## Tech Stack
- **Frontend:** Web browser-based UI (SA-CH standard compliant)
- **Backend:** Web application running on a virtual machine alongside UeLS-zentras, active-passive cluster with failover
- **Database:** Local database for storing system assets, alarm data, SMS/pager messages
- **API Type:** Dedicated interfaces to UeLS-zentras; F24 eCall HTTP/HTTPS interface for SMS/pager message transmission
- **External Integration:** F24 Schweiz AG eCall interface for SMS and pager message delivery

## Environment
- **Dev URL:** [NEEDS CLARIFICATION]
- **Staging URL:** [NEEDS CLARIFICATION]
- **Prod URL:** Deployed at two locations (Stans and Senti) in active-passive cluster configuration

## Architecture Overview
- The on-call system is an independent application running alongside UeLS-zentras
- Communicates with UeLS-zentras via dedicated interfaces
- Runs within an active-passive cluster with failover to prevent duplicate alarm sending
- Only one instance runs at any given time; failover handles availability
- UeLS-zentras automatically synchronizes system assets with the on-call system

## User Roles
- Uses the same user roles and authorization rights as defined in UeLS-zentras (LDAP-based authentication)
- Authorization settings determine which functions a logged-in user can access
- Users can log in directly or via SSO service from the UeLS application

## Key Modules / Views
1. **Planning View** – Basic on-call schedule planning and period management
2. **Configuration View** – Regions, pause settings, alarm delays, shipping delays, system activation, on-call participants, alarm media
3. **Appointment View** – Absence planning and public holiday configuration
4. **Message View** – On-call alarms, delayed alarms, SMS/pager messages, shipping list, internal alarms, measurements, suppressed data points, test messages
5. **Evaluation View** – Overall planning reports, on-call region reports, on-call participant reports
6. **System Configuration View** – Objects, system computers, assets, data point groups, data points, communication
7. **Document View** – Stored help and user documentation

## Key Constraints
- Only one on-call system instance can be active at a time to prevent duplicate alarm messages
- SMS/pager message maximum length is 154 characters (160 with transmission time appended)
- Message format: `UeLS-Z <Alarm log and message text>`
- SMS and pager messages are transmitted via the F24 eCall interface (contract with F24 Schweiz AG)
- Region names limited to 20 alphanumeric characters and cannot be edited after initial entry
- Alarm medium identification cannot be edited after initial entry
- System identifications cannot be edited after initial entry
- Authorization-dependent functionality – not all features visible to all users

## Document Reference
- **Document:** 6.3 Pikettsystem 2 en-US.pdf
- **Version:** 0.2
- **Date:** January 16, 2026
- **Author:** Sopra Steria AG
- **Project Author:** Nay Engineering AG
- **Status:** Draft
- **Pages:** 67
- **Dossier No.:** 900568
