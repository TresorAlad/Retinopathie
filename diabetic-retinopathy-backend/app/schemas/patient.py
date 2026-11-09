from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field

class PatientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    patient_code: str
    first_name: str
    last_name: str
    birth_date: date | None
    created_at: datetime
