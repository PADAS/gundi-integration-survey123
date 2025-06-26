
from typing import List
from datetime import datetime, timezone
from pydantic import BaseModel, Field, validator
from pydantic.config import BaseConfig, Extra
from .core import WebhookPayload

class Attributes(BaseModel):
    reported_time: datetime
    globalid: str
    
    @validator('reported_time', pre=True)
    def validate_reported_time(cls, v):
        if isinstance(v, int):
            return datetime.fromtimestamp(v/1000).replace(tzinfo=timezone.utc)
        return v
    
    class Config:
        allow_population_by_field_name = True
        extra = Extra.allow


class SpatialReference(BaseModel):
    wkid: int


class Geometry(BaseModel):
    x: float
    y: float
    spatialReference: SpatialReference


class Result(BaseModel):
    globalId: str
    objectId: int
    success: bool
    uniqueId: int


class LayerInfo(BaseModel):
    id: int
    name: str


class Feature(BaseModel):
    attributes: Attributes
    geometry: Geometry
    result: Result
    layerInfo: LayerInfo


class Attributes1(BaseModel):
    notes: str
    radness: str
    reported_time: int
    species: str
    globalid: str


class SpatialReference1(BaseModel):
    wkid: int


class Geometry1(BaseModel):
    x: float
    y: float
    spatialReference: SpatialReference1


class Result1(BaseModel):
    globalId: str
    objectId: int
    success: bool
    uniqueId: int


class LayerInfo1(BaseModel):
    id: int
    name: str


class Add(BaseModel):
    attributes: Attributes1
    geometry: Geometry1
    result: Result1
    layerInfo: LayerInfo1


class LayerInfo2(BaseModel):
    id: int
    name: str
    type: str
    objectIdField: str
    globalIdField: str
    relationships: List


class ApplyEdit(BaseModel):
    id: int
    adds: List[Add]
    layerInfo: LayerInfo2


class AddResult(BaseModel):
    globalId: str
    objectId: int
    success: bool
    uniqueId: int


class ResponseItem(BaseModel):
    addResults: List[AddResult]
    id: int


class SurveyInfo(BaseModel):
    formItemId: str
    formTitle: str
    serviceItemId: str
    serviceUrl: str


class PortalInfo(BaseModel):
    url: str
    token: str


class UserInfo(BaseModel):
    username: str
    firstName: str
    lastName: str
    fullName: str
    email: str


class Survey123ResponsePayload(BaseModel):
    eventType: str
    feature: Feature
    applyEdits: List[ApplyEdit]
    response: List[ResponseItem]
    surveyInfo: SurveyInfo
    portalInfo: PortalInfo
    userInfo: UserInfo
    class Config:
        allow_population_by_field_name = True
        extra = Extra.allow
