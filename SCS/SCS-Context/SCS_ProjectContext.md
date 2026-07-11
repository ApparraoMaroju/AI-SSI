# Project Context

## Application
- **Name:** SCS Core (Sopra Crypto Solutions)
- **Type:** Web / API
- **Domain:** Banking / FinTech / Cryptocurrency

## Tech Stack
- **Frontend:** Web UI (customer and bank user interfaces)
- **Backend:** AWS EKS (Kubernetes microservices architecture)
- **Database:** AWS DocumentDB, S3, EFS
- **API Type:** REST API
- **Cloud Infrastructure:** AWS (EKS, Cognito, API Gateway, WAF, GuardDuty, Secrets Manager, CloudWatch)
- **Container Orchestration:** Kubernetes with Cluster Autoscaler and Horizontal Pod Autoscaler (HPA)

## Environment
- **Dev URL:** [NEEDS CLARIFICATION - Not specified in requirements]
- **Staging URL:** [NEEDS CLARIFICATION - Not specified in requirements]
- **Prod URL:** [NEEDS CLARIFICATION - Not specified in requirements]

---

## Diagrams

### Figure 1 - Overview of the Solution
![Overview of the Solution](images/image_1.png)

### Figure 2 - Capability Map
![Capability Map](images/image_2.png)

### Figure 3 - Subledger Concepts
![Subledger Concepts](images/image_3.png)

### Figure 4 - Application Architecture
![Application Architecture](images/image_4.png)

### Figure 5 - Deployment
![Deployment](images/image_5.png)

### Figure 6 - Link Components vs Capabilities
![Link Components vs Capabilities](images/image_6.png)

### Figure 36 - Architecture Principles
![Architecture Principles](images/image_48.png)

### Figure 37 - Technology Stack
![Technology Stack](images/image_49.png)

### Figure 38 - Current Infrastructure
![Current Infrastructure](images/image_50.png)

### Figure 39 - Target Infrastructure
![Target Infrastructure](images/image_51.png)

### Figure 40 - Cluster Autoscaler
![Cluster Autoscaler](images/image_52.png)

### Figure 41 - Horizontal Pod Autoscaler
![Horizontal Pod Autoscaler](images/image_53.png)

---

## Architecture Overview
- **Deployment:** Private subnets within AWS VPC with EKS workloads
- **Security:** Multi-layered approach including Security Groups, NACLs, AWS Network Firewall, Kubernetes Network Policies, Service Mesh (Istio)
- **Authentication:** AWS Cognito with OAuth2, MFA, enterprise SSO integration
- **Encryption:** TLS 1.3 for data in transit, AWS KMS for data at rest

## External Integrations
- **Custodians:** Fireblocks, Taurus (for blockchain interactions and security)
- **Order Management System (OMS):** Wyden
- **Exchange Venues:** Kraken, Coinbase
- **KYT/AML Provider:** Chainalysis
- **Core Banking System (CBS):** Integration via defined API endpoints

## Key Constraints
- All API communications must use HTTPS with TLS 1.3
- JWT tokens required for all API calls with attributes: sub, iat, exp, client, customer, role
- Idempotency management required for state-changing API endpoints
- Rate limiting and throttling enforced via AWS API Gateway and WAF
- Data encryption at rest using AWS KMS (EBS, S3, EFS, DocumentDB)
- Role-Based Access Control (RBAC) enforced at UI and API levels
- Asset-link based access control for customer resources
- Logs must not contain PII - only technical IDs allowed
- Amount formatting: 2 significant digits after decimal separator (minimum)
