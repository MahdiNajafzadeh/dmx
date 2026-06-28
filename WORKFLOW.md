# MULTI-AGENT WORKFLOW DEFINITION

## CANONICAL WORKFLOW SEQUENCE

User Request
    ↓
[ORCHESTRATOR] Parse & Plan
    ↓
[DEVELOPER AGENT] Execute
    ↓
[VERSION CONTROL AGENT] Validate Versions
    ↓
[TESTER AGENT] Validate Quality
    ↓
[REVIEWER AGENT] Final Quality Gate
    ↓
[ORCHESTRATOR] Deliver Result

## AGENT ROLES

### Developer Agent

- Generates code/artifacts
- Submits with structured header
- Can iterate max 2-3 times
- Addresses feedback from Version Control, Testing, Reviewer

### Version Control Agent

- Validates semantic versioning
- Checks dependency compatibility
- Identifies breaking changes
- Coordinates with Developer if issues found

### Tester Agent

- Writes and executes tests (unit, integration, E2E)
- Measures coverage
- Reports test results and gaps
- Coordinates with Developer if failures found

### Reviewer Agent

- Final quality gate
- Reviews code, tests, versions, documentation
- Returns verdict: APPROVED / APPROVED_WITH_MINOR_CHANGES / REVISE_REQUESTED / REJECTED
- Does NOT generate or fix content

### Orchestrator

- Coordinates all agents
- Makes decisions when agents disagree
- Escalates blockers
- Delivers final result to user
