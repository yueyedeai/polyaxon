// Copyright 2019 Polyaxon, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// Code generated by go-swagger; DO NOT EDIT.

package service_model

// This file was generated by the swagger tool.
// Editing this file might prove futile when you re-run the swagger generate command

import (
	"encoding/json"

	strfmt "github.com/go-openapi/strfmt"

	"github.com/go-openapi/errors"
	"github.com/go-openapi/validate"
)

// V1ConnectionKind Connection kinds
// swagger:model v1ConnectionKind
type V1ConnectionKind string

const (

	// V1ConnectionKindHostPath captures enum value "host_path"
	V1ConnectionKindHostPath V1ConnectionKind = "host_path"

	// V1ConnectionKindVolumeClaim captures enum value "volume_claim"
	V1ConnectionKindVolumeClaim V1ConnectionKind = "volume_claim"

	// V1ConnectionKindFtp captures enum value "ftp"
	V1ConnectionKindFtp V1ConnectionKind = "ftp"

	// V1ConnectionKindGcp captures enum value "gcp"
	V1ConnectionKindGcp V1ConnectionKind = "gcp"

	// V1ConnectionKindGcs captures enum value "gcs"
	V1ConnectionKindGcs V1ConnectionKind = "gcs"

	// V1ConnectionKindGcpcloudsql captures enum value "gcpcloudsql"
	V1ConnectionKindGcpcloudsql V1ConnectionKind = "gcpcloudsql"

	// V1ConnectionKindGrpc captures enum value "grpc"
	V1ConnectionKindGrpc V1ConnectionKind = "grpc"

	// V1ConnectionKindHdfs captures enum value "hdfs"
	V1ConnectionKindHdfs V1ConnectionKind = "hdfs"

	// V1ConnectionKindHTTP captures enum value "http"
	V1ConnectionKindHTTP V1ConnectionKind = "http"

	// V1ConnectionKindPigCli captures enum value "pig_cli"
	V1ConnectionKindPigCli V1ConnectionKind = "pig_cli"

	// V1ConnectionKindHiveCli captures enum value "hive_cli"
	V1ConnectionKindHiveCli V1ConnectionKind = "hive_cli"

	// V1ConnectionKindHiveMetastore captures enum value "hive_metastore"
	V1ConnectionKindHiveMetastore V1ConnectionKind = "hive_metastore"

	// V1ConnectionKindHiveServer2 captures enum value "hive_server2"
	V1ConnectionKindHiveServer2 V1ConnectionKind = "hive_server2"

	// V1ConnectionKindJdbc captures enum value "jdbc"
	V1ConnectionKindJdbc V1ConnectionKind = "jdbc"

	// V1ConnectionKindJenkins captures enum value "jenkins"
	V1ConnectionKindJenkins V1ConnectionKind = "jenkins"

	// V1ConnectionKindMysql captures enum value "mysql"
	V1ConnectionKindMysql V1ConnectionKind = "mysql"

	// V1ConnectionKindPostgres captures enum value "postgres"
	V1ConnectionKindPostgres V1ConnectionKind = "postgres"

	// V1ConnectionKindOracle captures enum value "oracle"
	V1ConnectionKindOracle V1ConnectionKind = "oracle"

	// V1ConnectionKindVertica captures enum value "vertica"
	V1ConnectionKindVertica V1ConnectionKind = "vertica"

	// V1ConnectionKindSqlite captures enum value "sqlite"
	V1ConnectionKindSqlite V1ConnectionKind = "sqlite"

	// V1ConnectionKindMssql captures enum value "mssql"
	V1ConnectionKindMssql V1ConnectionKind = "mssql"

	// V1ConnectionKindRedis captures enum value "redis"
	V1ConnectionKindRedis V1ConnectionKind = "redis"

	// V1ConnectionKindPresto captures enum value "presto"
	V1ConnectionKindPresto V1ConnectionKind = "presto"

	// V1ConnectionKindMongo captures enum value "mongo"
	V1ConnectionKindMongo V1ConnectionKind = "mongo"

	// V1ConnectionKindCassandra captures enum value "cassandra"
	V1ConnectionKindCassandra V1ConnectionKind = "cassandra"

	// V1ConnectionKindSamba captures enum value "samba"
	V1ConnectionKindSamba V1ConnectionKind = "samba"

	// V1ConnectionKindAws captures enum value "aws"
	V1ConnectionKindAws V1ConnectionKind = "aws"

	// V1ConnectionKindS3 captures enum value "s3"
	V1ConnectionKindS3 V1ConnectionKind = "s3"

	// V1ConnectionKindEmr captures enum value "emr"
	V1ConnectionKindEmr V1ConnectionKind = "emr"

	// V1ConnectionKindSnowflake captures enum value "snowflake"
	V1ConnectionKindSnowflake V1ConnectionKind = "snowflake"

	// V1ConnectionKindSSH captures enum value "ssh"
	V1ConnectionKindSSH V1ConnectionKind = "ssh"

	// V1ConnectionKindCloudant captures enum value "cloudant"
	V1ConnectionKindCloudant V1ConnectionKind = "cloudant"

	// V1ConnectionKindDatabricks captures enum value "databricks"
	V1ConnectionKindDatabricks V1ConnectionKind = "databricks"

	// V1ConnectionKindSegment captures enum value "segment"
	V1ConnectionKindSegment V1ConnectionKind = "segment"

	// V1ConnectionKindAzureDataLake captures enum value "azure_data_lake"
	V1ConnectionKindAzureDataLake V1ConnectionKind = "azure_data_lake"

	// V1ConnectionKindAzureCosmos captures enum value "azure_cosmos"
	V1ConnectionKindAzureCosmos V1ConnectionKind = "azure_cosmos"

	// V1ConnectionKindWasb captures enum value "wasb"
	V1ConnectionKindWasb V1ConnectionKind = "wasb"

	// V1ConnectionKindRegistry captures enum value "registry"
	V1ConnectionKindRegistry V1ConnectionKind = "registry"

	// V1ConnectionKindGit captures enum value "git"
	V1ConnectionKindGit V1ConnectionKind = "git"
)

// for schema
var v1ConnectionKindEnum []interface{}

func init() {
	var res []V1ConnectionKind
	if err := json.Unmarshal([]byte(`["host_path","volume_claim","ftp","gcp","gcs","gcpcloudsql","grpc","hdfs","http","pig_cli","hive_cli","hive_metastore","hive_server2","jdbc","jenkins","mysql","postgres","oracle","vertica","sqlite","mssql","redis","presto","mongo","cassandra","samba","aws","s3","emr","snowflake","ssh","cloudant","databricks","segment","azure_data_lake","azure_cosmos","wasb","registry","git"]`), &res); err != nil {
		panic(err)
	}
	for _, v := range res {
		v1ConnectionKindEnum = append(v1ConnectionKindEnum, v)
	}
}

func (m V1ConnectionKind) validateV1ConnectionKindEnum(path, location string, value V1ConnectionKind) error {
	if err := validate.Enum(path, location, value, v1ConnectionKindEnum); err != nil {
		return err
	}
	return nil
}

// Validate validates this v1 connection kind
func (m V1ConnectionKind) Validate(formats strfmt.Registry) error {
	var res []error

	// value enum
	if err := m.validateV1ConnectionKindEnum("", "body", m); err != nil {
		return err
	}

	if len(res) > 0 {
		return errors.CompositeValidationError(res...)
	}
	return nil
}