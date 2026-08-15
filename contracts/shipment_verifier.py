# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


class ShipmentVerifier(gl.Contract):

    last_result: str
    last_container_id: str
    last_event_type: str
    last_reason: str
    last_sources: str

    def __init__(self):
        self.last_result = "NO_VERIFICATION"
        self.last_container_id = ""
        self.last_event_type = ""
        self.last_reason = ""
        self.last_sources = ""

    @gl.public.write
    def verify_shipment(
        self,
        container_id: str,
        event_type: str,
        ais_url: str,
        port_url: str,
        carrier_url: str,
        iot_url: str,
    ) -> str:

        # Basic source validation.
        # The contract records the exact evidence locations used
        # for this verification case.
        urls = [ais_url, port_url, carrier_url, iot_url]

        for url in urls:
            if not url.startswith("https://"):
                raise gl.UserError(
                    "All evidence sources must use HTTPS."
                )

        evidence_sources = f"""
AIS SOURCE:
{ais_url}

PORT AUTHORITY SOURCE:
{port_url}

CARRIER SOURCE:
{carrier_url}

IoT SOURCE:
{iot_url}
"""

        def evaluate_evidence():

            # IMPORTANT:
            # Evidence is fetched directly by GenLayer validators.
            # The caller provides source locations, not source claims.

            ais_response = gl.nondet.web.get(ais_url)
            port_response = gl.nondet.web.get(port_url)
            carrier_response = gl.nondet.web.get(carrier_url)
            iot_response = gl.nondet.web.get(iot_url)

            ais_data = ais_response.body.decode("utf-8")
            port_data = port_response.body.decode("utf-8")
            carrier_data = carrier_response.body.decode("utf-8")
            iot_data = iot_response.body.decode("utf-8")

            evidence = f"""
SHIPMENT CASE
Container ID: {container_id}
Event Type: {event_type}

SOURCE 1 — AIS
URL: {ais_url}
Evidence:
{ais_data}

SOURCE 2 — PORT AUTHORITY
URL: {port_url}
Evidence:
{port_data}

SOURCE 3 — CARRIER
URL: {carrier_url}
Evidence:
{carrier_data}

SOURCE 4 — IoT
URL: {iot_url}
Evidence:
{iot_data}
"""

            prompt = f"""
You are a maritime RWA verification agent.

Your task is to determine whether a real-world shipment event
is sufficiently supported by INDEPENDENT external evidence.

Do NOT trust caller-provided claims.
Use ONLY the evidence fetched from the four supplied sources.

SHIPMENT:
Container ID: {container_id}
Event: {event_type}

INDEPENDENT EVIDENCE:
{evidence}

Classify the event into exactly ONE:

VERIFIED
DISPUTED
UNVERIFIED

Rules:

VERIFIED:
Use VERIFIED only when multiple independent sources
substantially agree that the stated shipment event happened.

DISPUTED:
Use DISPUTED when important independent sources directly
conflict about whether the event happened.

UNVERIFIED:
Use UNVERIFIED when there is insufficient reliable evidence
to establish that the event happened.

Important:
- Do not treat one source as sufficient by itself.
- Do not invent missing information.
- Do not assume that a source is correct merely because it
  claims to represent a carrier, port, AIS provider, or IoT system.
- Compare the actual fetched evidence.
- Return ONLY one word.

Valid outputs:

VERIFIED
DISPUTED
UNVERIFIED
"""

            result = gl.nondet.exec_prompt(prompt)

            return result.strip().upper()

        result = gl.eq_principle.prompt_comparative(
            evaluate_evidence,
            principle="""
The validators must independently evaluate the same shipment
case and externally fetched evidence.

The final classification must be exactly one of:

VERIFIED
DISPUTED
UNVERIFIED

Validators should agree on the classification based on the
independent evidence, even if their internal reasoning differs.
"""
        )

        # Durable case record
        self.last_result = result
        self.last_container_id = container_id
        self.last_event_type = event_type
        self.last_sources = evidence_sources

        if result == "VERIFIED":
            self.last_reason = (
                "Multiple independent external sources substantially "
                "agree with the shipment event."
            )

        elif result == "DISPUTED":
            self.last_reason = (
                "Important independent external sources directly "
                "conflict about the shipment event."
            )

        else:
            self.last_reason = (
                "Insufficient reliable independent evidence to "
                "establish the shipment event."
            )

        return result

    @gl.public.view
    def get_last_result(self) -> str:
        return self.last_result

    @gl.public.view
    def get_last_container(self) -> str:
        return self.last_container_id

    @gl.public.view
    def get_last_event(self) -> str:
        return self.last_event_type

    @gl.public.view
    def get_last_reason(self) -> str:
        return self.last_reason

    @gl.public.view
    def get_last_sources(self) -> str:
        return self.last_sources        
