from pydantic import BaseModel


class ExportComponent(BaseModel):
    PRJ_ID: str
    CMPNT_NM: str
    CMPNT_NMSPC: str
    CMPNT_RVSN_DESC: str
    CMPNT_TYPE_CD: str
    CMPNT_IN: dict[str, str]
    CMPNT_OUT: list[str]
    CMPNT_SCRIPT: str
    CMPNT_DESC: str
    REG_ID: str

    class Config:
        extra = 'forbid'


class GetComponent(BaseModel):
    PRJ_ID: str
    CMPNT_NM: str
    CMPNT_RVSN: int | None

    class Config:
        extra = 'forbid'
