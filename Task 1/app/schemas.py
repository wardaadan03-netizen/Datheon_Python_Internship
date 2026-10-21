from typing import List, Optional
from pydantic import BaseModel, Field


class InvoiceItem(BaseModel):
    description: str = Field(description="Description of the item or service")
    quantity: int = Field(description="Number of items")
    unit_price: float = Field(description="Price per unit")
    total: float = Field(description="Total price for this line item")


class Invoice(BaseModel):
    invoice_number: str = Field(description="Unique invoice identifier")
    vendor_name: str = Field(description="Name of the vendor/company")
    invoice_date: str = Field(description="Date of invoice in YYYY-MM-DD format")
    items: List[InvoiceItem] = Field(description="List of items purchased")
    total_amount: float = Field(description="Total amount due")
    currency: str = Field(default="USD", description="Currency code")


class Resume(BaseModel):
    candidate_name: str = Field(description="Full name of the candidate")
    email: Optional[str] = Field(None, description="Contact email")
    phone: Optional[str] = Field(None, description="Contact phone number")
    skills: List[str] = Field(description="List of technical and soft skills")
    years_of_experience: float = Field(description="Total years of professional experience")
    current_company: Optional[str] = Field(None, description="Current or most recent employer")