# Test script 4

import asyncio

from opentelemetry import trace

from typing import List
from typing import Dict

tracer = trace.get_tracer("script_4_tracer")


async def fetch_mock_data() -> Dict[str, List[int]]:
    """Simulate async data fetch with delay."""
    await asyncio.sleep(0.1)  # Simulate network delay
    return {"data": [1, 2, 3, 4, 5]}


async def process_mock_data(data: Dict) -> List[int]:
    """Simulate async data processing."""
    await asyncio.sleep(0.05)  # Simulate processing time
    return [x * 2 for x in data["data"]]


async def async_fetch_data():
    """
    Async function that fetches data with telemetry.
    """
    async with tracer.start_as_current_span("fetch_data") as span:
        span.set_attribute("request_type", "async")
        try:
            raw_data = await fetch_mock_data()
            span.set_attribute("data_size", len(raw_data["data"]))

            processed_data = await process_mock_data(raw_data)
            span.add_event(
                "data_processed",
                {
                    "input_size": len(raw_data["data"]),
                    "output_size": len(processed_data),
                },
            )

            return processed_data
        except Exception as e:
            span.record_exception(e)
            raise
