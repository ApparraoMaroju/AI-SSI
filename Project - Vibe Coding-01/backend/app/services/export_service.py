"""Export service for test cases."""

import csv
import io
from typing import List
from datetime import datetime

from app.schemas import TestCase, ExportFormat


class ExportService:
    """Service for exporting test cases to various formats."""
    
    @staticmethod
    def to_markdown(test_cases: List[TestCase], include_header: bool = True) -> str:
        """Export test cases to Markdown format."""
        lines = []
        
        if include_header:
            lines.append(f"# Test Cases")
            lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            lines.append(f"Total Test Cases: {len(test_cases)}")
            lines.append("")
            lines.append("---")
            lines.append("")
        
        for tc in test_cases:
            lines.append(f"## {tc.id}: {tc.title}")
            lines.append("")
            lines.append(f"**Type:** {tc.type.value}")
            lines.append(f"**Priority:** {tc.priority.value}")
            lines.append(f"**Linked Jira:** {tc.linked_jira_id}")
            lines.append("")
            
            lines.append("### Preconditions")
            lines.append(tc.preconditions)
            lines.append("")
            
            lines.append("### Test Steps")
            for i, step in enumerate(tc.steps, 1):
                lines.append(f"{i}. {step}")
            lines.append("")
            
            lines.append("### Test Data")
            lines.append(tc.test_data)
            lines.append("")
            
            lines.append("### Expected Result")
            lines.append(tc.expected_result)
            lines.append("")
            lines.append("---")
            lines.append("")
        
        return "\n".join(lines)
    
    @staticmethod
    def to_csv(test_cases: List[TestCase], include_header: bool = True) -> str:
        """Export test cases to CSV format."""
        output = io.StringIO()
        writer = csv.writer(output)
        
        if include_header:
            writer.writerow([
                "ID", "Title", "Type", "Priority", "Preconditions",
                "Steps", "Test Data", "Expected Result", "Linked Jira ID"
            ])
        
        for tc in test_cases:
            # Join steps with numbered format
            steps_str = " | ".join([f"{i+1}. {step}" for i, step in enumerate(tc.steps)])
            
            writer.writerow([
                tc.id,
                tc.title,
                tc.type.value,
                tc.priority.value,
                tc.preconditions,
                steps_str,
                tc.test_data,
                tc.expected_result,
                tc.linked_jira_id
            ])
        
        return output.getvalue()
    
    @staticmethod
    def to_tsv(test_cases: List[TestCase], include_header: bool = True) -> str:
        """Export test cases to TSV format (for direct paste into Jira/Xray/TestRail)."""
        output = io.StringIO()
        writer = csv.writer(output, delimiter='\t')
        
        if include_header:
            writer.writerow([
                "ID", "Title", "Type", "Priority", "Preconditions",
                "Steps", "Test Data", "Expected Result", "Linked Jira ID"
            ])
        
        for tc in test_cases:
            # Join steps with numbered format
            steps_str = " | ".join([f"{i+1}. {step}" for i, step in enumerate(tc.steps)])
            
            writer.writerow([
                tc.id,
                tc.title,
                tc.type.value,
                tc.priority.value,
                tc.preconditions,
                steps_str,
                tc.test_data,
                tc.expected_result,
                tc.linked_jira_id
            ])
        
        return output.getvalue()
    
    @staticmethod
    def export(
        test_cases: List[TestCase],
        format: ExportFormat,
        include_header: bool = True
    ) -> tuple[str, str, str]:
        """
        Export test cases to specified format.
        
        Returns:
            Tuple of (content, filename, content_type)
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        jira_id = test_cases[0].linked_jira_id if test_cases else "unknown"
        
        if format == ExportFormat.MARKDOWN:
            content = ExportService.to_markdown(test_cases, include_header)
            filename = f"test_cases_{jira_id}_{timestamp}.md"
            content_type = "text/markdown"
        elif format == ExportFormat.CSV:
            content = ExportService.to_csv(test_cases, include_header)
            filename = f"test_cases_{jira_id}_{timestamp}.csv"
            content_type = "text/csv"
        else:  # TSV
            content = ExportService.to_tsv(test_cases, include_header)
            filename = f"test_cases_{jira_id}_{timestamp}.tsv"
            content_type = "text/tab-separated-values"
        
        return content, filename, content_type
