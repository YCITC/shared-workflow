---
name: Mermaid
description: Defines formatting constraints for generating Mermaid diagrams to ensure readability and narrow width.
---

## Rule: Mermaid Diagram Formatting

### Constraints:

1. **Orientation**: Default to `graph TD` (Top-Down) unless a horizontal flow is explicitly requested for clarity.
2. **Subgraphs**:
    - Inside subgraphs, prefer vertical chaining (`A --> B --> C`) instead of wide branching from a single node to many nodes in parallel.
    - Use `direction TB` inside subgraphs to force vertical layout if necessary.
3. **Text Content**:
    - Keep node labels concise.
    - If a label exceeds 15-20 characters, use actual newlines with leading spaces for indentation for manual line breaks, including for text within nodes (e.g., `A["Long
    Node
    Text"]`).
    - Avoid using parentheses `()` in node labels.
4. **Consistency**: Use consistent naming conventions for node IDs (e.g., CamelCase like `InitMav`, `EntryPoint`).

### Actions:

- Apply these styles whenever generating or updating Mermaid diagrams in Markdown documentation.
