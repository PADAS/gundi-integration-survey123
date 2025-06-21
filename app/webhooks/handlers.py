import json
import pyjq
import logging
from app.services.gundi import send_observations_to_gundi, send_events_to_gundi
from app.services.activity_logger import webhook_activity_logger
from .core import WebhookPayload,  GenericJsonTransformConfig
from pydantic import Field

logger = logging.getLogger(__name__)

class Survey123Payload(WebhookPayload):
    _json: dict = Field(alias="json")


@webhook_activity_logger()
async def webhook_handler(payload: Survey123Payload, integration=None, webhook_config: GenericJsonTransformConfig = None):
    logger.info(f"Webhook handler executed with integration: '{integration}'.")
    logger.info(f"Payload: '{payload}'.")
    logger.info(f"Config: '{webhook_config}'.")
    # input_data = json.loads(payload.json())
    # filter_expression = webhook_config.jq_filter.replace("\n", "")
    # transformed_data = pyjq.all(filter_expression, input_data)
    logger.info(f"Transformed Data: {payload.dict()}")
    
    # TODO: Send data to Gundi
    
    return {"survey_items_count": 1}
