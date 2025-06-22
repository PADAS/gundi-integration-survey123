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

    input_data = json.loads(payload.json())
    filter_expression = webhook_config.jq_filter.replace("\n", "")
    transformed_data = pyjq.all(filter_expression, input_data)
    logger.info(f"Transformed Data: {transformed_data}")

    if transformed_data:
        event_type = transformed_data[0]['event_type']
    
    # TODO: Add support for other Survey123 event types
    if payload.survey_response.eventType == "addData":
        event_details = payload.survey_response.feature.attributes.dict()
        event_details['user_info'] = payload.survey_response.userInfo.dict()

        event_data = {
            "title": payload.survey_response.surveyInfo.formTitle,
            "event_type": event_type,
            "recorded_at": payload.survey_response.feature.attributes.reported_time.isoformat(),
            "location":{
                "lat":payload.survey_response.feature.geometry.y,
                "lon":payload.survey_response.feature.geometry.x
            },
            "event_details": event_details  
        }

        await send_events_to_gundi([event_data], integration_id=integration.id)
        
        return {"survey_items_count": 1}
    else:
        logger.info(f'Skipping event with even_type: {payload.survey_response.eventType} that is not yet supported.')
        logger.debug(f'Skipping event {payload.json()}')
        return {"survey_items_count": 0}
