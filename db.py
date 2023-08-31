from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('postgresql://gmsjeogd:P3mjgSAjm_fMJHTa2qERhSET00dhNdhd@snuffleupagus.db.elephantsql.com/gmsjeogd')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
