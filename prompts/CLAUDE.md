# CLAUDE

## Memory

- No CLAUDE.md in the project root
- Use project root .claude/ directory for memory
  - architecture.md - Project structure, reference, lookup
  - status.md - Recent changes, pending work, session notes
  - work-mapping.md - File purposes, patterns, APIs, references
  - claude-notes.md - Optional for claude-internal memory and notes

Keep your memory up to date as you work unless directed otherwise.  
Do not wait to be told to update memory.

## Communication

### Before Implementation

- Ask, don't assume
- Provide options with analysis, pros and cons, and a recommendation
- Confirm alignment of recommendations before proceeding
- Structure Comparisons - Prefer tables for options, API, file mapping

### During Implementation
- Use TODO lists - Keep track of what has been done and what needs to be done
- Work systematically - Complete each logical unit before moving to next
- Update documentation alongside code - Keep README, docstrings, comments insync with changes

### After Implementation
- Provide change summaries - List files modified and what changed in each
- Show usage examples - Demonstrate how new features work

## Design Philosophy
- Shared Internals - Extract common logic for maximal re-usability
- Backwards Compatibility - Do not break API unless otherwise told
  - If break is necessary, provide options and warn about scope
- Don't over-engineer - Complicated means there is probably a better solution
- Less Code means Less Debt - Minimize the footprint


# Repo Management - Git

- Never initialize a fresh project as a git repo unless asked to
- Your memory files MUST ALWAYS be in the .gitignore
- Never work on main, suggest a branch before starting work
- NEVER mention a `co-authored-by` or similar; No generation tool references


## Commits

- Use best practice for commit messages, be brief and exact
- Commit frequently to maintain check points during work

## Pull Requests

- Squash to a single commit before submitting a PR
- Create a detailed message of what changed
- Focus on high level description (what was the problem, how was it solved)
- Do not delve into specifics of the code unless absolutely necessary for clarity



# Python

## Code Quality

- Type hints required for all code
- Public APIs must have docstrings
  - Use Single Quotes `'''` for docstrings (never `"""`)
- Follow existing patterns exactly
- Line limit: 89 characters maximum
- Organize code in sections and label with comment blocks:

```python
# =============================================================================
# Section Name - Note about section if necessary
# =============================================================================
```

## Code Style

- PEP8 naming (snake case for functions/variables)
- Class names in PascalCase
- Constants in UPPER_SNAKE_CASE
- Use f-strings for formatting
- Keep namespace clean and tidy


# Frontend Web

I'm a total newbie when it comes to front-end, both in stack and in javascript,
typescript, etc.

For new projects, use `bun`

Give me deep explanations and details about what you are doing and why to help me
learn.