# OceanProof

## GenLayer-Powered RWA Maritime Verification

OceanProof is a GenLayer Intelligent Contract for verifying real-world
maritime shipping events using independent evidence sources and
AI-powered consensus.

It transforms fragmented maritime data into a consensus-backed,
machine-readable verification result:

- `VERIFIED`
- `DISPUTED`
- `UNVERIFIED`

The goal is to provide a reusable verification primitive for
real-world asset (RWA) and supply-chain applications.

---

## Problem

Maritime shipping data is fragmented across multiple independent
sources.

For the same shipment, different systems may report different states.

For example:

- AIS: Vessel has not arrived
- Port Authority: Container has arrived
- Carrier: Shipment marked as arrived
- IoT: No reliable sensor data available

A traditional application may simply trust one source.

OceanProof instead asks GenLayer's Intelligent Contract validators
to independently evaluate the available evidence and reach a
consensus-backed classification.

---

## Core Workflow

```text
Real-World Maritime Data
        │
        ├── AIS
        ├── Port Authority
        ├── Carrier
        └── IoT
        │
        ▼
OceanProof Verification Request
        │
        ▼
GenLayer Intelligent Contract
        │
        ▼
AI Validators
        │
        ▼
GenLayer Consensus
        │
        ├── VERIFIED
        ├── DISPUTED
        └── UNVERIFIED
        │
        ▼
On-Chain Verification Result
