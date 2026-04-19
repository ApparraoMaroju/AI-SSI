## Using Templates in Prompts

### Method 1: Copy-Paste

```
CONTEXT:
[Paste content from context_project.md]
[Paste content from context_feature.md]

TASK:
Generate test cases...
```

### Method 2: Reference Files

```
CONTEXT:
See attached files:
- context_project.md
- context_feature.md
- context_constraints.md

TASK:
Using the context from the attached files, generate...
```

---

## Folder Structure

```
📁 prompts/
├── 📁 context/
│   ├── context_project.md
│   ├── context_constraints.md
│   └── 📁 features/
│       ├── context_login.md
│       ├── context_checkout.md
│       └── context_payment.md
├── 📁 templates/
│   ├── template_test_cases.md
│   ├── template_bug_report.md
│   └── template_api_tests.md
└── README.md
```
