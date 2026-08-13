# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import typing


class ShipmentVerifier(gl.Contract):
    last_result: str
    last_container_id: str
    last_event_type: str
    last_reason: str

    def __init__(self):
        self.last_result = "NO_VERIFICATION"
        self.last_container_id = ""
        self.last_event_type = ""
        self.last_reason = ""

    @gl.public.write
    def verify_shipment(
        self,
        container_id: str,
        event_type: str,
        ais_status: str,
        port_status: str,
        carrier_status: str,
        iot_status: str,
    ) -> typing.Any:

        evidence = f"""
Container ID: {container_id}
Event being verified: {event_type}

AIS evidence:
{ais_status}

Port Authority evidence:
{port_status}

Carrier evidence:
{carrier_status}

IoT evidence:
{iot_status}
"""

        def get_verification_input() -> str:
            return evidence

        result = gl.eq_principle.prompt_non_comparative(
            get_verification_input,
            task="""
Evaluate the maritime shipment evidence and classify the event.

Return exactly one of these three words:

VERIFIED
DISPUTED
UNVERIFIED

Use these rules:

VERIFIED:
Independent evidence substantially agrees that the event happened.

DISPUTED:
Important sources conflict with each other.

UNVERIFIED:
There is not enough independent evidence to establish that the event happened.

Do not return explanations.
Do not return JSON.
Return only one of:
VERIFIED
DISPUTED
UNVERIFIED
""",
            criteria="""
The response must be exactly one of:
VERIFIED
DISPUTED
UNVERIFIED

VERIFIED means the independent maritime evidence substantially agrees.

DISPUTED means important evidence sources conflict.

UNVERIFIED means there is insufficient evidence.

The response must contain no explanation and no additional text.
""",
        )

        self.last_result = result
        self.last_container_id = container_id
        self.last_event_type = event_type

        if result == "VERIFIED":
            self.last_reason = "Independent maritime evidence substantially agrees."
        elif result == "DISPUTED":
            self.last_reason = "Important maritime evidence sources conflict."
        else:
            self.last_reason = "Insufficient independent evidence."

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
      def get_last_reason(self) -> str:
    return self.last_reason
