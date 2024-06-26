from datetime import datetime
from contextlib import contextmanager
from chronos.lib.config_parser import cfg
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from chronos.lib.root_logger import root_logger as logger
from sqlalchemy import create_engine, Column, INTEGER, REAL, BOOLEAN, DateTime

engine = create_engine("sqlite:///{}".format(cfg.db.path), echo=False, connect_args={"timeout": 15})
session_factory = sessionmaker(bind=engine)

Base = declarative_base()


class Boiler(Base):

    __tablename__ = "boiler"

    id = Column(INTEGER, primary_key=True)
    backup = Column(BOOLEAN, default=False, nullable=False)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    switched_timestamp = Column(DateTime, nullable=False)
    status = Column(INTEGER, default=0, nullable=False)
    manual_override = Column(INTEGER, default=0, nullable=False)
    system_supply_temp = Column(REAL, default=0, nullable=False)
    outlet_temp = Column(REAL, default=0, nullable=False)
    inlet_temp = Column(REAL, default=0, nullable=False)
    flue_temp = Column(REAL, default=0, nullable=False)
    cascade_current_power = Column(REAL, default=0, nullable=False)
    lead_firing_rate = Column(REAL, default=0, nullable=False)


class Chiller1(Base):

    __tablename__ = "chiller1"

    id = Column(INTEGER, primary_key=True)
    backup = Column(BOOLEAN, default=False, nullable=False)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    switched_timestamp = Column(DateTime, nullable=False)
    status = Column(INTEGER, default=0, nullable=False)
    manual_override = Column(INTEGER, default=0, nullable=False)


class Chiller2(Base):

    __tablename__ = "chiller2"

    id = Column(INTEGER, primary_key=True)
    backup = Column(BOOLEAN, default=False, nullable=False)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    switched_timestamp = Column(DateTime, nullable=False)
    status = Column(INTEGER, default=0, nullable=False)
    manual_override = Column(INTEGER, default=0, nullable=False)


class Chiller3(Base):

    __tablename__ = "chiller3"

    id = Column(INTEGER, primary_key=True)
    backup = Column(BOOLEAN, default=False, nullable=False)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    switched_timestamp = Column(DateTime, nullable=False)
    status = Column(INTEGER, default=0, nullable=False)
    manual_override = Column(INTEGER, default=0, nullable=False)


class Chiller4(Base):

    __tablename__ = "chiller4"

    id = Column(INTEGER, primary_key=True)
    backup = Column(BOOLEAN, default=False, nullable=False)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    switched_timestamp = Column(DateTime, nullable=False)
    status = Column(INTEGER, default=0, nullable=False)
    manual_override = Column(INTEGER, default=0, nullable=False)


class SummerValve(Base):

    __tablename__ = "summer_valve"

    id = Column(INTEGER, primary_key=True)
    backup = Column(BOOLEAN, default=False, nullable=False)
    status = Column(INTEGER, default=0, nullable=False)


class WinterValve(Base):

    __tablename__ = "winter_valve"

    id = Column(INTEGER, primary_key=True)
    backup = Column(BOOLEAN, default=False, nullable=False)
    status = Column(INTEGER, default=0, nullable=False)


class History(Base):

    __tablename__ = "history"

    id = Column(INTEGER, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    outside_temp = Column(REAL, default=0, nullable=False)
    effective_setpoint = Column(REAL, default=0, nullable=False)
    water_out_temp = Column(REAL, default=0, nullable=False)
    return_temp = Column(REAL, default=0, nullable=False)
    boiler_status = Column(INTEGER, default=0, nullable=False)
    cascade_fire_rate = Column(REAL, default=0, nullable=False)
    lead_fire_rate = Column(REAL, default=0, nullable=False)
    chiller1_status = Column(INTEGER, default=0, nullable=False)
    chiller2_status = Column(INTEGER, default=0, nullable=False)
    chiller3_status = Column(INTEGER, default=0, nullable=False)
    chiller4_status = Column(INTEGER, default=0, nullable=False)
    tha_setpoint = Column(REAL, default=0, nullable=False)
    setpoint_offset_winter = Column(REAL, default=0, nullable=False)
    setpoint_offset_summer = Column(REAL, default=0, nullable=False)
    tolerance = Column(REAL, default=0, nullable=False)
    boiler_manual_override = Column(INTEGER, default=0, nullable=False)
    chiller1_manual_override = Column(INTEGER, default=0, nullable=False)
    chiller2_manual_override = Column(INTEGER, default=0, nullable=False)
    chiller3_manual_override = Column(INTEGER, default=0, nullable=False)
    chiller4_manual_override = Column(INTEGER, default=0, nullable=False)
    mode = Column(INTEGER, default=1, nullable=False)
    cascade_time = Column(INTEGER, default=0, nullable=False)
    wind_speed = Column(REAL, default=0, nullable=False)
    avg_outside_temp = Column(REAL, default=0, nullable=False)
    avg_cascade_fire_rate = Column(REAL, default=0, nullable=False)
    delta = Column(INTEGER, default=0, nullable=False)


class SetpointLookup(Base):

    __tablename__ = "setpoint_lookup"

    id = Column(INTEGER, primary_key=True)
    wind_chill = Column(INTEGER)
    setpoint = Column(REAL)
    avg_wind_chill = Column(INTEGER)
    setpoint_offset = Column(INTEGER)


class Settings(Base):

    __tablename__ = "settings"

    id = Column(INTEGER, primary_key=True)
    setpoint_min = Column(REAL, default=0, nullable=False)
    setpoint_max = Column(REAL, default=0, nullable=False)
    setpoint_offset_summer = Column(REAL, default=0, nullable=False)
    setpoint_offset_winter = Column(REAL, default=0, nullable=False)
    tolerance = Column(REAL, default=0, nullable=False)
    mode_change_delta_temp = Column(INTEGER, default=0, nullable=False)
    cascade_time = Column(INTEGER, default=0, nullable=False)
    mode = Column(INTEGER, default=1, nullable=False)
    mode_switch_timestamp = Column(DateTime, default=datetime.now, nullable=False)
    mode_switch_lockout_time = Column(INTEGER, default=2, nullable=False)


@contextmanager
def session_scope():
    "Provide a transactional scope around a series of operations."
    Session = scoped_session(session_factory)
    Session()
    try:
        yield Session
        Session.commit()
    except Exception as e:
        logger.exception("Failed during interaction with the db: {}".format(e))
        Session.rollback()
    finally:
        Session.remove()
