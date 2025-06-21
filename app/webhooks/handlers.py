import json
import pyjq
from datetime import datetime, timezone
import logging
from app.services.gundi import send_observations_to_gundi, send_events_to_gundi
from app.services.activity_logger import webhook_activity_logger
from .core import WebhookPayload,  GenericJsonTransformConfig
from pydantic import Field

logger = logging.getLogger(__name__)

# class Survey123Payload(WebhookPayload):
#     _json: dict = Field(alias="json")

from .models import Survey123Payload

@webhook_activity_logger()
async def webhook_handler(payload: Survey123Payload, integration=None, webhook_config: GenericJsonTransformConfig = None):
    logger.info(f"Webhook handler executed with integration: '{integration}'.")
    logger.info(f"Payload: '{payload}'.")
    logger.info(f"Config: '{webhook_config}'.")
    # input_data = json.loads(payload.json())
    # filter_expression = webhook_config.jq_filter.replace("\n", "")
    # transformed_data = pyjq.all(filter_expression, input_data)
    logger.info(f"Transformed Data: {payload.dict()}")
    
    # events = None
    # vals = payload._json

    event_details = payload._json.feature.attributes.dict()
    event_details['user_info'] = payload._json.userInfo.dict()

    event_data = {
        "title": payload._json.surveyInfo.formTitle,
        "event_type": "survey123_response",
        "recorded_at": datetime.fromtimestamp(payload._json.feature.attributes.reported_time/1000).replace(tzinfo=timezone.utc).isoformat(),
        "location":{
            "lat":payload._json.feature.geometry.y,
            "lon":payload._json.feature.geometry.x
        },
        "event_details": event_details
    }

    send_events_to_gundi([event_data], integration_id=integration.id)
    
    return {"survey_items_count": 1}
