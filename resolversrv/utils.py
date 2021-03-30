
from builtins import str
from builtins import range
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from sqlalchemy import and_
from sqlalchemy.dialects.postgresql import insert

from resolversrv.models import DataLinks

def get_records(bibcode, link_type=None, link_sub_type=None):
    """
    Queries nonbib.datalinks table and returns results.

    :param bibcode:
    :param link_type:
    :param link_sub_type:
    :return: list of json records or None
    """
    try:
        with current_app.session_scope() as session:
            if link_type is None:
                rows = session.query(DataLinks).filter(and_(DataLinks.bibcode == bibcode)).all()
                current_app.logger.info("Fetched records for bibcode = %s."  % (bibcode))
            elif link_sub_type is None:
                rows = session.query(DataLinks).filter(and_(DataLinks.bibcode == bibcode, DataLinks.link_type == link_type)).all()
                current_app.logger.info("Fetched records for bibcode = %s and link type = %s." % (bibcode, link_type))
            elif '%' in link_sub_type:
                rows = session.query(DataLinks).filter(and_(DataLinks.bibcode == bibcode, DataLinks.link_type == link_type,
                                                            DataLinks.link_sub_type.match(link_sub_type))).all()
                current_app.logger.info("Fetched records for bibcode = %s, link type = %s and link sub type = %s." %
                                        (bibcode, link_type, link_sub_type))
            else:
                rows = session.query(DataLinks).filter(and_(DataLinks.bibcode == bibcode, DataLinks.link_type == link_type,
                                                            DataLinks.link_sub_type == link_sub_type)).all()
                current_app.logger.info("Fetched records for bibcode = %s, link type = %s and link sub type = %s." %
                                        (bibcode, link_type, link_sub_type))

            if len(rows) == 0:
                if link_type is None:
                    current_app.logger.error("No records found for bibcode = %s." % (bibcode))
                elif link_sub_type is None:
                    current_app.logger.error("No records found for bibcode = %s and link type = %s." % (bibcode, link_type))
                else:
                    current_app.logger.error("No records found for bibcode = %s, link type = %s and link sub type = %s." %
                                             (bibcode, link_type, link_sub_type))
                return None

            results = []
            for row in rows:
                results.append(row.toJSON())
            return results
    except (SQLAlchemyError, DBAPIError) as e:
        current_app.logger.error('SQLAlchemy: ' + str(e))
        return None

def add_records(datalinks_records_list):
    """
    upserts records into db

    :param datalinks_records_list:
    :return: success boolean, plus a status text for retuning error message, if any, to the calling program
    """
    rows = []
    for i in range(len(datalinks_records_list.datalinks_records)):
        for j in range(len(datalinks_records_list.datalinks_records[i].data_links_rows)):
            rows.append([
                datalinks_records_list.datalinks_records[i].bibcode,
                datalinks_records_list.datalinks_records[i].data_links_rows[j].link_type,
                datalinks_records_list.datalinks_records[i].data_links_rows[j].link_sub_type,
                datalinks_records_list.datalinks_records[i].data_links_rows[j].url,
                datalinks_records_list.datalinks_records[i].data_links_rows[j].title,
                datalinks_records_list.datalinks_records[i].data_links_rows[j].item_count
            ])

    if len(rows) > 0:
        table = DataLinks.__table__
        stmt = insert(table).values(rows)

        no_update_cols = []
        update_cols = [c.name for c in table.c
                       if c not in list(table.primary_key.columns)
                       and c.name not in no_update_cols]

        on_conflict_stmt = stmt.on_conflict_do_update(
            index_elements=table.primary_key.columns,
            set_={k: getattr(stmt.excluded, k) for k in update_cols}
        )

        try:
            with current_app.session_scope() as session:
                session.execute(on_conflict_stmt)
            current_app.logger.info('updated db with new data successfully')
            return True, 'updated db with new data successfully'
        except (SQLAlchemyError, DBAPIError) as e:
            current_app.logger.error('SQLAlchemy: ' + str(e))
            return False, 'SQLAlchemy: ' + str(e)
    return False, 'unable to extract data from protobuf structure'


def del_records(bibcode_list):
    """

    :param bibcode_list:
    :return:
    """
    try:
        with current_app.session_scope() as session:
            count = 0
            for bibcode in bibcode_list:
                count += session.query(DataLinks).filter(DataLinks.bibcode == bibcode).delete(synchronize_session=False)
            session.commit()
    except (SQLAlchemyError, DBAPIError) as e:
        current_app.logger.error('SQLAlchemy: ' + str(e))
        return False, 'SQLAlchemy: ' + str(e)
    return True, count, 'removed ' + str(count) + ' records of ' + str(len(bibcode_list)) + ' bibcodes'