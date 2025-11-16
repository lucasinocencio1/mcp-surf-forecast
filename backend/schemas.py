"""
Pydantic schemas for the surf school booking system.
"""

from datetime import date, time
from typing import Optional, Literal

from pydantic import BaseModel, EmailStr, Field


#surf school booking system schemas


class SurfSchoolBase(BaseModel):
    name: str = Field(..., max_length=255)
    location: str = Field(..., max_length=255)
    description: Optional[str] = Field(None, max_length=1024)
    rating: float = Field(0.0, ge=0, le=5)


class SurfSchoolCreate(SurfSchoolBase):
    pass


class SurfSchoolUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=1024)
    rating: Optional[float] = Field(None, ge=0, le=5)


class SurfSchoolInDBBase(SurfSchoolBase):
    id: int

    class Config:
        from_attributes = True


class SurfSchool(SurfSchoolInDBBase):
    pass


# Instructor


class InstructorBase(BaseModel):
    name: str = Field(..., max_length=255)
    experience_years: int = Field(..., ge=0)
    school_id: int


class InstructorCreate(InstructorBase):
    pass


class InstructorUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    experience_years: Optional[int] = Field(None, ge=0)
    school_id: Optional[int]


class InstructorInDBBase(InstructorBase):
    id: int

    class Config:
        from_attributes = True


class Instructor(InstructorInDBBase):
    pass


# Lesson


LessonLevel = Literal["beginner", "intermediate", "advanced"]


class LessonBase(BaseModel):
    school_id: int
    instructor_id: int
    level: LessonLevel
    duration_minutes: int = Field(..., gt=0)
    price: float = Field(..., gt=0)


class LessonCreate(LessonBase):
    pass


class LessonUpdate(BaseModel):
    school_id: Optional[int]
    instructor_id: Optional[int]
    level: Optional[LessonLevel]
    duration_minutes: Optional[int] = Field(None, gt=0)
    price: Optional[float] = Field(None, gt=0)


class LessonInDBBase(LessonBase):
    id: int

    class Config:
        from_attributes = True


class Lesson(LessonInDBBase):
    pass


# Schedule


class ScheduleBase(BaseModel):
    lesson_id: int
    date: date
    start_time: time
    end_time: time
    available: bool = True


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleUpdate(BaseModel):
    lesson_id: Optional[int]
    date: Optional[date]
    start_time: Optional[time]
    end_time: Optional[time]
    available: Optional[bool]


class ScheduleInDBBase(ScheduleBase):
    id: int

    class Config:
        from_attributes = True


class Schedule(ScheduleInDBBase):
    pass

# Booking

BookingStatus = Literal["pending", "confirmed", "cancelled"]


class BookingBase(BaseModel):
    student_name: str = Field(..., max_length=255)
    student_email: EmailStr
    lesson_id: int
    schedule_id: int


class BookingCreate(BookingBase):
    # status is managed by business logic; default to confirmed on creation
    pass


class BookingInDBBase(BookingBase):
    id: int
    status: BookingStatus

    class Config:
        from_attributes = True


class Booking(BookingInDBBase):
    pass


class BookingCancelResponse(BaseModel):
    id: int
    status: BookingStatus


