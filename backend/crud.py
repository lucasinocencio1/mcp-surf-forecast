"""
CRUD operations and business logic for the surf school booking system.
"""

from typing import List, Optional

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from . import models, schemas


#surf school crud

def get_school(db: Session, school_id: int) -> Optional[models.SurfSchool]:
    return db.get(models.SurfSchool, school_id)


def get_schools(db: Session, skip: int = 0, limit: int = 100) -> List[models.SurfSchool]:
    return db.execute(select(models.SurfSchool).offset(skip).limit(limit)).scalars().all()


def create_school(db: Session, school_in: schemas.SurfSchoolCreate) -> models.SurfSchool:
    db_school = models.SurfSchool(**school_in.model_dump())
    db.add(db_school)
    db.commit()
    db.refresh(db_school)
    return db_school


def update_school(
    db: Session,
    db_school: models.SurfSchool,
    school_in: schemas.SurfSchoolUpdate,
) -> models.SurfSchool:
    data = school_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_school, field, value)
    db.add(db_school)
    db.commit()
    db.refresh(db_school)
    return db_school


def delete_school(db: Session, db_school: models.SurfSchool) -> None:
    db.delete(db_school)
    db.commit()


#instructor crud


def get_instructor(db: Session, instructor_id: int) -> Optional[models.Instructor]:
    return db.get(models.Instructor, instructor_id)


def get_instructors(db: Session, skip: int = 0, limit: int = 100) -> List[models.Instructor]:
    return db.execute(select(models.Instructor).offset(skip).limit(limit)).scalars().all()


def create_instructor(db: Session, instructor_in: schemas.InstructorCreate) -> models.Instructor:
    db_instructor = models.Instructor(**instructor_in.model_dump())
    db.add(db_instructor)
    db.commit()
    db.refresh(db_instructor)
    return db_instructor


def update_instructor(
    db: Session,
    db_instructor: models.Instructor,
    instructor_in: schemas.InstructorUpdate,
) -> models.Instructor:
    data = instructor_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_instructor, field, value)
    db.add(db_instructor)
    db.commit()
    db.refresh(db_instructor)
    return db_instructor


def delete_instructor(db: Session, db_instructor: models.Instructor) -> None:
    db.delete(db_instructor)
    db.commit()


#lesson crud


def get_lesson(db: Session, lesson_id: int) -> Optional[models.Lesson]:
    return db.get(models.Lesson, lesson_id)


def get_lessons(db: Session, skip: int = 0, limit: int = 100) -> List[models.Lesson]:
    return db.execute(select(models.Lesson).offset(skip).limit(limit)).scalars().all()


def create_lesson(db: Session, lesson_in: schemas.LessonCreate) -> models.Lesson:
    db_lesson = models.Lesson(**lesson_in.model_dump())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson


def update_lesson(
    db: Session,
    db_lesson: models.Lesson,
    lesson_in: schemas.LessonUpdate,
) -> models.Lesson:
    data = lesson_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_lesson, field, value)
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson


def delete_lesson(db: Session, db_lesson: models.Lesson) -> None:
    db.delete(db_lesson)
    db.commit()


#Schedule crud


def get_schedule(db: Session, schedule_id: int) -> Optional[models.Schedule]:
    return db.get(models.Schedule, schedule_id)


def get_schedules(db: Session, skip: int = 0, limit: int = 100) -> List[models.Schedule]:
    return db.execute(select(models.Schedule).offset(skip).limit(limit)).scalars().all()


def create_schedule(db: Session, schedule_in: schemas.ScheduleCreate) -> models.Schedule:
    db_schedule = models.Schedule(**schedule_in.model_dump())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


def update_schedule(
    db: Session,
    db_schedule: models.Schedule,
    schedule_in: schemas.ScheduleUpdate,
) -> models.Schedule:
    data = schedule_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_schedule, field, value)
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


def delete_schedule(db: Session, db_schedule: models.Schedule) -> None:
    db.delete(db_schedule)
    db.commit()


#Booking crud and business logic


def get_booking(db: Session, booking_id: int) -> Optional[models.Booking]:
    return db.get(models.Booking, booking_id)


def create_booking(db: Session, booking_in: schemas.BookingCreate) -> models.Booking:
    """
    Create a booking with business rules:
    - schedule must exist
    - schedule must be available
    - no double booking for the same schedule (pending/confirmed)
    - after booking, mark schedule.available = False
    """
    schedule = db.get(models.Schedule, booking_in.schedule_id)
    if not schedule:
        raise ValueError("Schedule not found")

    if not schedule.available:
        raise ValueError("Schedule is not available")

    # ensure schedule belongs to the same lesson
    if schedule.lesson_id != booking_in.lesson_id:
        raise ValueError("Schedule does not belong to the given lesson")

    # Check double-booking (pending/confirmed)
    existing = db.execute(
        select(models.Booking).where(
            and_(
                models.Booking.schedule_id == booking_in.schedule_id,
                models.Booking.status.in_(["pending", "confirmed"]),
            )
        )
    ).scalars().first()

    if existing:
        raise ValueError("Schedule already has an active booking")

    db_booking = models.Booking(
        **booking_in.model_dump(),
        status="confirmed",
    )
    db.add(db_booking)

    schedule.available = False
    db.add(schedule)

    db.commit()
    db.refresh(db_booking)
    return db_booking


def cancel_booking(db: Session, booking: models.Booking) -> models.Booking:
    """
    Cancel a booking and re-open the associated schedule.
    """
    booking.status = "cancelled"
    db.add(booking)

    schedule = db.get(models.Schedule, booking.schedule_id)
    if schedule:
        schedule.available = True
        db.add(schedule)

    db.commit()
    db.refresh(booking)
    return booking


