from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime, date

class ReportExportMetadata(BaseModel):
    report_type: str
    exported_at: datetime
    exported_by: str
    record_id: int
    system_version: str = "4.0.0"

class FreshnessReportExportPayload(BaseModel):
    metadata: ReportExportMetadata
    inspection_data: Dict[str, Any]

class ShelfLifeReportExportPayload(BaseModel):
    metadata: ReportExportMetadata
    prediction_data: Dict[str, Any]
