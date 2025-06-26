import json
import pyjq
from datetime import datetime, timezone
import logging
from app.services.gundi import send_observations_to_gundi, send_events_to_gundi
from app.services.activity_logger import webhook_activity_logger
from .core import WebhookPayload,  GenericJsonTransformConfig
from pydantic import Field

logger = logging.getLogger(__name__)

from .models import Survey123ResponsePayload

@webhook_activity_logger()
async def webhook_handler(payload: Survey123ResponsePayload, integration=None, webhook_config: GenericJsonTransformConfig = None):
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
    if payload.eventType == "addData":
        event_details = payload.feature.attributes.dict()
        event_details['user_info'] = payload.userInfo.dict()


        # TODO: Revisit after we allow null location in Gundi.
        location = {
            "lat":payload.feature.geometry.y,
            "lon":payload.feature.geometry.x
            } if payload.feature.geometry else {"lat": 0, "lon": 0}

        event_data = {
            "title": payload.surveyInfo.formTitle,
            "event_type": event_type,
            "recorded_at": payload.feature.attributes.reported_time.isoformat(),
            "location":location,
            "event_details": event_details  
        }

        await send_events_to_gundi([event_data], integration_id=integration.id)
        
        return {"survey_items_count": 1}
    else:
        logger.info(f'Skipping event with even_type: {payload.eventType} that is not yet supported.')
        logger.debug(f'Skipping event {payload.json()}')
        return {"survey_items_count": 0}
