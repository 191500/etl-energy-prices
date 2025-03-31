import requests

from energy_prices.utils.class_model import ApiResponse, ApiParameters

BASE_URL = "https://api.eia.gov/v2"

def getEndpoint(endpoint:str, params:ApiParameters) -> ApiResponse:
    response  = requests.get(
        url=f"{BASE_URL}/{endpoint}",
        params={
            "frequency": params.frequency,
            "data[0]": params.data0,
            "data[1]": params.data1,
            "data[2]": params.data2,
            "data[3]": params.data3,
            "sort[0][column]": params.sort0Column,
            "sort[0][direction]": params.sort0Direction,
            "offset": params.offset,
            "length": params.length,
            "api_key": params.api_key,
        })
    
    response.raise_for_status()
    
    return ApiResponse(response.json()["response"]["data"])