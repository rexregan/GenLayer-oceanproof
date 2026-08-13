# OceanProof

## GenLayer-Powered RWA Maritime Verification

OceanProof is a maritime RWA verification platform powered by GenLayer Intelligent Contracts.

It transforms fragmented real-world shipping data into consensus-backed, verifiable maritime events.

## Core Workflow

Real-world maritime data
→ AIS
→ Port Authority
→ Carrier
→ IoT

↓

OceanProof Verification Request

↓

GenLayer Intelligent Contract

↓

AI Validators

↓

GenLayer Consensus

↓

Verified / Disputed / Unverified

↓

On-chain Maritime Event Record

## Core Use Case

OceanProof verifies real-world container shipping events such as:

- Container loaded
- Vessel departed
- Vessel in transit
- Vessel arrived
- Container discharged
- Customs cleared
- Cargo delivered
- Shipment delayed
- Cargo damaged

## Why GenLayer?

Maritime data can conflict between independent sources.

For example:

AIS:
Vessel has not arrived.

Port:
Container has arrived.

Carrier:
Shipment marked as arrived.

OceanProof uses a GenLayer Intelligent Contract to evaluate conflicting evidence and produce a consensus-backed verification result.

## Demo Scenarios

### Scenario A — Verified

AIS → ARRIVED

Port → ARRIVED

Carrier → ARRIVED

Expected result:

VERIFIED

### Scenario B — Conflicting Evidence

AIS → NOT ARRIVED

Port → ARRIVED

Carrier → ARRIVED

IoT → UNKNOWN

Expected result:

DISPUTED

### Scenario C — Insufficient Evidence

AIS → UNKNOWN

Port → UNKNOWN

Carrier → ARRIVED

Expected result:

UNVERIFIED

## Project Architecture

ContainerRegistry
→ manages container RWA records

ShipmentVerifier
→ evaluates maritime evidence using GenLayer

MaritimeEventRegistry
→ stores verified maritime events

## Future Extensions

- Dangerous goods verification
- Cargo insurance verification
- Trade finance
- Customs verification
- Shipping dispute resolution
- Cargo damage verification
