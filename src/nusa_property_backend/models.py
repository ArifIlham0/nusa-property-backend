from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    Boolean,
    ForeignKey,
    DateTime,
    func
)
from sqlalchemy.orm import relationship
from .database import Base


class Property(Base):
    __tablename__ = "properties"

    id = Column(String(50), primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    price = Column(BigInteger, nullable=False)
    price_formatted = Column(String(100), nullable=False)
    installment_estimate = Column(String(100), nullable=False)
    bedrooms = Column(Integer, default=2)
    bathrooms = Column(Integer, default=1)
    carports = Column(Integer, default=1)
    building_area = Column(Integer, default=36)
    surface_area = Column(Integer, default=60)
    electricity_va = Column(Integer, default=1300)
    certificate_type = Column(String(50), default="SHM")
    tag_text = Column(String(100), nullable=False)
    tag_type = Column(String(50), nullable=False)
    image_url = Column(String(500), nullable=False)
    developer_name = Column(String(255), nullable=True)
    address_detail = Column(String(500), nullable=True)
    is_favorite = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())


class Document(Base):
    __tablename__ = "documents"

    id = Column(String(50), primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)
    status_label = Column(String(100), nullable=False)
    file_name = Column(String(255), nullable=True)
    file_meta = Column(String(255), nullable=True)
    file_path = Column(String(500), nullable=True)
    action_label = Column(String(100), nullable=False)
    order_index = Column(Integer, default=0)


class Sp3kApplication(Base):
    __tablename__ = "sp3k_applications"

    registration_number = Column(String(100), primary_key=True, index=True)
    developer = Column(String(255), nullable=False)
    unit_name = Column(String(255), nullable=False)
    approved_amount = Column(BigInteger, nullable=False)
    interest_rate_text = Column(String(100), nullable=False)
    monthly_installment = Column(BigInteger, nullable=False)
    tenor_years = Column(Integer, nullable=False)
    dp_paid = Column(BigInteger, nullable=False)
    status = Column(String(50), default="APPROVED")
    akad_date = Column(String(100), nullable=True)
    akad_location = Column(String(255), nullable=True)

    steps = relationship("Sp3kStep", back_populates="application", cascade="all, delete-orphan", order_by="Sp3kStep.step_number")


class Sp3kStep(Base):
    __tablename__ = "sp3k_steps"

    id = Column(Integer, primary_key=True, autoincrement=True)
    registration_number = Column(String(100), ForeignKey("sp3k_applications.registration_number", ondelete="CASCADE"), nullable=False)
    step_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    subtitle = Column(String(500), nullable=False)
    status = Column(String(50), nullable=False)
    status_badge_text = Column(String(100), nullable=True)

    application = relationship("Sp3kApplication", back_populates="steps")


class MortgageAdvisor(Base):
    __tablename__ = "mortgage_advisors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    bank = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    is_online = Column(Boolean, default=True)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    message = Column(String(500), nullable=False)
    type = Column(String(50), default="INFO")
    created_at = Column(DateTime, server_default=func.now())


class User(Base):
    __tablename__ = "users"

    id = Column(String(50), primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(String(50), primary_key=True)
    user_id = Column(String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    name = Column(String(255), nullable=False)
    greeting = Column(String(255), nullable=True)
    subtitle = Column(String(255), nullable=True)
    plafon_estimate = Column(BigInteger, default=0)
    financial_score = Column(String(50), nullable=True)
    financial_score_grade = Column(String(10), nullable=True)

    user = relationship("User", back_populates="profile")
