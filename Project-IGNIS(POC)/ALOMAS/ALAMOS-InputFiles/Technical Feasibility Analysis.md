# Technical Feasibility Analysis — Multiple Inbound TLS Certificates for Adapter

---

# 1. Executive Summary

The Event Integration Adapter receives inbound HTTPS requests from multiple external source systems such as IPL, UCRI, and future partners.

A requirement was raised to present a different inbound server certificate to each source system while:

- Using the same hostname.
- Using the same IP address.
- Using the same HTTPS port.
- Selecting the certificate after validating the caller certificate and key.

This exact requirement is **not achievable**.

This is not a limitation of Quarkus, Vert.x, Java, or any implementation framework. It is a **TLS protocol constraint**:

> The server must select and send its server certificate immediately after receiving the TLS ClientHello, before HTTP headers, URI, payload, business identity, authorization tokens, or the client's own certificate are available.

## Recommendation Hierarchy

1. Clarify with the customer whether a single shared server certificate for all inbound HTTPS communication is acceptable.
2. If accepted, use one shared server certificate while authenticating callers using:
   - Mutual TLS (mTLS).
   - Client certificates.
   - Application-level authorization mechanisms.

---

# 2. Why We Need This Change

The Adapter currently supports inbound HTTPS integrations and must continue supporting IPL while onboarding UCRI and future external systems.

Each partner may have different certificate and trust requirements. The goal is to secure inbound traffic without fragmenting the business application.

The business objective is valid:

- Secure inbound communication.
- Prove the Adapter identity to external partners.
- Validate which external system is calling.

However, the proposed mechanism conflicts with TLS handshake timing.

The requirement:

> Select a different server certificate after validating the caller certificate/key while all partners use the same endpoint.

cannot be implemented using standard TLS behavior.

---

# 3. Existing Architecture

## Current Configuration

```properties
quarkus.http.host={{BIND_ADDRESS}}

quarkus.tls.http-server.key-store.pem.0.cert=config/ssl/{{SSL_CERT_FILE}}

quarkus.tls.http-server.key-store.pem.0.key=config/ssl/{{SSL_KEY_FILE}}

quarkus.http.ssl-port={{BIND_PORT_HTTPS}}

quarkus.http.tls-configuration-name=http-server
```

## Current Limitation

- One Quarkus HTTP server is bound to one TLS configuration by default.
- Every inbound HTTPS request on that listener receives the same server certificate.
- Application controllers and business logic execute only after TLS establishment.

Certificate selection happens before application processing.

---

# 4. Requirement

## Business Requirement

Continue supporting IPL while onboarding UCRI and future source systems.

The desired outcome:

- Secure all inbound requests.
- Validate caller identity.
- Maintain interoperability with external systems.

## Strict Technical Requirement

Automatically present the correct server certificate during the TLS handshake, ideally only after:

1. Validating the caller certificate.
2. Identifying the calling system.

Constraints:

- Same hostname.
- Same IP address.
- Same HTTPS port.

---

# 5. TLS Constraint

TLS server certificate selection happens during the TLS handshake.

Therefore certificate selection cannot depend on:

- HTTP headers.
- Request URI.
- Request payload.
- Authorization tokens.
- Business routing logic.

If all partners use the same:

- Hostname.
- IP address.
- Port.

then TLS has no reliable differentiator for selecting different certificates.

---

# 6. Problem Statement

## 6.1 Current Setup

- One Adapter application receives inbound HTTPS requests.
- Multiple systems connect:
  - IPL.
  - UCRI.
  - Future partners.
- Each system may expect a different server certificate.
- All clients connect using the same endpoint.

Example:

```text
https://adapter.company.com:8443
```

---

## 6.2 Goal

Automatically present the correct server certificate during TLS handshake without changing:

- Hostname.
- IP address.
- HTTPS port.

---

## 6.3 Why This Is Not Achievable

The expected flow assumes:

1. Receive request.
2. Identify caller.
3. Select certificate.
4. Respond.

Actual TLS behavior:

1. Establish secure channel.
2. Exchange certificates.
3. Complete TLS handshake.
4. Receive HTTP request.
5. Execute business logic.

The server certificate is part of establishing the secure channel, not part of the application request processing.

---

# 7. TLS Handshake Sequence

Simplified TLS flow:

```
Client                         Server
  |                              |
  |---- TCP Connection --------->|
  |                              |
  |---- ClientHello ------------>|
  |                              |
  |<--- ServerHello + Certificate|
  |                              |
  |---- Key Exchange ---------->|
  |                              |
  |<--- Finished ---------------|
  |                              |
  |---- HTTP Request ---------->|
  |                              |
```

## Key Takeaway

The server certificate is selected during:

```
ServerHello + Certificate
```

The HTTP request exists only later.

Therefore:

