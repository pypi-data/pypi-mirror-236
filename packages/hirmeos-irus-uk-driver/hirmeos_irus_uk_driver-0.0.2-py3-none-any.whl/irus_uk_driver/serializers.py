from typing import List

from pydantic import BaseModel, Field


class IrusCountry(BaseModel):
    code: str = Field(alias='Country_Code')
    name: str = Field(alias='Country')


class IrusMetricsItem(BaseModel):
    unique_requests: int = Field(alias='Unique_Item_Requests')


class IrusInstance(BaseModel):
    country: IrusCountry = Field(alias='Country')
    metrics: IrusMetricsItem = Field(alias='Metric_Type_Counts')
    month: str = Field(alias='Event_Month')


class IrusReportItem(BaseModel):
    doi: str = Field(alias='DOI')
    instances: List[IrusInstance] = Field(alias='Performance_Instances')
