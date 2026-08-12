import pandas as pd
from datetime import datetime

# Read the Excel file
excel_path = r'c:\Apparao Maroju\AI-SSI\Project-IGNIS(POC)\UCRI2.0-Input\UCRI-Phase I1-TestCases V0.4.xlsx'
df = pd.read_excel(excel_path)

# Fill forward the TID, Test Case Name, Category, Description, Pre-conditions for grouped rows
df['TID'] = df['TID'].ffill()
df['Test Case Name'] = df['Test Case Name'].ffill()
df['Category'] = df['Category'].ffill()
df['Description'] = df['Description'].ffill()
df['Pre-conditions'] = df['Pre-conditions'].ffill()

# Group by TID
test_cases = df.groupby('TID')

# Start building the markdown document
md_content = """# UCRI 2.0 Phase II – Integration Testing

## Overview

As part of the end-to-end integration testing phase for UCRI 2.0 Phase II, comprehensive test scenarios were developed to validate the interface connectivity, data flow, and communication between IPL (Incident Processing Layer) and UCRI (Unified Central Routing Infrastructure) systems. The following test scenarios ensure that information is exchanged, processed, and synchronized as expected within the integrated environment.

### Integration Scope
- **System A (Initiator/Receiver):** IPL (Incident Processing Layer)
- **System B (Partner/Mock Service):** UCRI (Unified Central Routing Infrastructure)
- **Communication Protocols:** REST API, Event-driven messaging
- **Testing Focus:** Bidirectional event flow validation, error handling, edge cases, and boundary conditions

---

## Test Categories Summary

| Category | Description | Test Count |
|:---------|:------------|:-----------|
| **Functional** | Core business flow validations for IPL-UCRI integration | {functional_count} |
| **Negative** | Error handling, invalid inputs, and failure scenarios | {negative_count} |
| **Edge** | Concurrent flows, race conditions, and stress scenarios | {edge_count} |
| **Boundary** | Payload limits and boundary condition testing | {boundary_count} |

---

## Test Matrix

"""

# Count tests by category
category_counts = df.drop_duplicates(subset=['TID'])['Category'].value_counts()
functional_count = category_counts.get('Functional', 0)
negative_count = category_counts.get('Negative', 0)
edge_count = category_counts.get('Edge', 0)
boundary_count = category_counts.get('Boundary', 0)

md_content = md_content.format(
    functional_count=functional_count,
    negative_count=negative_count,
    edge_count=edge_count,
    boundary_count=boundary_count
)

# Add the test matrix table
md_content += """| Test | Pre-Requisite | Verification Detail | Expected Outcome | Reference & Status |
|:-----|:--------------|:--------------------|:-----------------|:-------------------|
"""

# Process each test case
for tid, group in test_cases:
    if pd.isna(tid):
        continue
    
    # Get test case details (from first row)
    first_row = group.iloc[0]
    test_name = first_row['Test Case Name'] if pd.notna(first_row['Test Case Name']) else ''
    category = first_row['Category'] if pd.notna(first_row['Category']) else ''
    description = first_row['Description'] if pd.notna(first_row['Description']) else ''
    preconditions = first_row['Pre-conditions'] if pd.notna(first_row['Pre-conditions']) else ''
    
    # Clean up preconditions - replace newlines with <br>
    if preconditions:
        preconditions = preconditions.replace('_x000D_\n', '<br>').replace('\n', '<br>').strip()
        if not preconditions.startswith('*'):
            preconditions = '* ' + preconditions.replace('<br>', '<br>* ')
    
    # Build verification steps and expected outcomes
    steps = []
    expected = []
    
    for _, row in group.iterrows():
        step_no = row['Step No']
        step_desc = row['Step Description']
        exp_result = row['Expected Result']
        
        if pd.notna(step_no) and pd.notna(step_desc):
            steps.append(f"{int(step_no)}. {step_desc}")
        
        if pd.notna(exp_result) and str(exp_result).strip():
            expected.append(f"* {exp_result}")
    
    verification = '<br>'.join(steps) if steps else 'N/A'
    expected_outcome = '<br>'.join(expected) if expected else 'N/A'
    
    # Build the test title
    test_title = f"**{tid}: {test_name}** [{category}]"
    
    # Build reference info
    reference = f"**Test ID:** {tid}<br>**Category:** {category}<br>**Priority:** Medium<br>**Status:** Draft"
    
    # Add table row
    md_content += f"| {test_title} | {preconditions} | {verification} | {expected_outcome} | {reference} |\n"

# Add footer
md_content += f"""
---

## Document Information

| Field | Value |
|:------|:------|
| **Document Version** | 0.4 |
| **Phase** | UCRI 2.0 Phase II |
| **Generated Date** | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
| **Test Cases Count** | {len(test_cases)} |
| **Document Type** | Integration Test Plan |

---

## Appendix: Test Execution Guidelines

### Pre-requisites for Test Execution
1. Adapter service running with `adapter.transport=in-memory`
2. All relevant modules enabled (IPL, UCRI dispatch centers)
3. Postman/API testing tools configured
4. Logging infrastructure operational
5. Metrics/monitoring endpoint accessible

### Test Environment Configuration
- **Transport Mode:** In-memory (for unit/integration testing)
- **Logging Level:** DEBUG (for detailed verification)
- **Timeout Settings:** Standard production values

### Test Evidence Requirements
- API request/response payloads
- System logs with correlationId traces
- Metrics dashboard screenshots
- Error logs for negative scenarios

---

*This document is auto-generated from UCRI-Phase II-TestCases V0.4.xlsx*
"""

# Write the output file
output_path = r'c:\Apparao Maroju\AI-SSI\Project-IGNIS(POC)\UCRI2.0-Output\UCRI2-Phase-II-IntegrationTestPlan.md'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f"Generated: {output_path}")
print(f"Total test cases processed: {len(test_cases)}")
