# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: datafakehouse.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13\x64\x61tafakehouse.proto\x12\rdatafakehouse\x1a\x1fgoogle/protobuf/timestamp.proto\"\x7f\n\x17\x43reateDbInstanceRequest\x12.\n\x0bsql_dialect\x18\x01 \x01(\x0e\x32\x19.datafakehouse.SQLDialect\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x17\n\ncatalog_id\x18\x03 \x01(\tH\x00\x88\x01\x01\x42\r\n\x0b_catalog_id\"\xde\x01\n\nDbInstance\x12\x16\n\x0e\x64\x62_instance_id\x18\x01 \x01(\t\x12\x0e\n\x06org_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x30\n\x0c\x63reated_time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x10\n\x08\x64\x62_token\x18\x05 \x01(\t\x12.\n\x0bsql_dialect\x18\x06 \x01(\x0e\x32\x19.datafakehouse.SQLDialect\x12\x17\n\ncatalog_id\x18\x07 \x01(\tH\x00\x88\x01\x01\x42\r\n\x0b_catalog_id\"\x9d\x02\n\x07\x43\x61talog\x12\x12\n\ncatalog_id\x18\x01 \x01(\t\x12\x0e\n\x06org_id\x18\x02 \x01(\t\x12\x30\n\x0c\x63reated_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12(\n\x04type\x18\x04 \x01(\x0e\x32\x1a.datafakehouse.CatalogType\x12\x0c\n\x04name\x18\x05 \x01(\t\x12\x0c\n\x04path\x18\x06 \x01(\t\x12\x35\n\x0c\x65xpires_time\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x00\x88\x01\x01\x12\x1b\n\x0e\x64\x62_instance_id\x18\x08 \x01(\tH\x01\x88\x01\x01\x42\x0f\n\r_expires_timeB\x11\n\x0f_db_instance_id\"N\n\"CreateCatalogFromDbInstanceRequest\x12\x16\n\x0e\x64\x62_instance_id\x18\x01 \x01(\t\x12\x10\n\x08\x64\x62_token\x18\x02 \x01(\t\"\xa4\x01\n\x14\x43reateCatalogRequest\x12(\n\x04type\x18\x04 \x01(\x0e\x32\x1a.datafakehouse.CatalogType\x12\x0c\n\x04name\x18\x05 \x01(\t\x12\x0c\n\x04path\x18\x06 \x01(\t\x12\x35\n\x0c\x65xpires_time\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x00\x88\x01\x01\x42\x0f\n\r_expires_time\"@\n\x15\x43reateCatalogResponse\x12\'\n\x07\x63\x61talog\x18\x01 \x01(\x0b\x32\x16.datafakehouse.Catalog\"\x15\n\x13ListCatalogsRequest\"\'\n\x11GetCatalogRequest\x12\x12\n\ncatalog_id\x18\x01 \x01(\t\".\n\x14GetDbInstanceRequest\x12\x16\n\x0e\x64\x62_instance_id\x18\x01 \x01(\t\"S\n\x15\x45xitDbInstanceRequest\x12\x16\n\x0e\x64\x62_instance_id\x18\x01 \x01(\t\x12\x15\n\x08\x64\x62_token\x18\x03 \x01(\tH\x00\x88\x01\x01\x42\x0b\n\t_db_token\"\x18\n\x16\x45xitDbInstanceResponse\"K\n\x12RunSQLQueryRequest\x12\x16\n\x0e\x64\x62_instance_id\x18\x01 \x01(\t\x12\x0b\n\x03sql\x18\x02 \x01(\t\x12\x10\n\x08\x64\x62_token\x18\x03 \x01(\t\"\x86\x04\n\x13RunSQLQueryResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12=\n\x05\x65rror\x18\x03 \x01(\x0b\x32,.datafakehouse.RunSQLQueryResponse.ErrorBodyH\x00\x12\x37\n\x04\x64\x61ta\x18\x04 \x01(\x0b\x32\'.datafakehouse.RunSQLQueryResponse.DataH\x00\x1a\xef\x01\n\tErrorBody\x12K\n\x08messages\x18\x01 \x03(\x0b\x32\x39.datafakehouse.RunSQLQueryResponse.ErrorBody.ErrorMessage\x1a\x94\x01\n\x0c\x45rrorMessage\x12\x10\n\x08severity\x18\x01 \x01(\t\x12\x12\n\nerror_type\x18\x02 \x01(\t\x12\x16\n\x0estart_position\x18\x03 \x01(\x03\x12\x14\n\x0c\x65nd_position\x18\x04 \x01(\x03\x12\x1c\n\x0frelation_entity\x18\x05 \x01(\tH\x00\x88\x01\x01\x42\x12\n\x10_relation_entity\x1al\n\x04\x44\x61ta\x12(\n\x06schema\x18\x01 \x01(\x0b\x32\x18.datafakehouse.SQLSchema\x12\x12\n\ntotal_rows\x18\x02 \x01(\x03\x12&\n\x04rows\x18\x03 \x03(\x0b\x32\x18.datafakehouse.ResultRowB\x06\n\x04\x62ody\"@\n\x08SQLField\x12\x0c\n\x04name\x18\x01 \x01(\t\x12&\n\x04type\x18\x02 \x01(\x0e\x32\x18.datafakehouse.FieldType\"4\n\tSQLSchema\x12\'\n\x06\x66ields\x18\x01 \x03(\x0b\x32\x17.datafakehouse.SQLField\"\x1b\n\tResultRow\x12\x0e\n\x06values\x18\x01 \x03(\t*\x1a\n\nSQLDialect\x12\x0c\n\x08\x42IGQUERY\x10\x00*7\n\x0b\x43\x61talogType\x12\x11\n\rMETADATA_SYNC\x10\x00\x12\x15\n\x11\x44\x42INSTANCE_OUTPUT\x10\x01*H\n\tFieldType\x12\r\n\tTIMESTAMP\x10\x00\x12\n\n\x06STRING\x10\x01\x12\t\n\x05INT64\x10\x02\x12\x0b\n\x07\x46LOAT64\x10\x03\x12\x08\n\x04\x42OOL\x10\x04\x32\xba\x05\n\rDatafakehouse\x12U\n\x10\x43reateDbInstance\x12&.datafakehouse.CreateDbInstanceRequest\x1a\x19.datafakehouse.DbInstance\x12T\n\x0bRunSQLQuery\x12!.datafakehouse.RunSQLQueryRequest\x1a\".datafakehouse.RunSQLQueryResponse\x12]\n\x0e\x45xitDbInstance\x12$.datafakehouse.ExitDbInstanceRequest\x1a%.datafakehouse.ExitDbInstanceResponse\x12O\n\rGetDbInstance\x12#.datafakehouse.GetDbInstanceRequest\x1a\x19.datafakehouse.DbInstance\x12L\n\rCreateCatalog\x12#.datafakehouse.CreateCatalogRequest\x1a\x16.datafakehouse.Catalog\x12h\n\x1b\x43reateCatalogFromDbInstance\x12\x31.datafakehouse.CreateCatalogFromDbInstanceRequest\x1a\x16.datafakehouse.Catalog\x12L\n\x0cListCatalogs\x12\".datafakehouse.ListCatalogsRequest\x1a\x16.datafakehouse.Catalog0\x01\x12\x46\n\nGetCatalog\x12 .datafakehouse.GetCatalogRequest\x1a\x16.datafakehouse.Catalogb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'datafakehouse_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_SQLDIALECT']._serialized_start=1996
  _globals['_SQLDIALECT']._serialized_end=2022
  _globals['_CATALOGTYPE']._serialized_start=2024
  _globals['_CATALOGTYPE']._serialized_end=2079
  _globals['_FIELDTYPE']._serialized_start=2081
  _globals['_FIELDTYPE']._serialized_end=2153
  _globals['_CREATEDBINSTANCEREQUEST']._serialized_start=71
  _globals['_CREATEDBINSTANCEREQUEST']._serialized_end=198
  _globals['_DBINSTANCE']._serialized_start=201
  _globals['_DBINSTANCE']._serialized_end=423
  _globals['_CATALOG']._serialized_start=426
  _globals['_CATALOG']._serialized_end=711
  _globals['_CREATECATALOGFROMDBINSTANCEREQUEST']._serialized_start=713
  _globals['_CREATECATALOGFROMDBINSTANCEREQUEST']._serialized_end=791
  _globals['_CREATECATALOGREQUEST']._serialized_start=794
  _globals['_CREATECATALOGREQUEST']._serialized_end=958
  _globals['_CREATECATALOGRESPONSE']._serialized_start=960
  _globals['_CREATECATALOGRESPONSE']._serialized_end=1024
  _globals['_LISTCATALOGSREQUEST']._serialized_start=1026
  _globals['_LISTCATALOGSREQUEST']._serialized_end=1047
  _globals['_GETCATALOGREQUEST']._serialized_start=1049
  _globals['_GETCATALOGREQUEST']._serialized_end=1088
  _globals['_GETDBINSTANCEREQUEST']._serialized_start=1090
  _globals['_GETDBINSTANCEREQUEST']._serialized_end=1136
  _globals['_EXITDBINSTANCEREQUEST']._serialized_start=1138
  _globals['_EXITDBINSTANCEREQUEST']._serialized_end=1221
  _globals['_EXITDBINSTANCERESPONSE']._serialized_start=1223
  _globals['_EXITDBINSTANCERESPONSE']._serialized_end=1247
  _globals['_RUNSQLQUERYREQUEST']._serialized_start=1249
  _globals['_RUNSQLQUERYREQUEST']._serialized_end=1324
  _globals['_RUNSQLQUERYRESPONSE']._serialized_start=1327
  _globals['_RUNSQLQUERYRESPONSE']._serialized_end=1845
  _globals['_RUNSQLQUERYRESPONSE_ERRORBODY']._serialized_start=1488
  _globals['_RUNSQLQUERYRESPONSE_ERRORBODY']._serialized_end=1727
  _globals['_RUNSQLQUERYRESPONSE_ERRORBODY_ERRORMESSAGE']._serialized_start=1579
  _globals['_RUNSQLQUERYRESPONSE_ERRORBODY_ERRORMESSAGE']._serialized_end=1727
  _globals['_RUNSQLQUERYRESPONSE_DATA']._serialized_start=1729
  _globals['_RUNSQLQUERYRESPONSE_DATA']._serialized_end=1837
  _globals['_SQLFIELD']._serialized_start=1847
  _globals['_SQLFIELD']._serialized_end=1911
  _globals['_SQLSCHEMA']._serialized_start=1913
  _globals['_SQLSCHEMA']._serialized_end=1965
  _globals['_RESULTROW']._serialized_start=1967
  _globals['_RESULTROW']._serialized_end=1994
  _globals['_DATAFAKEHOUSE']._serialized_start=2156
  _globals['_DATAFAKEHOUSE']._serialized_end=2854
# @@protoc_insertion_point(module_scope)
