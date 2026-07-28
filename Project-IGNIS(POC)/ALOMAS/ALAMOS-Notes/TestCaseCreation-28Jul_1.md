# Test Case Generation Prompt - ALAMOS Integration (Optimized)

**Date:** 2026-07-28  
**Purpose:** Generate optimized functional integration test cases with minimum count and maximum coverage  
**Output Format:** Excel (.xlsx)

---

## Prompt

```
You are an expert QA Engineer specializing in system integration testing for enterprise backend applications.

## Context Documents
Analyze the following context documents to understand the ALAMOS Integration system:
- `ALAMOS_Project_Context.md` - Project overview, architecture, tech stack, constraints
- `ALAMOS_Feature_Context.md` - Feature specifications, user stories, acceptance criteria
- `ALAMOS_Testing_Context.md` - Testing scope, scenarios, dependencies, traceability

## Objective
Generate **optimized functional integration test cases** that:
1. **Minimize test count** while **maximizing coverage**
2. **Eliminate duplicates** - consolidate test cases where:
   - Same process/verification steps with different naming
   - Similar error handling scenarios (group business/technical faults together)
   - Same flow with minor parameter variations (parameterize instead of duplicate)
   - Component tests already covered by E2E tests
3. Maintain **full traceability** to all user stories

## Consolidation Rules
Apply these deduplication strategies:

### 1. Request Validation Consolidation
Combine tests for HTTP method, content-type, authentication, and field validation into a single negative test case with multiple verification steps.

### 2. Error Handling Consolidation  
Group similar error scenarios (business fault, technical fault, timeout, unavailable) into one comprehensive error handling test case.

### 3. Parameterized Test Consolidation
When testing multiple triggers/variations of the same flow (e.g., 4 Mission Update triggers), combine into one test case with steps for each variation.

### 4. Correlation/Fallback Consolidation
Combine primary path and fallback path tests (e.g., external_id → incident_number fallback) into single test cases.

### 5. E2E Deduplication
Only include E2E tests that validate cross-component behavior NOT already covered by component-level tests.

## User Stories to Cover
- US-ADAPTER-ALAMOS-001: Situation Report Receive & Validate
- US-ADAPTER-ALAMOS-002: Domain Event Generation
- US-ADAPTER-ALAMOS-003: FacadeService Routing Layer
- US-ADAPTER-ALAMOS-004: FacadeService IPL Processing
- US-ADAPTER-RELIABILITY-001: Retry & DLQ Validation
- US-ALAMOS-GW-001: Legacy Alerting
- US-ALAMOS-GW-002: Continuous Mission Updates
- US-ALAMOS-GW-003: Squad Information Extension
- US-ALAMOSGW-MOCK-001: Mock Gateway Service
- US-INTEGRATION-E2E-001: End-to-End Integration Testing

## Output Format
Generate test cases in Excel format with columns:
| Column | Description |
|--------|-------------|
| TID | Test Case ID (TC-001, TC-002, ...) |
| Test Case Name | [User Story ID] Descriptive name |
| Category | Functional (Happy Path) / Negative Scenario / Edge Case / Integration (E2E) |
| Description | Comprehensive description including consolidation scope |
| Pre-conditions | Numbered list of prerequisites |
| Step No | Step number (1, 2, 3...) |
| Step Description | Detailed action to perform |
| Expected Result | Expected outcome for the step |
| Priority | High / Medium / Low |
| User Story Reference | Source user story ID |

## Quality Requirements
1. Each test case should be **self-contained** with clear pre-conditions
2. Steps should be **atomic** and **verifiable**
3. Expected results should be **specific** and **measurable**
4. Include both **positive** and **negative** scenarios
5. Cover **boundary conditions** and **edge cases** within consolidated tests
6. Maintain **backward compatibility** verification where applicable

## Target
Reduce from 50+ test cases to ~20 optimized test cases while maintaining 100% requirement coverage.
```

---

## Expected Output Summary

| Metric | Target |
|--------|--------|
| Total Test Cases | ~19-25 |
| Coverage | 100% of all user stories |
| Reduction | 60%+ from original count |

### Test Case Distribution (Target)

| User Story | Test Cases | Coverage Focus |
|------------|------------|----------------|
| US-ADAPTER-ALAMOS-001 | 2-3 | Valid flow + consolidated validation errors + IPL failure |
| US-ADAPTER-ALAMOS-002 | 2 | Domain Event with correlation paths + error handling |
| US-ADAPTER-ALAMOS-003 | 2 | Routing + response propagation + invalid config |
| US-ADAPTER-ALAMOS-004 | 2 | IPL invocation + consolidated error scenarios |
| US-ADAPTER-RELIABILITY-001 | 1 | Retry/DLQ/logging consolidated |
| US-ALAMOS-GW-001 | 2 | Valid Alerting + error handling |
| US-ALAMOS-GW-002 | 2 | All 4 triggers consolidated + errors |
| US-ALAMOS-GW-003 | 1 | Squad info (single/multiple/backward compat) |
| US-ALAMOSGW-MOCK-001 | 1 | Mock mode functionality consolidated |
| US-INTEGRATION-E2E-001 | 3 | Unique E2E flows only |

---

## Anti-Patterns to Avoid

1. ❌ Separate test cases for each HTTP error code (405, 415, 401, 400)
2. ❌ Separate test cases for business fault vs technical fault vs timeout
3. ❌ Separate test cases for each Mission Update trigger type
4. ❌ Separate test cases for single vs multiple squads
5. ❌ E2E tests that duplicate component-level tests
6. ❌ Separate tests for external_id correlation vs incident_number fallback

---

## Notes

- This prompt was used to generate `ALAMOS_Functional_Integration_TestCases_Optimized_20260728_064453.xlsx`
- Original test count: 50
- Optimized test count: 19
- Reduction achieved: 62%
