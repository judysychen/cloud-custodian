# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0
from c7n_tencentcloud.provider import resources
from c7n_tencentcloud.query import ResourceTypeInfo, QueryResourceManager
from c7n_tencentcloud.utils import PageMethod, isoformat_datetime_str
from c7n.filters.core import Filter
import pytz
from c7n.utils import type_schema


@resources.register("tdsql")
class TDSQL(QueryResourceManager):
    """
        TDSQL-C for MySQL: It combines the strengths of traditional databases, cloud computing,
        and cutting-edge hardware technologies to provide elastically scalable database services featuring
        high performance, security, and reliability, as well as full compatibility with MySQL 5.7 and 8.0.
        https://www.tencentcloud.com/document/product/1098/40615

        :example:

        .. code-block:: yaml

            policies:
            - name: tdsql-check
              resource: tencentcloud.tdsql
        """

    class resource_type(ResourceTypeInfo):
        """resource_type"""
        id = "InstanceId"
        endpoint = "dcdb.tencentcloudapi.com"
        service = "dcdb"
        version = "2018-04-11"
        enum_spec = ("DescribeDCDBInstances", "Response.Instances[]", {})
        metrics_enabled = True
        metrics_namespace = "QCE/DCDB"
        metrics_dimension_def = [("InstanceId", "InstanceId"), ("InstanceType", "InstanceType")]
        metrics_instance_id_name = "InstanceId"

        paging_def = {"method": PageMethod.Offset, "limit": {"key": "Limit", "value": 10}}
        resource_prefix = "instanceId"
        taggable = True

        datetime_fields_format = {
            "CreateTime": ("%Y-%m-%d %H:%M:%S", pytz.timezone("Asia/Shanghai"))
        }

    def augment(self, resources):
        for resource in resources:
            field_format = self.resource_type.datetime_fields_format["CreateTime"]
            resource["CreateTime"] = isoformat_datetime_str(resource["CreateTime"],
                                                                field_format[0],
                                                                field_format[1])
        return resources
