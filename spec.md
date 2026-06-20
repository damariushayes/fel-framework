# FEL-P-01: Forensic Extraction Lifecycle Core Protocol

## 1. Boundary Isolation Invariant
An Ancestral Core system is defined mathematically by isolating state mutations and eliminating semantic leakage across the system boundary. The Mutation Delta ($\Delta M$) over a given observation epoch ($E$) must strictly equal zero:

$$\Delta M = \int_{E} \left( \sum W_{db} + \sum M_{state} \right) dt = 0$$

Where:
* $W_{db}$ represents direct state writes intercepted at the storage layer.
* $M_{state}$ represents memory-mapped or runtime state changes altering internal schemas.

## 2. Enforcement Gates
* **Gate 01 (Write-Isolation):** If $\Delta M > 0$, the module is volatile. Direct writes are prohibited; modifications must be externalized via log-based Change Data Capture (CDC).
* **Gate 02 (Zero-Leak Translation):** Greenfield services are strictly forbidden from executing synchronous IPC directly against an ancestral domain. All data must pass through the Anti-Corruption Layer (ACL).
