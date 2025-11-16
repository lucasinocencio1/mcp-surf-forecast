"""
API router for the surf school booking system.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import get_db


router = APIRouter()


#surf school endpoints


@router.get("/schools", response_model=list[schemas.SurfSchool])
def list_schools(db: Session = Depends(get_db)):
    return crud.get_schools(db)


@router.get("/schools/{school_id}", response_model=schemas.SurfSchool)
def get_school(school_id: int, db: Session = Depends(get_db)):
    school = crud.get_school(db, school_id)
    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="School not found")
    return school


@router.post("/schools", response_model=schemas.SurfSchool, status_code=status.HTTP_201_CREATED)
def create_school(school_in: schemas.SurfSchoolCreate, db: Session = Depends(get_db)):
    return crud.create_school(db, school_in)


@router.put("/schools/{school_id}", response_model=schemas.SurfSchool)
def update_school(school_id: int, school_in: schemas.SurfSchoolUpdate, db: Session = Depends(get_db)):
    db_school = crud.get_school(db, school_id)
    if not db_school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="School not found")
    return crud.update_school(db, db_school, school_in)


@router.delete("/schools/{school_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_school(school_id: int, db: Session = Depends(get_db)):
    db_school = crud.get_school(db, school_id)
    if not db_school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="School not found")
    crud.delete_school(db, db_school)
    return None


# instructor endpoints


@router.get("/instructors", response_model=list[schemas.Instructor])
def list_instructors(db: Session = Depends(get_db)):
    return crud.get_instructors(db)


@router.get("/instructors/{instructor_id}", response_model=schemas.Instructor)
def get_instructor(instructor_id: int, db: Session = Depends(get_db)):
    instructor = crud.get_instructor(db, instructor_id)
    if not instructor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instructor not found")
    return instructor


@router.post("/instructors", response_model=schemas.Instructor, status_code=status.HTTP_201_CREATED)
def create_instructor(instructor_in: schemas.InstructorCreate, db: Session = Depends(get_db)):
    return crud.create_instructor(db, instructor_in)


@router.put("/instructors/{instructor_id}", response_model=schemas.Instructor)
def update_instructor(
    instructor_id: int,
    instructor_in: schemas.InstructorUpdate,
    db: Session = Depends(get_db),
):
    db_instructor = crud.get_instructor(db, instructor_id)
    if not db_instructor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instructor not found")
    return crud.update_instructor(db, db_instructor, instructor_in)


@router.delete("/instructors/{instructor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_instructor(instructor_id: int, db: Session = Depends(get_db)):
    db_instructor = crud.get_instructor(db, instructor_id)
    if not db_instructor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instructor not found")
    crud.delete_instructor(db, db_instructor)
    return None


# lesson endpoints


@router.get("/lessons", response_model=list[schemas.Lesson])
def list_lessons(db: Session = Depends(get_db)):
    return crud.get_lessons(db)


@router.get("/lessons/{lesson_id}", response_model=schemas.Lesson)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = crud.get_lesson(db, lesson_id)
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    return lesson


@router.post("/lessons", response_model=schemas.Lesson, status_code=status.HTTP_201_CREATED)
def create_lesson(lesson_in: schemas.LessonCreate, db: Session = Depends(get_db)):
    return crud.create_lesson(db, lesson_in)


@router.put("/lessons/{lesson_id}", response_model=schemas.Lesson)
def update_lesson(
    lesson_id: int,
    lesson_in: schemas.LessonUpdate,
    db: Session = Depends(get_db),
):
    db_lesson = crud.get_lesson(db, lesson_id)
    if not db_lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    return crud.update_lesson(db, db_lesson, lesson_in)


@router.delete("/lessons/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    db_lesson = crud.get_lesson(db, lesson_id)
    if not db_lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    crud.delete_lesson(db, db_lesson)
    return None


#schedule endpoints


@router.get("/schedules", response_model=list[schemas.Schedule])
def list_schedules(db: Session = Depends(get_db)):
    return crud.get_schedules(db)


@router.get("/schedules/{schedule_id}", response_model=schemas.Schedule)
def get_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = crud.get_schedule(db, schedule_id)
    if not schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
    return schedule


@router.post("/schedules", response_model=schemas.Schedule, status_code=status.HTTP_201_CREATED)
def create_schedule(schedule_in: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    return crud.create_schedule(db, schedule_in)


@router.put("/schedules/{schedule_id}", response_model=schemas.Schedule)
def update_schedule(
    schedule_id: int,
    schedule_in: schemas.ScheduleUpdate,
    db: Session = Depends(get_db),
):
    db_schedule = crud.get_schedule(db, schedule_id)
    if not db_schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
    return crud.update_schedule(db, db_schedule, schedule_in)


@router.delete("/schedules/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    db_schedule = crud.get_schedule(db, schedule_id)
    if not db_schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
    crud.delete_schedule(db, db_schedule)
    return None


#booking endpoints

@router.post("/bookings", response_model=schemas.Booking, status_code=status.HTTP_201_CREATED)
def create_booking(booking_in: schemas.BookingCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_booking(db, booking_in)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/bookings/{booking_id}", response_model=schemas.Booking)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = crud.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    return booking


@router.patch("/bookings/{booking_id}/cancel", response_model=schemas.BookingCancelResponse)
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = crud.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    if booking.status == "cancelled":
        return schemas.BookingCancelResponse(id=booking.id, status=booking.status)

    booking = crud.cancel_booking(db, booking)
    return schemas.BookingCancelResponse(id=booking.id, status=booking.status)


