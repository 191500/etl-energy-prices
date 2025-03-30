from dataclasses import dataclass
from typing import List, Literal, Optional

@dataclass
class ApiParameters:
    frequency: Optional[Literal["monthly"]] = "monthly"
    data0: Optional[Literal["customers"]] = "customers"
    data1: Optional[Literal["price"]] = "price"
    data2: Optional[Literal["revenue"]] = "revenue"
    data3: Optional[Literal["sales"]] = "sales" 
    sort0Column: Optional[Literal["period"]] = "period"
    sort0Direction: Optional[Literal["desc"]] = "desc" 
    offset: Optional[int] = None
    length: Optional[int] = None
    api_key: Optional[str] = None

@dataclass
class EnergySchema:
    period: str
    stateid: Literal["MN"]
    stateDescription: str
    sectorid: Literal["RES"]
    sectorName: Literal["residential"]
    customers: str
    price: str
    revenue: str
    sales: str
    customers_units: Literal["number of customers"]
    price_units: Literal["cents per kilowatt-hour"]
    revenue_units: Literal["million dollars"]
    sales_units: Literal["million kilowatt hours"]

    @classmethod
    def from_kwargs(cls, **kwargs):
        for key in ["customers-units", "price-units", "revenue-units", "sales-units"]:
            kwargs[key.replace("-", "_")] = kwargs[key]
            del kwargs[key]
        return cls(**kwargs)

@dataclass
class ApiResponse:
    data: List[EnergySchema]

    def __post_init__(self):
        self.data = [EnergySchema.from_kwargs(**x) for x in self.data]
