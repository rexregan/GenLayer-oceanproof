# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


class ShipmentVerifier(gl.Contract):

    # Durable verification case
    last_case_id: str
    last_container_id: str
    last_event_type: str

    # Consensus result
    last_result: str
    last_reason: str

    # Structured evidence record
    last_ais_evidence: str
    last_port_evidence: str
    last_carrier_evidence: str
    last_iot_evidence: str

    # Source locations
    last_sources: str

    def __init__(self):
        self.last_case_id = ""
        self.last_container_id = ""
        self.last_event_type = ""

        self.last_result = "NO_VERIFICATION"
        self.last_reason = ""

        self.last_ais_evidence = ""
        self.last_port_evidence = ""
        self.last_carrier_evidence = ""
        self.last_iot_evidence = ""

        self.last_sources = ""

    @gl.public.write
    def verify_shipment(
        self,
        case_id: str,
        container_id: str,
        event_type: str,
        ais_url: str,
        port_url: str,
        carrier_url: str,
        iot_url: str,
    ) -> str:

        # ---------------------------------------------------------
        # 1. Basic input validation
        # ---------------------------------------------------------

        if case_id == "":
            raise gl.vm.UserError("Case ID is required.")

        if container_id == "":
            raise gl.vm.UserError("Container ID is required.")

        if event_type == "":
            raise gl.vm.UserError("Event type is required.")

        urls = [
            ais_url,
            port_url,
            carrier_url,
            iot_url,
        ]

        for url in urls:
            if not url.startswith("https://"):
                raise gl.vm.UserError(
                    "All evidence sources must use HTTPS."
                )

        # ---------------------------------------------------------
        # 2. Fetch and normalize evidence
        #
        # The caller provides source locations, not source claims.
        # GenLayer validators independently fetch the evidence.
        # ---------------------------------------------------------

        def evaluate_evidence():

            ais_response = gl.nondet.web.get(ais_url)
            port_response = gl.nondet.web.get(port_url)
            carrier_response = gl.nondet.web.get(carrier_url)
            iot_response = gl.nondet.web.get(iot_url)

            ais_data = ais_response.body.decode("utf-8")
            port_data = port_response.body.decode("utf-8")
            carrier_data = carrier_response.body.decode("utf-8")
            iot_data = iot_response.body.decode("utf-8")

            # -----------------------------------------------------
            # Evidence case
            # -----------------------------------------------------

            evidence = f"""
OCEANPROOF VERIFICATION CASE

Case ID:
{case_id}

Container ID:
{container_id}

Event Type:
{event_type}


================ AIS EVIDENCE ================

Source URL:
{ais_url}

Evidence:
{ais_data}


================ PORT EVIDENCE ================

Source URL:
{port_url}

Evidence:
{port_data}


================ CARRIER EVIDENCE ================

Source URL:
{carrier_url}

Evidence:
{carrier_data}


================ IOT EVIDENCE ================

Source URL:
{iot_url}

Evidence:
{iot_data}
"""

            # -----------------------------------------------------
            # GenLayer verification prompt
            # -----------------------------------------------------

            prompt = f"""
You are the verification engine for OceanProof,
a maritime RWA shipment verification system.

Your task is to determine whether the specified shipment event
is sufficiently supported by the independently fetched evidence.

IMPORTANT:

The caller provides SOURCE LOCATIONS only.

Do not trust the caller's claim about the shipment.

The evidence below was fetched from the supplied URLs by the
GenLayer execution environment.

SHIPMENT CASE

Case ID:
{case_id}

Container ID:
{container_id}

Event:
{event_type}


INDEPENDENTLY FETCHED EVIDENCE

{evidence}


CLASSIFICATION

Return exactly one of:

VERIFIED
DISPUTED
UNVERIFIED


VERIFIED

Use VERIFIED only when multiple evidence sources independently
and substantially support the same shipment event.

DISPUTED

Use DISPUTED when important evidence sources directly conflict
about whether the event occurred.

UNVERIFIED

Use UNVERIFIED when the evidence is insufficient, missing,
unreliable, or cannot establish the shipment event.


IMPORTANT RULES

1. Do not trust a single source.

2. Do not assume a source is authoritative merely because
   it claims to represent a carrier, port, AIS provider,
   or IoT system.

3. Do not invent missing information.

4. The container ID and event type must be consistent
   with the evidence.

5. Conflicting evidence must result in DISPUTED unless
   the conflict is clearly irrelevant to the requested event.

6. Unknown or missing IoT evidence must not automatically
   mean that the shipment did not occur.

7. Test or synthetic evidence may be evaluated, but it must
   not be treated as authenticated real-world evidence.

8. Return ONLY the classification word.

Valid outputs:

VERIFIED
DISPUTED
UNVERIFIED
"""

            result = gl.nondet.exec_prompt(prompt)

            return result.strip().upper()

        # ---------------------------------------------------------
        # 3. GenLayer consensus
        # ---------------------------------------------------------

        result = gl.eq_principle.prompt_comparative(
            evaluate_evidence,
            principle="""
Independently evaluate the same shipment case and the
externally fetched evidence.

The validators must agree on the final classification.

The classification must be exactly:

VERIFIED
DISPUTED
UNVERIFIED

The decision should be based on evidence consistency,
source independence, container identity, and event identity.

Do not treat unauthenticated test fixtures as authoritative
real-world evidence.
"""
        )

        # ---------------------------------------------------------
        # 4. Build durable case record
        # ---------------------------------------------------------

        self.last_case_id = case_id
        self.last_container_id = container_id
        self.last_event_type = event_type

        self.last_result = result

        self.last_sources = f"""
Case ID: {case_id}

AIS:
{ais_url}

Port Authority:
{port_url}

Carrier:
{carrier_url}

IoT:
{iot_url}
"""

        # ---------------------------------------------------------
        # 5. Store the fetched evidence as a durable case record
        # ---------------------------------------------------------

        self.last_ais_evidence = (
            f"Case ID: {case_id}\n"
            f"Container ID: {container_id}\n"
            f"Event: {event_type}\n"
            f"Source Type: AIS\n"
            f"Source URL: {ais_url}\n"
        )

        self.last_port_evidence = (
            f"Case ID: {case_id}\n"
            f"Container ID: {container_id}\n"
            f"Event: {event_type}\n"
            f"Source Type: PORT_AUTHORITY\n"
            f"Source URL: {port_url}\n"
        )

        self.last_carrier_evidence = (
            f"Case ID: {case_id}\n"
            f"Container ID: {container_id}\n"
            f"Event: {event_type}\n"
            f"Source Type: CARRIER\n"
            f"Source URL: {carrier_url}\n"
        )

        self.last_iot_evidence = (
            f"Case ID: {case_id}\n"
            f"Container ID: {container_id}\n"
            f"Event: {event_type}\n"
            f"Source Type: IOT\n"
            f"Source URL: {iot_url}\n"
        )

        # ---------------------------------------------------------
        # 6. Durable reason
        # ---------------------------------------------------------

        if result == "VERIFIED":

            self.last_reason = (
                "Multiple independent evidence sources "
                "substantially support the shipment event."
            )

        elif result == "DISPUTED":

            self.last_reason = (
                "Important evidence sources conflict about "
                "the shipment event."
            )

        else:

            self.last_reason = (
                "The available evidence is insufficient to "
                "establish the shipment event."
            )

        return result

    # =============================================================
    # READ METHODS
    # =============================================================

    @gl.public.view
    def get_last_case_id(self) -> str:
        return self.last_case_id

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

    @gl.public.view
    def get_last_ais_evidence(self) -> str:
        return self.last_ais_evidence

    @gl.public.view
    def get_last_port_evidence(self) -> str:
        return self.last_port_evidence

    @gl.public.view
    def get_last_carrier_evidence(self) -> str:
        return self.last_carrier_evidence

    @gl.public.view
    def get_last_iot_evidence(self) -> str:
        return self.last_iot_evidence
