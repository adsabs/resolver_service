
from builtins import str
from builtins import range
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
from sqlalchemy.dialects.postgresql import insert

from google.protobuf import json_format

from resolversrv.models import DataLinks, Documents

def get_records(bibcode, link_type=None, link_sub_type=None):
    """
    Queries nonbib.datalinks table and returns results.

    :param bibcode:
    :param link_type:
    :param link_sub_type:
    :return: list of json records or None
    """
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
    return None


def get_records_new(bibcode, link_type=None, link_sub_type=None):
    """
    Queries nonbib.documents table and returns results.

    :param bibcode:
    :param link_type:
    :param link_sub_type:
    :return: list of json records or None
    """
    with current_app.session_scope() as session:
        # just bibcode was passed in
        if link_type is None:
            row = session.query(Documents).filter(Documents.bibcode == bibcode).first()
            current_app.logger.info("Fetched records for bibcode = %s."  % (bibcode))
        # query on bibcocd and link_type
        elif link_sub_type is None:
            row = session.query(Documents.links[link_type].label('links')).filter(Documents.bibcode == bibcode).first()
            if row:
                row = Documents(bibcode, [], {link_type: row[0]})
            current_app.logger.info("Fetched records for bibcode = %s and link type = %s." % (bibcode, link_type))
        # query on all three bibcode, link_type, and link_sub_type (with or without wildcard)
        elif '%' in link_sub_type:
            # get all the records for link_type and go through them to determine if they match wildcard string
            row = session.query(Documents.links[link_type].label('links')).filter(Documents.bibcode == bibcode).first()
            partial_link_sub_type = link_sub_type.replace('%', '')
            try:
                link_sub_type_wildcard = {}
                for key, value in row[0].items():
                    if partial_link_sub_type in key:
                        link_sub_type_wildcard.update({key: value})
                if len(link_sub_type_wildcard) > 0:
                    row = Documents(bibcode, [], {link_type: link_sub_type_wildcard})
                else:
                    row = {}
            except (KeyError, AttributeError):
                row = {}
            current_app.logger.info("Fetched records for bibcode = %s, link type = %s and link sub type = %s." %
                                    (bibcode, link_type, link_sub_type))
        else:
            row = session.query(Documents.links[link_type][link_sub_type].label('links')).filter(Documents.bibcode == bibcode).first()
            if row:
                row = Documents(bibcode, [], {link_type: {link_sub_type: row[0]}})
            current_app.logger.info("Fetched records for bibcode = %s, link type = %s and link sub type = %s." %
                                    (bibcode, link_type, link_sub_type))

        if not row:
            if link_type is None:
                current_app.logger.error("No records found for bibcode = %s." % (bibcode))
            elif link_sub_type is None:
                current_app.logger.error("No records found for bibcode = %s and link type = %s." % (bibcode, link_type))
            else:
                current_app.logger.error("No records found for bibcode = %s, link type = %s and link sub type = %s." %
                                         (bibcode, link_type, link_sub_type))
            return None

        return row.toJSON()
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
        except SQLAlchemyError as e:
            current_app.logger.error('SQLAlchemy: ' + str(e))
            return False, 'SQLAlchemy: ' + str(e)
    return False, 'unable to add records to the database'


def add_records_new(documents):
    """
    upserts records into db

    :param documents:
    :return: success boolean, plus a status text for retuning error message, if any, to the calling program
    """
    rows = []
    for doc in documents.document_records:
        rows.append({"bibcode":doc.bibcode,
                     "identifier": doc.identifier,
                     "links": json_format.MessageToDict(doc.links)})

    if len(rows) > 0:
        table = Documents.__table__
        stmt = insert(table).values(rows)

        # get list of fields making up primary key
        primary_keys = [c.name for c in list(table.primary_key.columns)]
        # define dict of non-primary keys for updating
        update_dict = {c.name: c for c in stmt.excluded if not c.primary_key}

        on_conflict_stmt = stmt.on_conflict_do_update(index_elements=primary_keys, set_=update_dict)

        try:
            with current_app.session_scope() as session:
                session.execute(on_conflict_stmt)
            current_app.logger.info('updated db with new data successfully')
            return True, 'updated db with new data successfully'
        except SQLAlchemyError as e:
            session.rollback()
            current_app.logger.error('SQLAlchemy: ' + str(e))
            return False, 'SQLAlchemy: ' + str(e)
    return False, 'unable to add records to the database'


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
    except SQLAlchemyError as e:
        session.rollback()
        current_app.logger.error('SQLAlchemy: ' + str(e))
        return False, 'SQLAlchemy: ' + str(e)
    return True, count, 'removed ' + str(count) + ' records of ' + str(len(bibcode_list)) + ' bibcodes'


def del_records_new(bibcode_list):
    """

    :param bibcode_list:
    :return:
    """
    try:
        with current_app.session_scope() as session:
            count = 0
            for bibcode in bibcode_list:
                count += session.query(Documents).filter(Documents.bibcode == bibcode).delete(synchronize_session=False)
            session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        current_app.logger.error('SQLAlchemy: ' + str(e))
        return False, 'SQLAlchemy: ' + str(e)
    return True, count, 'removed ' + str(count) + ' records of ' + str(len(bibcode_list)) + ' bibcodes'


def get_ids(identifier_list):
    """
    returns list of bibcodes and identifiers for the input identifier_list

    :param identifier_list:
    :return:
    """
    query = "SELECT bibcode,identifier FROM documents WHERE identifier && '{\"%s\"}';"%('","'.join(identifier_list))
    with current_app.session_scope() as session:
        rows = session.execute(query)
        if rows.rowcount > 0:
            message = "Fetched %d records for %d inputted identifiers." % (len(identifier_list), rows.rowcount)
            current_app.logger.info(message)
            return [dict(row) for row in rows], message
        current_app.logger.error('no matches found in database')
    return None, 'no matches found in database'