- No URI.
- No headers.
- No payload.
- No authentication token.

can influence certificate selection.

---

# 8. Available Information During Certificate Selection

At certificate selection time, the server only has TLS-level information.

## Available

- Destination port.
- Local IP address.
- TLS version.
- Cipher suites.
- SNI (Server Name Indication).
- ALPN protocol negotiation.

## Not Available

- HTTP headers.
- REST endpoint.
- Request body.
- Business identity.
- Authorization token.
- Client certificate.

The client certificate has not yet been exchanged.

---

# 9. Why the Requirement Is Not Achievable

If IPL and UCRI connect using:

```text
Same hostname
Same IP
Same HTTPS port
```

then the TLS ClientHello messages are indistinguishable.

The server cannot determine:

```
"This is IPL"
```

versus:

```
"This is UCRI"
```

before sending the server certificate.

This limitation applies universally:

- Quarkus.
- Vert.x.
- Netty.
- Spring.
- nginx.
- Apache.
- HAProxy.
- API gateways.

It is a TLS protocol limitation.

---

# 10. Evaluated Solutions

---

# 10.1 Multiple HTTPS Ports

## Approach

Use different HTTPS listeners:

Example:

| System | Port | Certificate |
|---|---|---|
| IPL | 8443 | IPL certificate |
| UCRI | 8444 | UCRI certificate |
| Partner X | 8445 | Partner certificate |

---

## Technical Considerations

### Vert.x Lifecycle Complexity

Quarkus internally uses Vert.x.

Multiple HTTPS listeners require:

- Multiple Vert.x HTTP servers.
- Custom lifecycle handling.
- Startup sequencing.
- Shutdown management.
- Resource management.

---

### Quarkus Configuration Limitations

Quarkus is designed around a standard single HTTP/HTTPS listener model.

Supporting multiple listeners requires:

- Lower-level Vert.x APIs.
- Custom bootstrap code.
- Non-standard implementation.

---

### Increased Code Complexity

Requires:

- Additional infrastructure code.
- Custom server management.
- Increased maintenance effort.
- Higher upgrade risk.

---

### Operational Overhead

Requires coordination for:

- Firewall rules.
- Load balancers.
- Ingress configuration.
- Monitoring.
- Deployment configuration.

---

### Security Considerations

Multiple exposed ports increase:

- Attack surface.
- Security policy complexity.
- Compliance tracking effort.

---

## Verdict

✅ Technically feasible.

❌ Not recommended.

Reasons:

- Increased complexity.
- Poor scalability.
- Deviates from Quarkus best practices.
- Does not satisfy the same hostname/IP/port requirement.

---

# 10.2 Shared Server Certificate

## Approach

Use one server certificate trusted by all partners.

Caller identity is validated using:

- mTLS client certificates.
- API tokens.
- Application authorization rules.
- Partner identity mapping.

---

## Verdict

✅ Recommended.

Advantages:

- Standards compliant.
- No infrastructure changes.
- No client endpoint changes.
- Simple operational model.

Security responsibilities are separated:

| Concern | Solution |
|---|---|
| Channel encryption | Shared server certificate |
| Caller identity | Client certificate / application authentication |

---

# 11. Summary Comparison Matrix

| Option | Differentiator Required | Extra Infrastructure | Client Change | Verdict |
|---|---|---|---|---|
| Multiple HTTPS Ports | Different port | No | Yes | Feasible but not recommended |
| Shared Server Certificate | None | No | No | Recommended |

---

# 12. Business Clarification Required

Implementing multiple inbound HTTPS listeners with different certificates inside a single Quarkus application introduces significant complexity.

Although custom Vert.x implementations are possible, they:

- Increase maintenance effort.
- Require manual lifecycle management.
- Deviate from standard Quarkus patterns.
- May still not satisfy the shared endpoint requirement.

## Customer Clarification

The following question must be confirmed:

> Is it acceptable for IPL and future external systems to use the same server certificate, provided the certificate is trusted by all systems and caller identity is validated using mTLS and/or application-level authentication?

This decision determines the final architecture.

---

# 13. Recommended Approach for Adapter

For the Event Integration Adapter:

1. Use one shared server certificate.
2. Use a single HTTPS listener.
3. Validate callers using:
   - mTLS client certificates.
   - Application-level authorization.

This keeps the design simple, secure, and aligned with TLS standards.

---

# 14. Conclusion

TLS requires the server certificate to be selected immediately after ClientHello.

At that moment the server does not know:

- HTTP headers.
- URI.
- Payload.
- Authorization token.
- Business caller identity.

If multiple clients connect using the same:

- Hostname.
- IP address.
- HTTPS port.

then the server cannot dynamically select different certificates.

This is a protocol-level constraint independent of:

- Quarkus.
- Vert.x.
- Java.
- Any specific server implementation.