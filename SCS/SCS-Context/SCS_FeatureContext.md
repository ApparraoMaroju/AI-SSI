# Feature Context: SCS Core Platform

## Overview
SCS Core is a banking solution that enables banks to deploy a crypto-account offering for their customers. It provides end-to-end management of digital asset accounts, orders (buy/sell), transactions (deposits/withdrawals), and integration with custodians, order management systems, and exchange venues.

## User Stories
- As a bank customer, I want to create a crypto-account so that I can hold and manage digital assets
- As a bank customer, I want to buy digital assets so that I can invest in cryptocurrencies
- As a bank customer, I want to sell digital assets so that I can convert them to fiat currency
- As a bank customer, I want to deposit digital assets so that I can transfer them to my account
- As a bank customer, I want to withdraw digital assets so that I can transfer them to external addresses
- As a bank user, I want to manage customer accounts so that I can provide support and oversight
- As a bank user, I want to view dashboards so that I can monitor bank positions and operations

---

## Process Flow Diagrams

### Figure 7 - Customer Request to Open a Digital Asset Account
![Account Opening Request](images/image_7.png)

### Figure 8 - Customer Accesses a Digital Asset Dashboard
![Digital Asset Dashboard](images/image_8.png)

### Figure 9 - Customer Logs In
![Customer Login](images/image_9.png)

### Figure 10 - Initiation of the Buying Order
![Buying Order Initiation](images/image_10.png)

### Figure 11 - Execution of a Buying Order
![Buying Order Execution](images/image_11.png)

### Figure 12 - Initiation of a Selling Order
![Selling Order Initiation](images/image_12.png)

### Figure 13 - Execution of a Selling Order
![Selling Order Execution](images/image_13.png)

### Figure 14 - New Deposit Address Request
![Deposit Address Request](images/image_14.png)

### Figure 15 - Deposit Receipt
![Deposit Receipt](images/image_15.png)

### Figure 16 - Whitelisted Address Creation
![Whitelisted Address Creation](images/image_16.png)

### Figure 17 - Customer Initiates Withdrawal
![Withdrawal Initiation](images/image_17.png)

### Figure 18 - Withdrawal Execution
![Withdrawal Execution](images/image_18.png)

### Figure 19 - Internal Withdrawal Execution
![Internal Withdrawal Execution](images/image_19.png)

### Figure 20 - Account-based Withdrawal Execution
![Account-based Withdrawal](images/image_20.png)

### Figure 21 - Batch Execution for UTXO Assets
![UTXO Batch Execution](images/image_21.png)

### Figure 22 - Customer Request Cancellation of an Order
![Order Cancellation](images/image_22.png)

### Figure 23 - Continuous Monitoring
![Continuous Monitoring](images/image_23.png)

### Figure 24 - Travel Rule Data Management
![Travel Rule Management](images/image_24.png)

### Figure 25 - KYT Task Management
![KYT Task Management](images/image_25.png)

### Figure 26 - Price Management
![Price Management](images/image_26.png)

### Figure 27 - Order Integration Module
![Order Integration Module](images/image_27.png)

### Figure 28 - Limit Update Management
![Limit Update Management](images/image_28.png)

### Figure 29 - Tax-related Data Computation
![Tax Data Computation](images/image_29.png)

### Figure 30 - Retrieve Tax Reports / Statement Report Generation
![Tax Reports](images/image_30.png)

### Figure 31 - Create Bank Position
![Create Bank Position](images/image_31.png)

### Figure 32 - Document Upload for KYT Issue
![KYT Document Upload](images/image_32.png)

---

## Status Flow Diagrams

### Figure 33 - Buy/Sell Order Statuses
![Order Statuses](images/image_45.png)

### Figure 34 - Withdrawal Statuses
![Withdrawal Statuses](images/image_46.png)

### Figure 35 - Deposit Statuses
![Deposit Statuses](images/image_47.png)

---

## Acceptance Criteria
- [ ] Customers can create only one crypto-account per customer
- [ ] All orders must pass pre-trade validation (limits, eligibility, balance checks)
- [ ] Transactions must be screened for KYT/AML compliance
- [ ] API calls must include valid JWT tokens with required attributes
- [ ] Simulation mode available for all state-changing operations
- [ ] Idempotency enforced using Idempotency-Key header
- [ ] Role-based access control enforced for all operations

## API Endpoints (if applicable)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /accounts | Create account opening request |
| POST | /orders | Create buy/sell order |
| GET | /orders | Retrieve orders |
| POST | /transactions | Create deposit/withdrawal transaction |
| GET | /transactions | Retrieve transactions |
| POST | /bank-user-access-controls | Verify bank user access to customer |

## UI Elements
- Customer Web Interface (login, account dashboard, order placement, transaction history)
- Bank User Web Interface (customer management, dashboards, monitoring)
- Role-based page access control

## Validation Rules
| Field | Rule |
|-------|------|
| JWT Token | Required for all API calls with valid signature |
| Idempotency-Key | Required for state-changing operations |
| simulationIndicator | Optional query parameter (true/false) |
| Customer ID | Must match JWT customer attribute for customer operations |
| Account ID | One account per customer limit |
| Trade Limits | Must be within configured limits |
| Withdrawal Limits | Must be within configured limits |
| Digital Asset | Must be in configured/enabled digital assets list |

## Error Messages
| Code | Message |
|------|---------|
| 400 | Bad Request - Invalid input data |
| 401 | Unauthorized - Invalid or missing JWT token |
| 403 | Forbidden - Access denied based on role or asset-link control |
| 404 | Not Found - Resource does not exist |
| 206 | Partial Content - Results limited due to pagination cap |
| 5xx | Server Error - Technical issues (DB unavailable, external service error) |

## Business Error Codes
| Return Code | Description |
|-------------|-------------|
| ACCOUNT_ALREADY_EXIST | Customer already has an account |
| CUSTODIAN_NOT_AVAILABLE | Fireblocks/Taurus API call failed |
| [NEEDS CLARIFICATION] | Full list of return codes not specified in requirements |

## Security Features
- Multi-Factor Authentication (MFA)
- OAuth2-based access
- JWT token validation
- Role-Based Access Control (RBAC)
- Asset-link based access control
- Non-repudiation via Authorization-Reference header
- TLS 1.3 encryption
