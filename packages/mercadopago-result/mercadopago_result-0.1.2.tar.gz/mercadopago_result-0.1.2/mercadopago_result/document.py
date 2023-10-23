from pydantic import BaseModel
from typing import Optional

DocumentIdField = str
DocumentNameField = str
DocumentTypeField = str
DocumentMinLengthField = int
DocumentMaxLengthField = int


class Document(BaseModel):
    id: Optional[DocumentIdField] = None
    name: Optional[DocumentNameField] = None
    type: Optional[DocumentTypeField] = None
    min_length: Optional[DocumentMinLengthField] = None
    max_length: Optional[DocumentMaxLengthField] = None
