# Testing Context

## Scope
- **In Scope:** 
  - Account management (creation, retrieval, status updates)
  - Order management (buy, sell, convert digital assets)
  - Transaction management (deposit, withdrawal)
  - API security (JWT validation, authentication, authorization)
  - Role-Based Access Control (RBAC)
  - Asset-link based access control
  - Simulation mode functionality
  - Idempotency handling
  - Error handling and response validation
  - Input validation and data sanitization
  - Rate limiting and throttling
  - Integration with external services (custodians, OMS, exchange venues)
  
- **Out of Scope:** 
  - Core Banking System (CBS) implementation
  - Bank-specific authentication provider implementation
  - Exchange venue internal logic
  - Custodian internal security mechanisms
  - Production infrastructure deployment

---

## Reference Diagrams for Testing

### Architecture & Infrastructure Reference

#### Figure 4 - Application Architecture
![Application Architecture](images/image_4.png)

#### Figure 37 - Technology Stack
![Technology Stack](images/image_49.png)

#### Figure 39 - Target Infrastructure
![Target Infrastructure](images/image_51.png)

### Status Flow Diagrams (for Test Case Design)

#### Figure 33 - Buy/Sell Order Statuses
![Order Statuses](images/image_45.png)

#### Figure 34 - Withdrawal Statuses
![Withdrawal Statuses](images/image_46.png)

#### Figure 35 - Deposit Statuses
![Deposit Statuses](images/image_47.png)

### Process Flow Diagrams (for Integration Testing)

#### Figure 11 - Execution of a Buying Order
![Buying Order Execution](images/image_11.png)

#### Figure 13 - Execution of a Selling Order
![Selling Order Execution](images/image_13.png)

#### Figure 18 - Withdrawal Execution
![Withdrawal Execution](images/image_18.png)

#### Figure 15 - Deposit Receipt
![Deposit Receipt](images/image_15.png)

#### Figure 25 - KYT Task Management
![KYT Task Management](images/image_25.png)

---

## Test Data
| Data Type | Value | Purpose |
|-----------|-------|---------|
| Valid JWT Token | Token with valid sub, iat, exp, client, customer, role | Happy path authentication |
| Expired JWT Token | Token with past exp timestamp | Negative - token expiration test |
| Invalid JWT Token | Malformed/corrupted token | Negative - security test |
| Valid Customer ID | [NEEDS CLARIFICATION] | Account operations |
| Valid Account ID | [NEEDS CLARIFICATION] | Transaction/Order operations |
| Valid Idempotency-Key | UUID format | Idempotency test |
| Duplicate Idempotency-Key | Same UUID as previous request | Idempotency validation |
| Valid Digital Asset | BTC, ETH, SHIB | Order creation tests |
| Invalid Digital Asset | Unsupported asset code | Negative - validation test |
| Amount within limits | Based on configured trade/withdrawal limits | Happy path |
| Amount exceeding limits | Above configured limits | Negative - limit validation |
| simulationIndicator=true | Query parameter | Simulation mode test |
| simulationIndicator=false | Query parameter | Normal execution test |

## Test Environment
- **Browser:** Chrome / Firefox / Safari
- **Device:** Desktop
- **OS:** Windows / macOS / Linux
- **API Testing:** REST client (Postman, Insomnia, or equivalent)
- **Cloud Environment:** AWS (EKS-based)

## Dependencies
- AWS Cognito must be configured for authentication
- AWS API Gateway must be running
- EKS cluster must be operational with microservices deployed
- DocumentDB must have seed data
- Mock services for CBS API endpoints (for testing)
- Custodian sandbox/test environment (Fireblocks, Taurus)
- OMS test environment (Wyden)

## Known Issues
- [NEEDS CLARIFICATION] - No known issues specified in requirements

## Security Testing Requirements
- TLS 1.3 enforcement validation
- JWT token manipulation attempts
- SQL injection and XSS attack prevention (WAF rules)
- CORS policy enforcement
- Rate limiting effectiveness
- Unauthorized access attempts (cross-customer access)

## Performance Considerations
- Rate limiting: Requests per second limits enforced at API Gateway
- Burst capacity management
- Horizontal Pod Autoscaler (HPA) scaling behavior
- Cluster Autoscaler response time

## Logging & Monitoring Verification
- CloudWatch logs capture API requests and responses
- No PII in logs (only technical IDs)
- Error codes properly masked in client responses
- Detailed errors logged internally for debugging
