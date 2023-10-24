# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel


class AddResolverEndpointRequestIpConfig(TeaModel):
    def __init__(self, az_id=None, cidr_block=None, ip=None, v_switch_id=None):
        self.az_id = az_id  # type: str
        self.cidr_block = cidr_block  # type: str
        self.ip = ip  # type: str
        self.v_switch_id = v_switch_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(AddResolverEndpointRequestIpConfig, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.az_id is not None:
            result['AzId'] = self.az_id
        if self.cidr_block is not None:
            result['CidrBlock'] = self.cidr_block
        if self.ip is not None:
            result['Ip'] = self.ip
        if self.v_switch_id is not None:
            result['VSwitchId'] = self.v_switch_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('AzId') is not None:
            self.az_id = m.get('AzId')
        if m.get('CidrBlock') is not None:
            self.cidr_block = m.get('CidrBlock')
        if m.get('Ip') is not None:
            self.ip = m.get('Ip')
        if m.get('VSwitchId') is not None:
            self.v_switch_id = m.get('VSwitchId')
        return self


class AddResolverEndpointRequest(TeaModel):
    def __init__(self, ip_config=None, lang=None, name=None, security_group_id=None, vpc_id=None, vpc_region_id=None):
        self.ip_config = ip_config  # type: list[AddResolverEndpointRequestIpConfig]
        self.lang = lang  # type: str
        self.name = name  # type: str
        self.security_group_id = security_group_id  # type: str
        self.vpc_id = vpc_id  # type: str
        self.vpc_region_id = vpc_region_id  # type: str

    def validate(self):
        if self.ip_config:
            for k in self.ip_config:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(AddResolverEndpointRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        result['IpConfig'] = []
        if self.ip_config is not None:
            for k in self.ip_config:
                result['IpConfig'].append(k.to_map() if k else None)
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.name is not None:
            result['Name'] = self.name
        if self.security_group_id is not None:
            result['SecurityGroupId'] = self.security_group_id
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.vpc_region_id is not None:
            result['VpcRegionId'] = self.vpc_region_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        self.ip_config = []
        if m.get('IpConfig') is not None:
            for k in m.get('IpConfig'):
                temp_model = AddResolverEndpointRequestIpConfig()
                self.ip_config.append(temp_model.from_map(k))
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('SecurityGroupId') is not None:
            self.security_group_id = m.get('SecurityGroupId')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('VpcRegionId') is not None:
            self.vpc_region_id = m.get('VpcRegionId')
        return self


class AddResolverEndpointResponseBody(TeaModel):
    def __init__(self, endpoint_id=None, request_id=None):
        self.endpoint_id = endpoint_id  # type: str
        self.request_id = request_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(AddResolverEndpointResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.endpoint_id is not None:
            result['EndpointId'] = self.endpoint_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('EndpointId') is not None:
            self.endpoint_id = m.get('EndpointId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class AddResolverEndpointResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: AddResolverEndpointResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(AddResolverEndpointResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = AddResolverEndpointResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class AddResolverRuleRequestForwardIp(TeaModel):
    def __init__(self, ip=None, port=None):
        self.ip = ip  # type: str
        self.port = port  # type: int

    def validate(self):
        pass

    def to_map(self):
        _map = super(AddResolverRuleRequestForwardIp, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.ip is not None:
            result['Ip'] = self.ip
        if self.port is not None:
            result['Port'] = self.port
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Ip') is not None:
            self.ip = m.get('Ip')
        if m.get('Port') is not None:
            self.port = m.get('Port')
        return self


class AddResolverRuleRequest(TeaModel):
    def __init__(self, endpoint_id=None, forward_ip=None, lang=None, name=None, type=None, zone_name=None):
        self.endpoint_id = endpoint_id  # type: str
        self.forward_ip = forward_ip  # type: list[AddResolverRuleRequestForwardIp]
        self.lang = lang  # type: str
        self.name = name  # type: str
        self.type = type  # type: str
        self.zone_name = zone_name  # type: str

    def validate(self):
        if self.forward_ip:
            for k in self.forward_ip:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(AddResolverRuleRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.endpoint_id is not None:
            result['EndpointId'] = self.endpoint_id
        result['ForwardIp'] = []
        if self.forward_ip is not None:
            for k in self.forward_ip:
                result['ForwardIp'].append(k.to_map() if k else None)
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.name is not None:
            result['Name'] = self.name
        if self.type is not None:
            result['Type'] = self.type
        if self.zone_name is not None:
            result['ZoneName'] = self.zone_name
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('EndpointId') is not None:
            self.endpoint_id = m.get('EndpointId')
        self.forward_ip = []
        if m.get('ForwardIp') is not None:
            for k in m.get('ForwardIp'):
                temp_model = AddResolverRuleRequestForwardIp()
                self.forward_ip.append(temp_model.from_map(k))
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('ZoneName') is not None:
            self.zone_name = m.get('ZoneName')
        return self


class AddResolverRuleResponseBody(TeaModel):
    def __init__(self, request_id=None, rule_id=None):
        self.request_id = request_id  # type: str
        self.rule_id = rule_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(AddResolverRuleResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        return self


class AddResolverRuleResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: AddResolverRuleResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(AddResolverRuleResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = AddResolverRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class AddUserVpcAuthorizationRequest(TeaModel):
    def __init__(self, auth_channel=None, auth_code=None, auth_type=None, authorized_user_id=None):
        self.auth_channel = auth_channel  # type: str
        self.auth_code = auth_code  # type: str
        self.auth_type = auth_type  # type: str
        self.authorized_user_id = authorized_user_id  # type: long

    def validate(self):
        pass

    def to_map(self):
        _map = super(AddUserVpcAuthorizationRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.auth_channel is not None:
            result['AuthChannel'] = self.auth_channel
        if self.auth_code is not None:
            result['AuthCode'] = self.auth_code
        if self.auth_type is not None:
            result['AuthType'] = self.auth_type
        if self.authorized_user_id is not None:
            result['AuthorizedUserId'] = self.authorized_user_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('AuthChannel') is not None:
            self.auth_channel = m.get('AuthChannel')
        if m.get('AuthCode') is not None:
            self.auth_code = m.get('AuthCode')
        if m.get('AuthType') is not None:
            self.auth_type = m.get('AuthType')
        if m.get('AuthorizedUserId') is not None:
            self.authorized_user_id = m.get('AuthorizedUserId')
        return self


class AddUserVpcAuthorizationResponseBody(TeaModel):
    def __init__(self, request_id=None):
        self.request_id = request_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(AddUserVpcAuthorizationResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class AddUserVpcAuthorizationResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: AddUserVpcAuthorizationResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(AddUserVpcAuthorizationResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = AddUserVpcAuthorizationResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class AddZoneRequest(TeaModel):
    def __init__(self, client_token=None, lang=None, proxy_pattern=None, resource_group_id=None, zone_name=None,
                 zone_tag=None, zone_type=None):
        self.client_token = client_token  # type: str
        self.lang = lang  # type: str
        self.proxy_pattern = proxy_pattern  # type: str
        self.resource_group_id = resource_group_id  # type: str
        self.zone_name = zone_name  # type: str
        self.zone_tag = zone_tag  # type: str
        self.zone_type = zone_type  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(AddZoneRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.proxy_pattern is not None:
            result['ProxyPattern'] = self.proxy_pattern
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.zone_name is not None:
            result['ZoneName'] = self.zone_name
        if self.zone_tag is not None:
            result['ZoneTag'] = self.zone_tag
        if self.zone_type is not None:
            result['ZoneType'] = self.zone_type
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('ProxyPattern') is not None:
            self.proxy_pattern = m.get('ProxyPattern')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('ZoneName') is not None:
            self.zone_name = m.get('ZoneName')
        if m.get('ZoneTag') is not None:
            self.zone_tag = m.get('ZoneTag')
        if m.get('ZoneType') is not None:
            self.zone_type = m.get('ZoneType')
        return self


class AddZoneResponseBody(TeaModel):
    def __init__(self, request_id=None, success=None, zone_id=None, zone_name=None):
        self.request_id = request_id  # type: str
        self.success = success  # type: bool
        # zone ID。
        self.zone_id = zone_id  # type: str
        self.zone_name = zone_name  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(AddZoneResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        if self.zone_name is not None:
            result['ZoneName'] = self.zone_name
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        if m.get('ZoneName') is not None:
            self.zone_name = m.get('ZoneName')
        return self


class AddZoneResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: AddZoneResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(AddZoneResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = AddZoneResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class AddZoneRecordRequest(TeaModel):
    def __init__(self, client_token=None, lang=None, line=None, priority=None, remark=None, rr=None, ttl=None,
                 type=None, user_client_ip=None, value=None, weight=None, zone_id=None):
        self.client_token = client_token  # type: str
        self.lang = lang  # type: str
        self.line = line  # type: str
        self.priority = priority  # type: int
        self.remark = remark  # type: str
        self.rr = rr  # type: str
        self.ttl = ttl  # type: int
        self.type = type  # type: str
        self.user_client_ip = user_client_ip  # type: str
        self.value = value  # type: str
        self.weight = weight  # type: int
        # Zone ID。
        self.zone_id = zone_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(AddZoneRecordRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.line is not None:
            result['Line'] = self.line
        if self.priority is not None:
            result['Priority'] = self.priority
        if self.remark is not None:
            result['Remark'] = self.remark
        if self.rr is not None:
            result['Rr'] = self.rr
        if self.ttl is not None:
            result['Ttl'] = self.ttl
        if self.type is not None:
            result['Type'] = self.type
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.value is not None:
            result['Value'] = self.value
        if self.weight is not None:
            result['Weight'] = self.weight
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('Line') is not None:
            self.line = m.get('Line')
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        if m.get('Rr') is not None:
            self.rr = m.get('Rr')
        if m.get('Ttl') is not None:
            self.ttl = m.get('Ttl')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Weight') is not None:
            self.weight = m.get('Weight')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        return self


class AddZoneRecordResponseBody(TeaModel):
    def __init__(self, record_id=None, request_id=None, success=None):
        self.record_id = record_id  # type: long
        self.request_id = request_id  # type: str
        self.success = success  # type: bool

    def validate(self):
        pass

    def to_map(self):
        _map = super(AddZoneRecordResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.record_id is not None:
            result['RecordId'] = self.record_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RecordId') is not None:
            self.record_id = m.get('RecordId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class AddZoneRecordResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: AddZoneRecordResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(AddZoneRecordResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = AddZoneRecordResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class BindResolverRuleVpcRequestVpc(TeaModel):
    def __init__(self, region_id=None, vpc_id=None, vpc_type=None):
        self.region_id = region_id  # type: str
        # vpcID
        self.vpc_id = vpc_id  # type: str
        self.vpc_type = vpc_type  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(BindResolverRuleVpcRequestVpc, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.vpc_type is not None:
            result['VpcType'] = self.vpc_type
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('VpcType') is not None:
            self.vpc_type = m.get('VpcType')
        return self


class BindResolverRuleVpcRequest(TeaModel):
    def __init__(self, lang=None, rule_id=None, vpc=None):
        self.lang = lang  # type: str
        self.rule_id = rule_id  # type: str
        self.vpc = vpc  # type: list[BindResolverRuleVpcRequestVpc]

    def validate(self):
        if self.vpc:
            for k in self.vpc:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(BindResolverRuleVpcRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        result['Vpc'] = []
        if self.vpc is not None:
            for k in self.vpc:
                result['Vpc'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        self.vpc = []
        if m.get('Vpc') is not None:
            for k in m.get('Vpc'):
                temp_model = BindResolverRuleVpcRequestVpc()
                self.vpc.append(temp_model.from_map(k))
        return self


class BindResolverRuleVpcResponseBody(TeaModel):
    def __init__(self, request_id=None):
        self.request_id = request_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(BindResolverRuleVpcResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class BindResolverRuleVpcResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: BindResolverRuleVpcResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(BindResolverRuleVpcResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = BindResolverRuleVpcResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class BindZoneVpcRequestVpcs(TeaModel):
    def __init__(self, region_id=None, vpc_id=None, vpc_type=None):
        self.region_id = region_id  # type: str
        self.vpc_id = vpc_id  # type: str
        self.vpc_type = vpc_type  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(BindZoneVpcRequestVpcs, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.vpc_type is not None:
            result['VpcType'] = self.vpc_type
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('VpcType') is not None:
            self.vpc_type = m.get('VpcType')
        return self


class BindZoneVpcRequest(TeaModel):
    def __init__(self, client_token=None, lang=None, user_client_ip=None, vpcs=None, zone_id=None):
        self.client_token = client_token  # type: str
        self.lang = lang  # type: str
        self.user_client_ip = user_client_ip  # type: str
        self.vpcs = vpcs  # type: list[BindZoneVpcRequestVpcs]
        self.zone_id = zone_id  # type: str

    def validate(self):
        if self.vpcs:
            for k in self.vpcs:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(BindZoneVpcRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        result['Vpcs'] = []
        if self.vpcs is not None:
            for k in self.vpcs:
                result['Vpcs'].append(k.to_map() if k else None)
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        self.vpcs = []
        if m.get('Vpcs') is not None:
            for k in m.get('Vpcs'):
                temp_model = BindZoneVpcRequestVpcs()
                self.vpcs.append(temp_model.from_map(k))
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        return self


class BindZoneVpcResponseBody(TeaModel):
    def __init__(self, request_id=None):
        self.request_id = request_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(BindZoneVpcResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class BindZoneVpcResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: BindZoneVpcResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(BindZoneVpcResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = BindZoneVpcResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CheckZoneNameRequest(TeaModel):
    def __init__(self, lang=None, user_client_ip=None, zone_name=None):
        self.lang = lang  # type: str
        self.user_client_ip = user_client_ip  # type: str
        self.zone_name = zone_name  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(CheckZoneNameRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.zone_name is not None:
            result['ZoneName'] = self.zone_name
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('ZoneName') is not None:
            self.zone_name = m.get('ZoneName')
        return self


class CheckZoneNameResponseBody(TeaModel):
    def __init__(self, check=None, request_id=None, success=None):
        self.check = check  # type: bool
        self.request_id = request_id  # type: str
        self.success = success  # type: bool

    def validate(self):
        pass

    def to_map(self):
        _map = super(CheckZoneNameResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.check is not None:
            result['Check'] = self.check
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Check') is not None:
            self.check = m.get('Check')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CheckZoneNameResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: CheckZoneNameResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(CheckZoneNameResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CheckZoneNameResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteResolverEndpointRequest(TeaModel):
    def __init__(self, endpoint_id=None, lang=None):
        self.endpoint_id = endpoint_id  # type: str
        self.lang = lang  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DeleteResolverEndpointRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.endpoint_id is not None:
            result['EndpointId'] = self.endpoint_id
        if self.lang is not None:
            result['Lang'] = self.lang
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('EndpointId') is not None:
            self.endpoint_id = m.get('EndpointId')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        return self


class DeleteResolverEndpointResponseBody(TeaModel):
    def __init__(self, request_id=None):
        self.request_id = request_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DeleteResolverEndpointResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteResolverEndpointResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: DeleteResolverEndpointResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(DeleteResolverEndpointResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteResolverEndpointResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteResolverRuleRequest(TeaModel):
    def __init__(self, lang=None, rule_id=None):
        self.lang = lang  # type: str
        self.rule_id = rule_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DeleteResolverRuleRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        return self


class DeleteResolverRuleResponseBody(TeaModel):
    def __init__(self, request_id=None):
        self.request_id = request_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DeleteResolverRuleResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteResolverRuleResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: DeleteResolverRuleResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(DeleteResolverRuleResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteResolverRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteUserVpcAuthorizationRequest(TeaModel):
    def __init__(self, auth_type=None, authorized_user_id=None):
        self.auth_type = auth_type  # type: str
        self.authorized_user_id = authorized_user_id  # type: long

    def validate(self):
        pass

    def to_map(self):
        _map = super(DeleteUserVpcAuthorizationRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.auth_type is not None:
            result['AuthType'] = self.auth_type
        if self.authorized_user_id is not None:
            result['AuthorizedUserId'] = self.authorized_user_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('AuthType') is not None:
            self.auth_type = m.get('AuthType')
        if m.get('AuthorizedUserId') is not None:
            self.authorized_user_id = m.get('AuthorizedUserId')
        return self


class DeleteUserVpcAuthorizationResponseBody(TeaModel):
    def __init__(self, request_id=None):
        self.request_id = request_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DeleteUserVpcAuthorizationResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteUserVpcAuthorizationResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: DeleteUserVpcAuthorizationResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(DeleteUserVpcAuthorizationResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteUserVpcAuthorizationResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteZoneRequest(TeaModel):
    def __init__(self, client_token=None, lang=None, user_client_ip=None, zone_id=None):
        self.client_token = client_token  # type: str
        self.lang = lang  # type: str
        self.user_client_ip = user_client_ip  # type: str
        # zone ID
        self.zone_id = zone_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DeleteZoneRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        return self


class DeleteZoneResponseBody(TeaModel):
    def __init__(self, request_id=None, zone_id=None):
        self.request_id = request_id  # type: str
        # zone ID
        self.zone_id = zone_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DeleteZoneResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        return self


class DeleteZoneResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: DeleteZoneResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(DeleteZoneResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteZoneResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteZoneRecordRequest(TeaModel):
    def __init__(self, client_token=None, lang=None, record_id=None, user_client_ip=None):
        self.client_token = client_token  # type: str
        self.lang = lang  # type: str
        self.record_id = record_id  # type: long
        self.user_client_ip = user_client_ip  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DeleteZoneRecordRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.record_id is not None:
            result['RecordId'] = self.record_id
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('RecordId') is not None:
            self.record_id = m.get('RecordId')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        return self


class DeleteZoneRecordResponseBody(TeaModel):
    def __init__(self, record_id=None, request_id=None):
        self.record_id = record_id  # type: long
        self.request_id = request_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DeleteZoneRecordResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.record_id is not None:
            result['RecordId'] = self.record_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RecordId') is not None:
            self.record_id = m.get('RecordId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteZoneRecordResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: DeleteZoneRecordResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(DeleteZoneRecordResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteZoneRecordResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeChangeLogsRequest(TeaModel):
    def __init__(self, end_timestamp=None, entity_type=None, keyword=None, lang=None, page_number=None,
                 page_size=None, start_timestamp=None, user_client_ip=None, zone_id=None):
        self.end_timestamp = end_timestamp  # type: long
        self.entity_type = entity_type  # type: str
        self.keyword = keyword  # type: str
        self.lang = lang  # type: str
        self.page_number = page_number  # type: int
        self.page_size = page_size  # type: int
        self.start_timestamp = start_timestamp  # type: long
        self.user_client_ip = user_client_ip  # type: str
        self.zone_id = zone_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeChangeLogsRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_timestamp is not None:
            result['EndTimestamp'] = self.end_timestamp
        if self.entity_type is not None:
            result['EntityType'] = self.entity_type
        if self.keyword is not None:
            result['Keyword'] = self.keyword
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.start_timestamp is not None:
            result['StartTimestamp'] = self.start_timestamp
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('EndTimestamp') is not None:
            self.end_timestamp = m.get('EndTimestamp')
        if m.get('EntityType') is not None:
            self.entity_type = m.get('EntityType')
        if m.get('Keyword') is not None:
            self.keyword = m.get('Keyword')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('StartTimestamp') is not None:
            self.start_timestamp = m.get('StartTimestamp')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        return self


class DescribeChangeLogsResponseBodyChangeLogsChangeLog(TeaModel):
    def __init__(self, content=None, creator_id=None, creator_sub_type=None, creator_type=None, entity_id=None,
                 entity_name=None, id=None, oper_action=None, oper_ip=None, oper_object=None, oper_time=None,
                 oper_timestamp=None):
        self.content = content  # type: str
        self.creator_id = creator_id  # type: str
        self.creator_sub_type = creator_sub_type  # type: str
        self.creator_type = creator_type  # type: str
        self.entity_id = entity_id  # type: str
        self.entity_name = entity_name  # type: str
        self.id = id  # type: long
        self.oper_action = oper_action  # type: str
        self.oper_ip = oper_ip  # type: str
        self.oper_object = oper_object  # type: str
        self.oper_time = oper_time  # type: str
        self.oper_timestamp = oper_timestamp  # type: long

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeChangeLogsResponseBodyChangeLogsChangeLog, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.content is not None:
            result['Content'] = self.content
        if self.creator_id is not None:
            result['CreatorId'] = self.creator_id
        if self.creator_sub_type is not None:
            result['CreatorSubType'] = self.creator_sub_type
        if self.creator_type is not None:
            result['CreatorType'] = self.creator_type
        if self.entity_id is not None:
            result['EntityId'] = self.entity_id
        if self.entity_name is not None:
            result['EntityName'] = self.entity_name
        if self.id is not None:
            result['Id'] = self.id
        if self.oper_action is not None:
            result['OperAction'] = self.oper_action
        if self.oper_ip is not None:
            result['OperIp'] = self.oper_ip
        if self.oper_object is not None:
            result['OperObject'] = self.oper_object
        if self.oper_time is not None:
            result['OperTime'] = self.oper_time
        if self.oper_timestamp is not None:
            result['OperTimestamp'] = self.oper_timestamp
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Content') is not None:
            self.content = m.get('Content')
        if m.get('CreatorId') is not None:
            self.creator_id = m.get('CreatorId')
        if m.get('CreatorSubType') is not None:
            self.creator_sub_type = m.get('CreatorSubType')
        if m.get('CreatorType') is not None:
            self.creator_type = m.get('CreatorType')
        if m.get('EntityId') is not None:
            self.entity_id = m.get('EntityId')
        if m.get('EntityName') is not None:
            self.entity_name = m.get('EntityName')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('OperAction') is not None:
            self.oper_action = m.get('OperAction')
        if m.get('OperIp') is not None:
            self.oper_ip = m.get('OperIp')
        if m.get('OperObject') is not None:
            self.oper_object = m.get('OperObject')
        if m.get('OperTime') is not None:
            self.oper_time = m.get('OperTime')
        if m.get('OperTimestamp') is not None:
            self.oper_timestamp = m.get('OperTimestamp')
        return self


class DescribeChangeLogsResponseBodyChangeLogs(TeaModel):
    def __init__(self, change_log=None):
        self.change_log = change_log  # type: list[DescribeChangeLogsResponseBodyChangeLogsChangeLog]

    def validate(self):
        if self.change_log:
            for k in self.change_log:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(DescribeChangeLogsResponseBodyChangeLogs, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        result['ChangeLog'] = []
        if self.change_log is not None:
            for k in self.change_log:
                result['ChangeLog'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        self.change_log = []
        if m.get('ChangeLog') is not None:
            for k in m.get('ChangeLog'):
                temp_model = DescribeChangeLogsResponseBodyChangeLogsChangeLog()
                self.change_log.append(temp_model.from_map(k))
        return self


class DescribeChangeLogsResponseBody(TeaModel):
    def __init__(self, change_logs=None, page_number=None, page_size=None, request_id=None, total_items=None,
                 total_pages=None):
        self.change_logs = change_logs  # type: DescribeChangeLogsResponseBodyChangeLogs
        self.page_number = page_number  # type: int
        self.page_size = page_size  # type: int
        self.request_id = request_id  # type: str
        self.total_items = total_items  # type: int
        self.total_pages = total_pages  # type: int

    def validate(self):
        if self.change_logs:
            self.change_logs.validate()

    def to_map(self):
        _map = super(DescribeChangeLogsResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.change_logs is not None:
            result['ChangeLogs'] = self.change_logs.to_map()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_items is not None:
            result['TotalItems'] = self.total_items
        if self.total_pages is not None:
            result['TotalPages'] = self.total_pages
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('ChangeLogs') is not None:
            temp_model = DescribeChangeLogsResponseBodyChangeLogs()
            self.change_logs = temp_model.from_map(m['ChangeLogs'])
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalItems') is not None:
            self.total_items = m.get('TotalItems')
        if m.get('TotalPages') is not None:
            self.total_pages = m.get('TotalPages')
        return self


class DescribeChangeLogsResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: DescribeChangeLogsResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(DescribeChangeLogsResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeChangeLogsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeRegionsRequest(TeaModel):
    def __init__(self, accept_language=None, authorized_user_id=None, lang=None, scene=None, user_client_ip=None,
                 vpc_type=None):
        self.accept_language = accept_language  # type: str
        self.authorized_user_id = authorized_user_id  # type: long
        self.lang = lang  # type: str
        self.scene = scene  # type: str
        self.user_client_ip = user_client_ip  # type: str
        self.vpc_type = vpc_type  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeRegionsRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.accept_language is not None:
            result['AcceptLanguage'] = self.accept_language
        if self.authorized_user_id is not None:
            result['AuthorizedUserId'] = self.authorized_user_id
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.scene is not None:
            result['Scene'] = self.scene
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.vpc_type is not None:
            result['VpcType'] = self.vpc_type
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('AcceptLanguage') is not None:
            self.accept_language = m.get('AcceptLanguage')
        if m.get('AuthorizedUserId') is not None:
            self.authorized_user_id = m.get('AuthorizedUserId')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('Scene') is not None:
            self.scene = m.get('Scene')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('VpcType') is not None:
            self.vpc_type = m.get('VpcType')
        return self


class DescribeRegionsResponseBodyRegionsRegion(TeaModel):
    def __init__(self, local_name=None, region_endpoint=None, region_id=None, region_name=None):
        self.local_name = local_name  # type: str
        self.region_endpoint = region_endpoint  # type: str
        self.region_id = region_id  # type: str
        self.region_name = region_name  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeRegionsResponseBodyRegionsRegion, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.local_name is not None:
            result['LocalName'] = self.local_name
        if self.region_endpoint is not None:
            result['RegionEndpoint'] = self.region_endpoint
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.region_name is not None:
            result['RegionName'] = self.region_name
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('LocalName') is not None:
            self.local_name = m.get('LocalName')
        if m.get('RegionEndpoint') is not None:
            self.region_endpoint = m.get('RegionEndpoint')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('RegionName') is not None:
            self.region_name = m.get('RegionName')
        return self


class DescribeRegionsResponseBodyRegions(TeaModel):
    def __init__(self, region=None):
        self.region = region  # type: list[DescribeRegionsResponseBodyRegionsRegion]

    def validate(self):
        if self.region:
            for k in self.region:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(DescribeRegionsResponseBodyRegions, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Region'] = []
        if self.region is not None:
            for k in self.region:
                result['Region'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        self.region = []
        if m.get('Region') is not None:
            for k in m.get('Region'):
                temp_model = DescribeRegionsResponseBodyRegionsRegion()
                self.region.append(temp_model.from_map(k))
        return self


class DescribeRegionsResponseBody(TeaModel):
    def __init__(self, regions=None, request_id=None):
        self.regions = regions  # type: DescribeRegionsResponseBodyRegions
        self.request_id = request_id  # type: str

    def validate(self):
        if self.regions:
            self.regions.validate()

    def to_map(self):
        _map = super(DescribeRegionsResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.regions is not None:
            result['Regions'] = self.regions.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Regions') is not None:
            temp_model = DescribeRegionsResponseBodyRegions()
            self.regions = temp_model.from_map(m['Regions'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DescribeRegionsResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: DescribeRegionsResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(DescribeRegionsResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeRegionsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeRequestGraphRequest(TeaModel):
    def __init__(self, biz_id=None, biz_type=None, end_timestamp=None, lang=None, start_timestamp=None,
                 user_client_ip=None, vpc_id=None, zone_id=None):
        self.biz_id = biz_id  # type: str
        self.biz_type = biz_type  # type: str
        self.end_timestamp = end_timestamp  # type: long
        self.lang = lang  # type: str
        self.start_timestamp = start_timestamp  # type: long
        self.user_client_ip = user_client_ip  # type: str
        # VPC ID
        self.vpc_id = vpc_id  # type: str
        # zone ID
        self.zone_id = zone_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeRequestGraphRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.biz_id is not None:
            result['BizId'] = self.biz_id
        if self.biz_type is not None:
            result['BizType'] = self.biz_type
        if self.end_timestamp is not None:
            result['EndTimestamp'] = self.end_timestamp
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.start_timestamp is not None:
            result['StartTimestamp'] = self.start_timestamp
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('BizId') is not None:
            self.biz_id = m.get('BizId')
        if m.get('BizType') is not None:
            self.biz_type = m.get('BizType')
        if m.get('EndTimestamp') is not None:
            self.end_timestamp = m.get('EndTimestamp')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('StartTimestamp') is not None:
            self.start_timestamp = m.get('StartTimestamp')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        return self


class DescribeRequestGraphResponseBodyRequestDetailsZoneRequestTop(TeaModel):
    def __init__(self, request_count=None, time=None, timestamp=None):
        self.request_count = request_count  # type: long
        self.time = time  # type: str
        self.timestamp = timestamp  # type: long

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeRequestGraphResponseBodyRequestDetailsZoneRequestTop, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_count is not None:
            result['RequestCount'] = self.request_count
        if self.time is not None:
            result['Time'] = self.time
        if self.timestamp is not None:
            result['Timestamp'] = self.timestamp
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestCount') is not None:
            self.request_count = m.get('RequestCount')
        if m.get('Time') is not None:
            self.time = m.get('Time')
        if m.get('Timestamp') is not None:
            self.timestamp = m.get('Timestamp')
        return self


class DescribeRequestGraphResponseBodyRequestDetails(TeaModel):
    def __init__(self, zone_request_top=None):
        self.zone_request_top = zone_request_top  # type: list[DescribeRequestGraphResponseBodyRequestDetailsZoneRequestTop]

    def validate(self):
        if self.zone_request_top:
            for k in self.zone_request_top:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(DescribeRequestGraphResponseBodyRequestDetails, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        result['ZoneRequestTop'] = []
        if self.zone_request_top is not None:
            for k in self.zone_request_top:
                result['ZoneRequestTop'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        self.zone_request_top = []
        if m.get('ZoneRequestTop') is not None:
            for k in m.get('ZoneRequestTop'):
                temp_model = DescribeRequestGraphResponseBodyRequestDetailsZoneRequestTop()
                self.zone_request_top.append(temp_model.from_map(k))
        return self


class DescribeRequestGraphResponseBody(TeaModel):
    def __init__(self, request_details=None, request_id=None):
        self.request_details = request_details  # type: DescribeRequestGraphResponseBodyRequestDetails
        self.request_id = request_id  # type: str

    def validate(self):
        if self.request_details:
            self.request_details.validate()

    def to_map(self):
        _map = super(DescribeRequestGraphResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_details is not None:
            result['RequestDetails'] = self.request_details.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestDetails') is not None:
            temp_model = DescribeRequestGraphResponseBodyRequestDetails()
            self.request_details = temp_model.from_map(m['RequestDetails'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DescribeRequestGraphResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: DescribeRequestGraphResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(DescribeRequestGraphResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeRequestGraphResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeResolverAvailableZonesRequest(TeaModel):
    def __init__(self, az_id=None, lang=None, resolver_region_id=None):
        self.az_id = az_id  # type: str
        self.lang = lang  # type: str
        self.resolver_region_id = resolver_region_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeResolverAvailableZonesRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.az_id is not None:
            result['AzId'] = self.az_id
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.resolver_region_id is not None:
            result['ResolverRegionId'] = self.resolver_region_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('AzId') is not None:
            self.az_id = m.get('AzId')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('ResolverRegionId') is not None:
            self.resolver_region_id = m.get('ResolverRegionId')
        return self


class DescribeResolverAvailableZonesResponseBodyAvailableZones(TeaModel):
    def __init__(self, az_id=None, status=None):
        self.az_id = az_id  # type: str
        self.status = status  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeResolverAvailableZonesResponseBodyAvailableZones, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.az_id is not None:
            result['AzId'] = self.az_id
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('AzId') is not None:
            self.az_id = m.get('AzId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class DescribeResolverAvailableZonesResponseBody(TeaModel):
    def __init__(self, available_zones=None, request_id=None):
        self.available_zones = available_zones  # type: list[DescribeResolverAvailableZonesResponseBodyAvailableZones]
        self.request_id = request_id  # type: str

    def validate(self):
        if self.available_zones:
            for k in self.available_zones:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(DescribeResolverAvailableZonesResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        result['AvailableZones'] = []
        if self.available_zones is not None:
            for k in self.available_zones:
                result['AvailableZones'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        self.available_zones = []
        if m.get('AvailableZones') is not None:
            for k in m.get('AvailableZones'):
                temp_model = DescribeResolverAvailableZonesResponseBodyAvailableZones()
                self.available_zones.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DescribeResolverAvailableZonesResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: DescribeResolverAvailableZonesResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(DescribeResolverAvailableZonesResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeResolverAvailableZonesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeResolverEndpointRequest(TeaModel):
    def __init__(self, endpoint_id=None, lang=None):
        self.endpoint_id = endpoint_id  # type: str
        self.lang = lang  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeResolverEndpointRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.endpoint_id is not None:
            result['EndpointId'] = self.endpoint_id
        if self.lang is not None:
            result['Lang'] = self.lang
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('EndpointId') is not None:
            self.endpoint_id = m.get('EndpointId')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        return self


class DescribeResolverEndpointResponseBodyIpConfigs(TeaModel):
    def __init__(self, az_id=None, cidr_block=None, ip=None, v_switch_id=None):
        self.az_id = az_id  # type: str
        self.cidr_block = cidr_block  # type: str
        self.ip = ip  # type: str
        self.v_switch_id = v_switch_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeResolverEndpointResponseBodyIpConfigs, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.az_id is not None:
            result['AzId'] = self.az_id
        if self.cidr_block is not None:
            result['CidrBlock'] = self.cidr_block
        if self.ip is not None:
            result['Ip'] = self.ip
        if self.v_switch_id is not None:
            result['VSwitchId'] = self.v_switch_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('AzId') is not None:
            self.az_id = m.get('AzId')
        if m.get('CidrBlock') is not None:
            self.cidr_block = m.get('CidrBlock')
        if m.get('Ip') is not None:
            self.ip = m.get('Ip')
        if m.get('VSwitchId') is not None:
            self.v_switch_id = m.get('VSwitchId')
        return self


class DescribeResolverEndpointResponseBody(TeaModel):
    def __init__(self, create_time=None, create_timestamp=None, id=None, ip_configs=None, name=None, request_id=None,
                 security_group_id=None, status=None, update_time=None, update_timestamp=None, vpc_id=None, vpc_name=None,
                 vpc_region_id=None, vpc_region_name=None):
        self.create_time = create_time  # type: str
        self.create_timestamp = create_timestamp  # type: long
        self.id = id  # type: str
        self.ip_configs = ip_configs  # type: list[DescribeResolverEndpointResponseBodyIpConfigs]
        self.name = name  # type: str
        self.request_id = request_id  # type: str
        self.security_group_id = security_group_id  # type: str
        self.status = status  # type: str
        self.update_time = update_time  # type: str
        self.update_timestamp = update_timestamp  # type: long
        self.vpc_id = vpc_id  # type: str
        self.vpc_name = vpc_name  # type: str
        self.vpc_region_id = vpc_region_id  # type: str
        self.vpc_region_name = vpc_region_name  # type: str

    def validate(self):
        if self.ip_configs:
            for k in self.ip_configs:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(DescribeResolverEndpointResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        if self.id is not None:
            result['Id'] = self.id
        result['IpConfigs'] = []
        if self.ip_configs is not None:
            for k in self.ip_configs:
                result['IpConfigs'].append(k.to_map() if k else None)
        if self.name is not None:
            result['Name'] = self.name
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.security_group_id is not None:
            result['SecurityGroupId'] = self.security_group_id
        if self.status is not None:
            result['Status'] = self.status
        if self.update_time is not None:
            result['UpdateTime'] = self.update_time
        if self.update_timestamp is not None:
            result['UpdateTimestamp'] = self.update_timestamp
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.vpc_name is not None:
            result['VpcName'] = self.vpc_name
        if self.vpc_region_id is not None:
            result['VpcRegionId'] = self.vpc_region_id
        if self.vpc_region_name is not None:
            result['VpcRegionName'] = self.vpc_region_name
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        self.ip_configs = []
        if m.get('IpConfigs') is not None:
            for k in m.get('IpConfigs'):
                temp_model = DescribeResolverEndpointResponseBodyIpConfigs()
                self.ip_configs.append(temp_model.from_map(k))
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('SecurityGroupId') is not None:
            self.security_group_id = m.get('SecurityGroupId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('UpdateTime') is not None:
            self.update_time = m.get('UpdateTime')
        if m.get('UpdateTimestamp') is not None:
            self.update_timestamp = m.get('UpdateTimestamp')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('VpcName') is not None:
            self.vpc_name = m.get('VpcName')
        if m.get('VpcRegionId') is not None:
            self.vpc_region_id = m.get('VpcRegionId')
        if m.get('VpcRegionName') is not None:
            self.vpc_region_name = m.get('VpcRegionName')
        return self


class DescribeResolverEndpointResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: DescribeResolverEndpointResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(DescribeResolverEndpointResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeResolverEndpointResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeResolverEndpointsRequest(TeaModel):
    def __init__(self, keyword=None, lang=None, page_number=None, page_size=None, status=None):
        self.keyword = keyword  # type: str
        self.lang = lang  # type: str
        self.page_number = page_number  # type: int
        self.page_size = page_size  # type: int
        self.status = status  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeResolverEndpointsRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.keyword is not None:
            result['Keyword'] = self.keyword
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Keyword') is not None:
            self.keyword = m.get('Keyword')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class DescribeResolverEndpointsResponseBodyEndpointsIpConfigs(TeaModel):
    def __init__(self, az_id=None, cidr_block=None, ip=None, v_switch_id=None):
        self.az_id = az_id  # type: str
        self.cidr_block = cidr_block  # type: str
        self.ip = ip  # type: str
        self.v_switch_id = v_switch_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeResolverEndpointsResponseBodyEndpointsIpConfigs, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.az_id is not None:
            result['AzId'] = self.az_id
        if self.cidr_block is not None:
            result['CidrBlock'] = self.cidr_block
        if self.ip is not None:
            result['Ip'] = self.ip
        if self.v_switch_id is not None:
            result['VSwitchId'] = self.v_switch_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('AzId') is not None:
            self.az_id = m.get('AzId')
        if m.get('CidrBlock') is not None:
            self.cidr_block = m.get('CidrBlock')
        if m.get('Ip') is not None:
            self.ip = m.get('Ip')
        if m.get('VSwitchId') is not None:
            self.v_switch_id = m.get('VSwitchId')
        return self


class DescribeResolverEndpointsResponseBodyEndpoints(TeaModel):
    def __init__(self, create_time=None, create_timestamp=None, id=None, ip_configs=None, name=None,
                 security_group_id=None, status=None, update_time=None, update_timestamp=None, vpc_id=None, vpc_name=None,
                 vpc_region_id=None, vpc_region_name=None):
        self.create_time = create_time  # type: str
        self.create_timestamp = create_timestamp  # type: long
        self.id = id  # type: str
        self.ip_configs = ip_configs  # type: list[DescribeResolverEndpointsResponseBodyEndpointsIpConfigs]
        self.name = name  # type: str
        self.security_group_id = security_group_id  # type: str
        self.status = status  # type: str
        self.update_time = update_time  # type: str
        self.update_timestamp = update_timestamp  # type: long
        self.vpc_id = vpc_id  # type: str
        self.vpc_name = vpc_name  # type: str
        self.vpc_region_id = vpc_region_id  # type: str
        self.vpc_region_name = vpc_region_name  # type: str

    def validate(self):
        if self.ip_configs:
            for k in self.ip_configs:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(DescribeResolverEndpointsResponseBodyEndpoints, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        if self.id is not None:
            result['Id'] = self.id
        result['IpConfigs'] = []
        if self.ip_configs is not None:
            for k in self.ip_configs:
                result['IpConfigs'].append(k.to_map() if k else None)
        if self.name is not None:
            result['Name'] = self.name
        if self.security_group_id is not None:
            result['SecurityGroupId'] = self.security_group_id
        if self.status is not None:
            result['Status'] = self.status
        if self.update_time is not None:
            result['UpdateTime'] = self.update_time
        if self.update_timestamp is not None:
            result['UpdateTimestamp'] = self.update_timestamp
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.vpc_name is not None:
            result['VpcName'] = self.vpc_name
        if self.vpc_region_id is not None:
            result['VpcRegionId'] = self.vpc_region_id
        if self.vpc_region_name is not None:
            result['VpcRegionName'] = self.vpc_region_name
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        self.ip_configs = []
        if m.get('IpConfigs') is not None:
            for k in m.get('IpConfigs'):
                temp_model = DescribeResolverEndpointsResponseBodyEndpointsIpConfigs()
                self.ip_configs.append(temp_model.from_map(k))
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('SecurityGroupId') is not None:
            self.security_group_id = m.get('SecurityGroupId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('UpdateTime') is not None:
            self.update_time = m.get('UpdateTime')
        if m.get('UpdateTimestamp') is not None:
            self.update_timestamp = m.get('UpdateTimestamp')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('VpcName') is not None:
            self.vpc_name = m.get('VpcName')
        if m.get('VpcRegionId') is not None:
            self.vpc_region_id = m.get('VpcRegionId')
        if m.get('VpcRegionName') is not None:
            self.vpc_region_name = m.get('VpcRegionName')
        return self


class DescribeResolverEndpointsResponseBody(TeaModel):
    def __init__(self, endpoints=None, page_number=None, page_size=None, request_id=None, total_items=None,
                 total_pages=None):
        self.endpoints = endpoints  # type: list[DescribeResolverEndpointsResponseBodyEndpoints]
        self.page_number = page_number  # type: int
        self.page_size = page_size  # type: int
        self.request_id = request_id  # type: str
        self.total_items = total_items  # type: int
        self.total_pages = total_pages  # type: int

    def validate(self):
        if self.endpoints:
            for k in self.endpoints:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(DescribeResolverEndpointsResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Endpoints'] = []
        if self.endpoints is not None:
            for k in self.endpoints:
                result['Endpoints'].append(k.to_map() if k else None)
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_items is not None:
            result['TotalItems'] = self.total_items
        if self.total_pages is not None:
            result['TotalPages'] = self.total_pages
        return result

    def from_map(self, m=None):
        m = m or dict()
        self.endpoints = []
        if m.get('Endpoints') is not None:
            for k in m.get('Endpoints'):
                temp_model = DescribeResolverEndpointsResponseBodyEndpoints()
                self.endpoints.append(temp_model.from_map(k))
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalItems') is not None:
            self.total_items = m.get('TotalItems')
        if m.get('TotalPages') is not None:
            self.total_pages = m.get('TotalPages')
        return self


class DescribeResolverEndpointsResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: DescribeResolverEndpointsResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(DescribeResolverEndpointsResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeResolverEndpointsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeResolverRuleRequest(TeaModel):
    def __init__(self, lang=None, rule_id=None):
        self.lang = lang  # type: str
        self.rule_id = rule_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeResolverRuleRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        return self


class DescribeResolverRuleResponseBodyBindVpcs(TeaModel):
    def __init__(self, region_id=None, region_name=None, vpc_id=None, vpc_name=None, vpc_type=None, vpc_user_id=None):
        self.region_id = region_id  # type: str
        self.region_name = region_name  # type: str
        # Vpc ID
        self.vpc_id = vpc_id  # type: str
        self.vpc_name = vpc_name  # type: str
        self.vpc_type = vpc_type  # type: str
        self.vpc_user_id = vpc_user_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeResolverRuleResponseBodyBindVpcs, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.region_name is not None:
            result['RegionName'] = self.region_name
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.vpc_name is not None:
            result['VpcName'] = self.vpc_name
        if self.vpc_type is not None:
            result['VpcType'] = self.vpc_type
        if self.vpc_user_id is not None:
            result['VpcUserId'] = self.vpc_user_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('RegionName') is not None:
            self.region_name = m.get('RegionName')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('VpcName') is not None:
            self.vpc_name = m.get('VpcName')
        if m.get('VpcType') is not None:
            self.vpc_type = m.get('VpcType')
        if m.get('VpcUserId') is not None:
            self.vpc_user_id = m.get('VpcUserId')
        return self


class DescribeResolverRuleResponseBodyForwardIps(TeaModel):
    def __init__(self, ip=None, port=None):
        self.ip = ip  # type: str
        self.port = port  # type: int

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeResolverRuleResponseBodyForwardIps, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.ip is not None:
            result['Ip'] = self.ip
        if self.port is not None:
            result['Port'] = self.port
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Ip') is not None:
            self.ip = m.get('Ip')
        if m.get('Port') is not None:
            self.port = m.get('Port')
        return self


class DescribeResolverRuleResponseBody(TeaModel):
    def __init__(self, bind_vpcs=None, create_time=None, create_timestamp=None, endpoint_id=None,
                 endpoint_name=None, forward_ips=None, id=None, name=None, request_id=None, type=None, update_time=None,
                 update_timestamp=None, zone_name=None):
        self.bind_vpcs = bind_vpcs  # type: list[DescribeResolverRuleResponseBodyBindVpcs]
        self.create_time = create_time  # type: str
        self.create_timestamp = create_timestamp  # type: long
        self.endpoint_id = endpoint_id  # type: str
        self.endpoint_name = endpoint_name  # type: str
        self.forward_ips = forward_ips  # type: list[DescribeResolverRuleResponseBodyForwardIps]
        self.id = id  # type: str
        self.name = name  # type: str
        self.request_id = request_id  # type: str
        self.type = type  # type: str
        self.update_time = update_time  # type: str
        self.update_timestamp = update_timestamp  # type: long
        self.zone_name = zone_name  # type: str

    def validate(self):
        if self.bind_vpcs:
            for k in self.bind_vpcs:
                if k:
                    k.validate()
        if self.forward_ips:
            for k in self.forward_ips:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(DescribeResolverRuleResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        result['BindVpcs'] = []
        if self.bind_vpcs is not None:
            for k in self.bind_vpcs:
                result['BindVpcs'].append(k.to_map() if k else None)
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        if self.endpoint_id is not None:
            result['EndpointId'] = self.endpoint_id
        if self.endpoint_name is not None:
            result['EndpointName'] = self.endpoint_name
        result['ForwardIps'] = []
        if self.forward_ips is not None:
            for k in self.forward_ips:
                result['ForwardIps'].append(k.to_map() if k else None)
        if self.id is not None:
            result['Id'] = self.id
        if self.name is not None:
            result['Name'] = self.name
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.type is not None:
            result['Type'] = self.type
        if self.update_time is not None:
            result['UpdateTime'] = self.update_time
        if self.update_timestamp is not None:
            result['UpdateTimestamp'] = self.update_timestamp
        if self.zone_name is not None:
            result['ZoneName'] = self.zone_name
        return result

    def from_map(self, m=None):
        m = m or dict()
        self.bind_vpcs = []
        if m.get('BindVpcs') is not None:
            for k in m.get('BindVpcs'):
                temp_model = DescribeResolverRuleResponseBodyBindVpcs()
                self.bind_vpcs.append(temp_model.from_map(k))
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        if m.get('EndpointId') is not None:
            self.endpoint_id = m.get('EndpointId')
        if m.get('EndpointName') is not None:
            self.endpoint_name = m.get('EndpointName')
        self.forward_ips = []
        if m.get('ForwardIps') is not None:
            for k in m.get('ForwardIps'):
                temp_model = DescribeResolverRuleResponseBodyForwardIps()
                self.forward_ips.append(temp_model.from_map(k))
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('UpdateTime') is not None:
            self.update_time = m.get('UpdateTime')
        if m.get('UpdateTimestamp') is not None:
            self.update_timestamp = m.get('UpdateTimestamp')
        if m.get('ZoneName') is not None:
            self.zone_name = m.get('ZoneName')
        return self


class DescribeResolverRuleResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: DescribeResolverRuleResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(DescribeResolverRuleResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeResolverRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeResolverRulesRequest(TeaModel):
    def __init__(self, endpoint_id=None, keyword=None, lang=None, need_detail_attributes=None, page_number=None,
                 page_size=None):
        self.endpoint_id = endpoint_id  # type: str
        self.keyword = keyword  # type: str
        self.lang = lang  # type: str
        self.need_detail_attributes = need_detail_attributes  # type: bool
        self.page_number = page_number  # type: int
        self.page_size = page_size  # type: int

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeResolverRulesRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.endpoint_id is not None:
            result['EndpointId'] = self.endpoint_id
        if self.keyword is not None:
            result['Keyword'] = self.keyword
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.need_detail_attributes is not None:
            result['NeedDetailAttributes'] = self.need_detail_attributes
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('EndpointId') is not None:
            self.endpoint_id = m.get('EndpointId')
        if m.get('Keyword') is not None:
            self.keyword = m.get('Keyword')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('NeedDetailAttributes') is not None:
            self.need_detail_attributes = m.get('NeedDetailAttributes')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeResolverRulesResponseBodyRulesBindVpcs(TeaModel):
    def __init__(self, region_id=None, region_name=None, vpc_id=None, vpc_name=None, vpc_type=None, vpc_user_id=None):
        self.region_id = region_id  # type: str
        self.region_name = region_name  # type: str
        # VPC ID
        self.vpc_id = vpc_id  # type: str
        self.vpc_name = vpc_name  # type: str
        self.vpc_type = vpc_type  # type: str
        self.vpc_user_id = vpc_user_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeResolverRulesResponseBodyRulesBindVpcs, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.region_name is not None:
            result['RegionName'] = self.region_name
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.vpc_name is not None:
            result['VpcName'] = self.vpc_name
        if self.vpc_type is not None:
            result['VpcType'] = self.vpc_type
        if self.vpc_user_id is not None:
            result['VpcUserId'] = self.vpc_user_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('RegionName') is not None:
            self.region_name = m.get('RegionName')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('VpcName') is not None:
            self.vpc_name = m.get('VpcName')
        if m.get('VpcType') is not None:
            self.vpc_type = m.get('VpcType')
        if m.get('VpcUserId') is not None:
            self.vpc_user_id = m.get('VpcUserId')
        return self


class DescribeResolverRulesResponseBodyRulesForwardIps(TeaModel):
    def __init__(self, ip=None, port=None):
        self.ip = ip  # type: str
        self.port = port  # type: int

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeResolverRulesResponseBodyRulesForwardIps, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.ip is not None:
            result['Ip'] = self.ip
        if self.port is not None:
            result['Port'] = self.port
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Ip') is not None:
            self.ip = m.get('Ip')
        if m.get('Port') is not None:
            self.port = m.get('Port')
        return self


class DescribeResolverRulesResponseBodyRules(TeaModel):
    def __init__(self, bind_vpcs=None, create_time=None, create_timestamp=None, endpoint_id=None,
                 endpoint_name=None, forward_ips=None, id=None, name=None, type=None, update_time=None, update_timestamp=None,
                 zone_name=None):
        self.bind_vpcs = bind_vpcs  # type: list[DescribeResolverRulesResponseBodyRulesBindVpcs]
        self.create_time = create_time  # type: str
        self.create_timestamp = create_timestamp  # type: long
        self.endpoint_id = endpoint_id  # type: str
        self.endpoint_name = endpoint_name  # type: str
        self.forward_ips = forward_ips  # type: list[DescribeResolverRulesResponseBodyRulesForwardIps]
        self.id = id  # type: str
        self.name = name  # type: str
        self.type = type  # type: str
        self.update_time = update_time  # type: str
        self.update_timestamp = update_timestamp  # type: long
        self.zone_name = zone_name  # type: str

    def validate(self):
        if self.bind_vpcs:
            for k in self.bind_vpcs:
                if k:
                    k.validate()
        if self.forward_ips:
            for k in self.forward_ips:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(DescribeResolverRulesResponseBodyRules, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        result['BindVpcs'] = []
        if self.bind_vpcs is not None:
            for k in self.bind_vpcs:
                result['BindVpcs'].append(k.to_map() if k else None)
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        if self.endpoint_id is not None:
            result['EndpointId'] = self.endpoint_id
        if self.endpoint_name is not None:
            result['EndpointName'] = self.endpoint_name
        result['ForwardIps'] = []
        if self.forward_ips is not None:
            for k in self.forward_ips:
                result['ForwardIps'].append(k.to_map() if k else None)
        if self.id is not None:
            result['Id'] = self.id
        if self.name is not None:
            result['Name'] = self.name
        if self.type is not None:
            result['Type'] = self.type
        if self.update_time is not None:
            result['UpdateTime'] = self.update_time
        if self.update_timestamp is not None:
            result['UpdateTimestamp'] = self.update_timestamp
        if self.zone_name is not None:
            result['ZoneName'] = self.zone_name
        return result

    def from_map(self, m=None):
        m = m or dict()
        self.bind_vpcs = []
        if m.get('BindVpcs') is not None:
            for k in m.get('BindVpcs'):
                temp_model = DescribeResolverRulesResponseBodyRulesBindVpcs()
                self.bind_vpcs.append(temp_model.from_map(k))
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        if m.get('EndpointId') is not None:
            self.endpoint_id = m.get('EndpointId')
        if m.get('EndpointName') is not None:
            self.endpoint_name = m.get('EndpointName')
        self.forward_ips = []
        if m.get('ForwardIps') is not None:
            for k in m.get('ForwardIps'):
                temp_model = DescribeResolverRulesResponseBodyRulesForwardIps()
                self.forward_ips.append(temp_model.from_map(k))
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('UpdateTime') is not None:
            self.update_time = m.get('UpdateTime')
        if m.get('UpdateTimestamp') is not None:
            self.update_timestamp = m.get('UpdateTimestamp')
        if m.get('ZoneName') is not None:
            self.zone_name = m.get('ZoneName')
        return self


class DescribeResolverRulesResponseBody(TeaModel):
    def __init__(self, page_number=None, page_size=None, request_id=None, rules=None, total_items=None,
                 total_pages=None):
        self.page_number = page_number  # type: int
        self.page_size = page_size  # type: int
        self.request_id = request_id  # type: str
        self.rules = rules  # type: list[DescribeResolverRulesResponseBodyRules]
        self.total_items = total_items  # type: int
        self.total_pages = total_pages  # type: int

    def validate(self):
        if self.rules:
            for k in self.rules:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(DescribeResolverRulesResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Rules'] = []
        if self.rules is not None:
            for k in self.rules:
                result['Rules'].append(k.to_map() if k else None)
        if self.total_items is not None:
            result['TotalItems'] = self.total_items
        if self.total_pages is not None:
            result['TotalPages'] = self.total_pages
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.rules = []
        if m.get('Rules') is not None:
            for k in m.get('Rules'):
                temp_model = DescribeResolverRulesResponseBodyRules()
                self.rules.append(temp_model.from_map(k))
        if m.get('TotalItems') is not None:
            self.total_items = m.get('TotalItems')
        if m.get('TotalPages') is not None:
            self.total_pages = m.get('TotalPages')
        return self


class DescribeResolverRulesResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: DescribeResolverRulesResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(DescribeResolverRulesResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeResolverRulesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeStatisticSummaryRequest(TeaModel):
    def __init__(self, lang=None, user_client_ip=None):
        self.lang = lang  # type: str
        self.user_client_ip = user_client_ip  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeStatisticSummaryRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        return self


class DescribeStatisticSummaryResponseBodyVpcRequestTopsVpcRequestTop(TeaModel):
    def __init__(self, region_id=None, region_name=None, request_count=None, tunnel_id=None, vpc_id=None,
                 vpc_type=None):
        self.region_id = region_id  # type: str
        self.region_name = region_name  # type: str
        self.request_count = request_count  # type: long
        self.tunnel_id = tunnel_id  # type: str
        # VPC ID
        self.vpc_id = vpc_id  # type: str
        self.vpc_type = vpc_type  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeStatisticSummaryResponseBodyVpcRequestTopsVpcRequestTop, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.region_name is not None:
            result['RegionName'] = self.region_name
        if self.request_count is not None:
            result['RequestCount'] = self.request_count
        if self.tunnel_id is not None:
            result['TunnelId'] = self.tunnel_id
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.vpc_type is not None:
            result['VpcType'] = self.vpc_type
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('RegionName') is not None:
            self.region_name = m.get('RegionName')
        if m.get('RequestCount') is not None:
            self.request_count = m.get('RequestCount')
        if m.get('TunnelId') is not None:
            self.tunnel_id = m.get('TunnelId')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('VpcType') is not None:
            self.vpc_type = m.get('VpcType')
        return self


class DescribeStatisticSummaryResponseBodyVpcRequestTops(TeaModel):
    def __init__(self, vpc_request_top=None):
        self.vpc_request_top = vpc_request_top  # type: list[DescribeStatisticSummaryResponseBodyVpcRequestTopsVpcRequestTop]

    def validate(self):
        if self.vpc_request_top:
            for k in self.vpc_request_top:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(DescribeStatisticSummaryResponseBodyVpcRequestTops, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        result['VpcRequestTop'] = []
        if self.vpc_request_top is not None:
            for k in self.vpc_request_top:
                result['VpcRequestTop'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        self.vpc_request_top = []
        if m.get('VpcRequestTop') is not None:
            for k in m.get('VpcRequestTop'):
                temp_model = DescribeStatisticSummaryResponseBodyVpcRequestTopsVpcRequestTop()
                self.vpc_request_top.append(temp_model.from_map(k))
        return self


class DescribeStatisticSummaryResponseBodyZoneRequestTopsZoneRequestTop(TeaModel):
    def __init__(self, biz_type=None, request_count=None, zone_name=None):
        self.biz_type = biz_type  # type: str
        self.request_count = request_count  # type: long
        self.zone_name = zone_name  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeStatisticSummaryResponseBodyZoneRequestTopsZoneRequestTop, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.biz_type is not None:
            result['BizType'] = self.biz_type
        if self.request_count is not None:
            result['RequestCount'] = self.request_count
        if self.zone_name is not None:
            result['ZoneName'] = self.zone_name
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('BizType') is not None:
            self.biz_type = m.get('BizType')
        if m.get('RequestCount') is not None:
            self.request_count = m.get('RequestCount')
        if m.get('ZoneName') is not None:
            self.zone_name = m.get('ZoneName')
        return self


class DescribeStatisticSummaryResponseBodyZoneRequestTops(TeaModel):
    def __init__(self, zone_request_top=None):
        self.zone_request_top = zone_request_top  # type: list[DescribeStatisticSummaryResponseBodyZoneRequestTopsZoneRequestTop]

    def validate(self):
        if self.zone_request_top:
            for k in self.zone_request_top:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(DescribeStatisticSummaryResponseBodyZoneRequestTops, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        result['ZoneRequestTop'] = []
        if self.zone_request_top is not None:
            for k in self.zone_request_top:
                result['ZoneRequestTop'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        self.zone_request_top = []
        if m.get('ZoneRequestTop') is not None:
            for k in m.get('ZoneRequestTop'):
                temp_model = DescribeStatisticSummaryResponseBodyZoneRequestTopsZoneRequestTop()
                self.zone_request_top.append(temp_model.from_map(k))
        return self


class DescribeStatisticSummaryResponseBody(TeaModel):
    def __init__(self, request_id=None, total_count=None, vpc_request_tops=None, zone_request_tops=None):
        self.request_id = request_id  # type: str
        self.total_count = total_count  # type: long
        self.vpc_request_tops = vpc_request_tops  # type: DescribeStatisticSummaryResponseBodyVpcRequestTops
        self.zone_request_tops = zone_request_tops  # type: DescribeStatisticSummaryResponseBodyZoneRequestTops

    def validate(self):
        if self.vpc_request_tops:
            self.vpc_request_tops.validate()
        if self.zone_request_tops:
            self.zone_request_tops.validate()

    def to_map(self):
        _map = super(DescribeStatisticSummaryResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.vpc_request_tops is not None:
            result['VpcRequestTops'] = self.vpc_request_tops.to_map()
        if self.zone_request_tops is not None:
            result['ZoneRequestTops'] = self.zone_request_tops.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('VpcRequestTops') is not None:
            temp_model = DescribeStatisticSummaryResponseBodyVpcRequestTops()
            self.vpc_request_tops = temp_model.from_map(m['VpcRequestTops'])
        if m.get('ZoneRequestTops') is not None:
            temp_model = DescribeStatisticSummaryResponseBodyZoneRequestTops()
            self.zone_request_tops = temp_model.from_map(m['ZoneRequestTops'])
        return self


class DescribeStatisticSummaryResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: DescribeStatisticSummaryResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(DescribeStatisticSummaryResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeStatisticSummaryResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeSyncEcsHostTaskRequest(TeaModel):
    def __init__(self, lang=None, zone_id=None):
        self.lang = lang  # type: str
        self.zone_id = zone_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeSyncEcsHostTaskRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        return self


class DescribeSyncEcsHostTaskResponseBodyEcsRegionsEcsRegionRegionIds(TeaModel):
    def __init__(self, region_id=None):
        self.region_id = region_id  # type: list[str]

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeSyncEcsHostTaskResponseBodyEcsRegionsEcsRegionRegionIds, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class DescribeSyncEcsHostTaskResponseBodyEcsRegionsEcsRegion(TeaModel):
    def __init__(self, region_ids=None, user_id=None):
        self.region_ids = region_ids  # type: DescribeSyncEcsHostTaskResponseBodyEcsRegionsEcsRegionRegionIds
        self.user_id = user_id  # type: long

    def validate(self):
        if self.region_ids:
            self.region_ids.validate()

    def to_map(self):
        _map = super(DescribeSyncEcsHostTaskResponseBodyEcsRegionsEcsRegion, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_ids is not None:
            result['RegionIds'] = self.region_ids.to_map()
        if self.user_id is not None:
            result['UserId'] = self.user_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RegionIds') is not None:
            temp_model = DescribeSyncEcsHostTaskResponseBodyEcsRegionsEcsRegionRegionIds()
            self.region_ids = temp_model.from_map(m['RegionIds'])
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        return self


class DescribeSyncEcsHostTaskResponseBodyEcsRegions(TeaModel):
    def __init__(self, ecs_region=None):
        self.ecs_region = ecs_region  # type: list[DescribeSyncEcsHostTaskResponseBodyEcsRegionsEcsRegion]

    def validate(self):
        if self.ecs_region:
            for k in self.ecs_region:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(DescribeSyncEcsHostTaskResponseBodyEcsRegions, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        result['EcsRegion'] = []
        if self.ecs_region is not None:
            for k in self.ecs_region:
                result['EcsRegion'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        self.ecs_region = []
        if m.get('EcsRegion') is not None:
            for k in m.get('EcsRegion'):
                temp_model = DescribeSyncEcsHostTaskResponseBodyEcsRegionsEcsRegion()
                self.ecs_region.append(temp_model.from_map(k))
        return self


class DescribeSyncEcsHostTaskResponseBodyRegions(TeaModel):
    def __init__(self, region_id=None):
        self.region_id = region_id  # type: list[str]

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeSyncEcsHostTaskResponseBodyRegions, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class DescribeSyncEcsHostTaskResponseBody(TeaModel):
    def __init__(self, ecs_regions=None, regions=None, request_id=None, status=None, success=None, zone_id=None):
        self.ecs_regions = ecs_regions  # type: DescribeSyncEcsHostTaskResponseBodyEcsRegions
        self.regions = regions  # type: DescribeSyncEcsHostTaskResponseBodyRegions
        self.request_id = request_id  # type: str
        self.status = status  # type: str
        self.success = success  # type: bool
        self.zone_id = zone_id  # type: str

    def validate(self):
        if self.ecs_regions:
            self.ecs_regions.validate()
        if self.regions:
            self.regions.validate()

    def to_map(self):
        _map = super(DescribeSyncEcsHostTaskResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.ecs_regions is not None:
            result['EcsRegions'] = self.ecs_regions.to_map()
        if self.regions is not None:
            result['Regions'] = self.regions.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.status is not None:
            result['Status'] = self.status
        if self.success is not None:
            result['Success'] = self.success
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('EcsRegions') is not None:
            temp_model = DescribeSyncEcsHostTaskResponseBodyEcsRegions()
            self.ecs_regions = temp_model.from_map(m['EcsRegions'])
        if m.get('Regions') is not None:
            temp_model = DescribeSyncEcsHostTaskResponseBodyRegions()
            self.regions = temp_model.from_map(m['Regions'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        return self


class DescribeSyncEcsHostTaskResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: DescribeSyncEcsHostTaskResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(DescribeSyncEcsHostTaskResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeSyncEcsHostTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeTagsRequest(TeaModel):
    def __init__(self, lang=None, page_number=None, page_size=None, resource_type=None):
        self.lang = lang  # type: str
        self.page_number = page_number  # type: int
        self.page_size = page_size  # type: int
        self.resource_type = resource_type  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeTagsRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        return self


class DescribeTagsResponseBodyTags(TeaModel):
    def __init__(self, key=None, values=None):
        self.key = key  # type: str
        self.values = values  # type: list[str]

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeTagsResponseBodyTags, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.values is not None:
            result['Values'] = self.values
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Values') is not None:
            self.values = m.get('Values')
        return self


class DescribeTagsResponseBody(TeaModel):
    def __init__(self, page_number=None, page_size=None, request_id=None, tags=None, total_count=None):
        self.page_number = page_number  # type: int
        self.page_size = page_size  # type: int
        self.request_id = request_id  # type: str
        self.tags = tags  # type: list[DescribeTagsResponseBodyTags]
        self.total_count = total_count  # type: int

    def validate(self):
        if self.tags:
            for k in self.tags:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(DescribeTagsResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Tags'] = []
        if self.tags is not None:
            for k in self.tags:
                result['Tags'].append(k.to_map() if k else None)
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.tags = []
        if m.get('Tags') is not None:
            for k in m.get('Tags'):
                temp_model = DescribeTagsResponseBodyTags()
                self.tags.append(temp_model.from_map(k))
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        return self


class DescribeTagsResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: DescribeTagsResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(DescribeTagsResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeTagsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeUserVpcAuthorizationsRequest(TeaModel):
    def __init__(self, auth_type=None, authorized_user_id=None, page_number=None, page_size=None):
        self.auth_type = auth_type  # type: str
        self.authorized_user_id = authorized_user_id  # type: long
        self.page_number = page_number  # type: int
        self.page_size = page_size  # type: int

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeUserVpcAuthorizationsRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.auth_type is not None:
            result['AuthType'] = self.auth_type
        if self.authorized_user_id is not None:
            result['AuthorizedUserId'] = self.authorized_user_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('AuthType') is not None:
            self.auth_type = m.get('AuthType')
        if m.get('AuthorizedUserId') is not None:
            self.authorized_user_id = m.get('AuthorizedUserId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeUserVpcAuthorizationsResponseBodyUsers(TeaModel):
    def __init__(self, auth_type=None, authorized_aliyun_id=None, authorized_user_id=None, create_time=None,
                 create_timestamp=None):
        self.auth_type = auth_type  # type: str
        self.authorized_aliyun_id = authorized_aliyun_id  # type: str
        self.authorized_user_id = authorized_user_id  # type: long
        self.create_time = create_time  # type: str
        self.create_timestamp = create_timestamp  # type: long

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeUserVpcAuthorizationsResponseBodyUsers, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.auth_type is not None:
            result['AuthType'] = self.auth_type
        if self.authorized_aliyun_id is not None:
            result['AuthorizedAliyunId'] = self.authorized_aliyun_id
        if self.authorized_user_id is not None:
            result['AuthorizedUserId'] = self.authorized_user_id
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('AuthType') is not None:
            self.auth_type = m.get('AuthType')
        if m.get('AuthorizedAliyunId') is not None:
            self.authorized_aliyun_id = m.get('AuthorizedAliyunId')
        if m.get('AuthorizedUserId') is not None:
            self.authorized_user_id = m.get('AuthorizedUserId')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        return self


class DescribeUserVpcAuthorizationsResponseBody(TeaModel):
    def __init__(self, page_number=None, page_size=None, request_id=None, total_items=None, total_pages=None,
                 users=None):
        self.page_number = page_number  # type: int
        self.page_size = page_size  # type: int
        self.request_id = request_id  # type: str
        self.total_items = total_items  # type: int
        self.total_pages = total_pages  # type: int
        self.users = users  # type: list[DescribeUserVpcAuthorizationsResponseBodyUsers]

    def validate(self):
        if self.users:
            for k in self.users:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(DescribeUserVpcAuthorizationsResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_items is not None:
            result['TotalItems'] = self.total_items
        if self.total_pages is not None:
            result['TotalPages'] = self.total_pages
        result['Users'] = []
        if self.users is not None:
            for k in self.users:
                result['Users'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalItems') is not None:
            self.total_items = m.get('TotalItems')
        if m.get('TotalPages') is not None:
            self.total_pages = m.get('TotalPages')
        self.users = []
        if m.get('Users') is not None:
            for k in m.get('Users'):
                temp_model = DescribeUserVpcAuthorizationsResponseBodyUsers()
                self.users.append(temp_model.from_map(k))
        return self


class DescribeUserVpcAuthorizationsResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: DescribeUserVpcAuthorizationsResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(DescribeUserVpcAuthorizationsResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeUserVpcAuthorizationsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeZoneInfoRequest(TeaModel):
    def __init__(self, lang=None, zone_id=None):
        self.lang = lang  # type: str
        # Zone ID。
        self.zone_id = zone_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeZoneInfoRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        return self


class DescribeZoneInfoResponseBodyBindVpcsVpc(TeaModel):
    def __init__(self, region_id=None, region_name=None, vpc_id=None, vpc_name=None, vpc_type=None, vpc_user_id=None):
        self.region_id = region_id  # type: str
        self.region_name = region_name  # type: str
        # Vpc ID。
        self.vpc_id = vpc_id  # type: str
        self.vpc_name = vpc_name  # type: str
        self.vpc_type = vpc_type  # type: str
        self.vpc_user_id = vpc_user_id  # type: long

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeZoneInfoResponseBodyBindVpcsVpc, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.region_name is not None:
            result['RegionName'] = self.region_name
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.vpc_name is not None:
            result['VpcName'] = self.vpc_name
        if self.vpc_type is not None:
            result['VpcType'] = self.vpc_type
        if self.vpc_user_id is not None:
            result['VpcUserId'] = self.vpc_user_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('RegionName') is not None:
            self.region_name = m.get('RegionName')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('VpcName') is not None:
            self.vpc_name = m.get('VpcName')
        if m.get('VpcType') is not None:
            self.vpc_type = m.get('VpcType')
        if m.get('VpcUserId') is not None:
            self.vpc_user_id = m.get('VpcUserId')
        return self


class DescribeZoneInfoResponseBodyBindVpcs(TeaModel):
    def __init__(self, vpc=None):
        self.vpc = vpc  # type: list[DescribeZoneInfoResponseBodyBindVpcsVpc]

    def validate(self):
        if self.vpc:
            for k in self.vpc:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(DescribeZoneInfoResponseBodyBindVpcs, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Vpc'] = []
        if self.vpc is not None:
            for k in self.vpc:
                result['Vpc'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        self.vpc = []
        if m.get('Vpc') is not None:
            for k in m.get('Vpc'):
                temp_model = DescribeZoneInfoResponseBodyBindVpcsVpc()
                self.vpc.append(temp_model.from_map(k))
        return self


class DescribeZoneInfoResponseBody(TeaModel):
    def __init__(self, bind_vpcs=None, create_time=None, create_timestamp=None, creator=None, creator_type=None,
                 dns_group=None, dns_group_changing=None, is_ptr=None, proxy_pattern=None, record_count=None, remark=None,
                 request_id=None, resource_group_id=None, slave_dns=None, update_time=None, update_timestamp=None,
                 zone_id=None, zone_name=None, zone_tag=None, zone_type=None):
        self.bind_vpcs = bind_vpcs  # type: DescribeZoneInfoResponseBodyBindVpcs
        self.create_time = create_time  # type: str
        self.create_timestamp = create_timestamp  # type: long
        self.creator = creator  # type: str
        self.creator_type = creator_type  # type: str
        self.dns_group = dns_group  # type: str
        self.dns_group_changing = dns_group_changing  # type: bool
        self.is_ptr = is_ptr  # type: bool
        self.proxy_pattern = proxy_pattern  # type: str
        self.record_count = record_count  # type: int
        self.remark = remark  # type: str
        self.request_id = request_id  # type: str
        self.resource_group_id = resource_group_id  # type: str
        self.slave_dns = slave_dns  # type: bool
        self.update_time = update_time  # type: str
        self.update_timestamp = update_timestamp  # type: long
        # Zone ID。
        self.zone_id = zone_id  # type: str
        self.zone_name = zone_name  # type: str
        self.zone_tag = zone_tag  # type: str
        self.zone_type = zone_type  # type: str

    def validate(self):
        if self.bind_vpcs:
            self.bind_vpcs.validate()

    def to_map(self):
        _map = super(DescribeZoneInfoResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.bind_vpcs is not None:
            result['BindVpcs'] = self.bind_vpcs.to_map()
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        if self.creator is not None:
            result['Creator'] = self.creator
        if self.creator_type is not None:
            result['CreatorType'] = self.creator_type
        if self.dns_group is not None:
            result['DnsGroup'] = self.dns_group
        if self.dns_group_changing is not None:
            result['DnsGroupChanging'] = self.dns_group_changing
        if self.is_ptr is not None:
            result['IsPtr'] = self.is_ptr
        if self.proxy_pattern is not None:
            result['ProxyPattern'] = self.proxy_pattern
        if self.record_count is not None:
            result['RecordCount'] = self.record_count
        if self.remark is not None:
            result['Remark'] = self.remark
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.slave_dns is not None:
            result['SlaveDns'] = self.slave_dns
        if self.update_time is not None:
            result['UpdateTime'] = self.update_time
        if self.update_timestamp is not None:
            result['UpdateTimestamp'] = self.update_timestamp
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        if self.zone_name is not None:
            result['ZoneName'] = self.zone_name
        if self.zone_tag is not None:
            result['ZoneTag'] = self.zone_tag
        if self.zone_type is not None:
            result['ZoneType'] = self.zone_type
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('BindVpcs') is not None:
            temp_model = DescribeZoneInfoResponseBodyBindVpcs()
            self.bind_vpcs = temp_model.from_map(m['BindVpcs'])
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        if m.get('Creator') is not None:
            self.creator = m.get('Creator')
        if m.get('CreatorType') is not None:
            self.creator_type = m.get('CreatorType')
        if m.get('DnsGroup') is not None:
            self.dns_group = m.get('DnsGroup')
        if m.get('DnsGroupChanging') is not None:
            self.dns_group_changing = m.get('DnsGroupChanging')
        if m.get('IsPtr') is not None:
            self.is_ptr = m.get('IsPtr')
        if m.get('ProxyPattern') is not None:
            self.proxy_pattern = m.get('ProxyPattern')
        if m.get('RecordCount') is not None:
            self.record_count = m.get('RecordCount')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('SlaveDns') is not None:
            self.slave_dns = m.get('SlaveDns')
        if m.get('UpdateTime') is not None:
            self.update_time = m.get('UpdateTime')
        if m.get('UpdateTimestamp') is not None:
            self.update_timestamp = m.get('UpdateTimestamp')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        if m.get('ZoneName') is not None:
            self.zone_name = m.get('ZoneName')
        if m.get('ZoneTag') is not None:
            self.zone_tag = m.get('ZoneTag')
        if m.get('ZoneType') is not None:
            self.zone_type = m.get('ZoneType')
        return self


class DescribeZoneInfoResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: DescribeZoneInfoResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(DescribeZoneInfoResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeZoneInfoResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeZoneRecordsRequest(TeaModel):
    def __init__(self, keyword=None, lang=None, page_number=None, page_size=None, search_mode=None, tag=None,
                 user_client_ip=None, zone_id=None):
        self.keyword = keyword  # type: str
        self.lang = lang  # type: str
        self.page_number = page_number  # type: int
        self.page_size = page_size  # type: int
        self.search_mode = search_mode  # type: str
        self.tag = tag  # type: str
        self.user_client_ip = user_client_ip  # type: str
        # Zone ID。
        self.zone_id = zone_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeZoneRecordsRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.keyword is not None:
            result['Keyword'] = self.keyword
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.search_mode is not None:
            result['SearchMode'] = self.search_mode
        if self.tag is not None:
            result['Tag'] = self.tag
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Keyword') is not None:
            self.keyword = m.get('Keyword')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('SearchMode') is not None:
            self.search_mode = m.get('SearchMode')
        if m.get('Tag') is not None:
            self.tag = m.get('Tag')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        return self


class DescribeZoneRecordsResponseBodyRecordsRecord(TeaModel):
    def __init__(self, create_time=None, create_timestamp=None, line=None, priority=None, record_id=None,
                 remark=None, rr=None, status=None, ttl=None, type=None, update_time=None, update_timestamp=None, value=None,
                 weight=None, zone_id=None):
        self.create_time = create_time  # type: str
        self.create_timestamp = create_timestamp  # type: long
        self.line = line  # type: str
        self.priority = priority  # type: int
        self.record_id = record_id  # type: long
        self.remark = remark  # type: str
        self.rr = rr  # type: str
        self.status = status  # type: str
        self.ttl = ttl  # type: int
        self.type = type  # type: str
        self.update_time = update_time  # type: str
        self.update_timestamp = update_timestamp  # type: long
        self.value = value  # type: str
        self.weight = weight  # type: int
        self.zone_id = zone_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeZoneRecordsResponseBodyRecordsRecord, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        if self.line is not None:
            result['Line'] = self.line
        if self.priority is not None:
            result['Priority'] = self.priority
        if self.record_id is not None:
            result['RecordId'] = self.record_id
        if self.remark is not None:
            result['Remark'] = self.remark
        if self.rr is not None:
            result['Rr'] = self.rr
        if self.status is not None:
            result['Status'] = self.status
        if self.ttl is not None:
            result['Ttl'] = self.ttl
        if self.type is not None:
            result['Type'] = self.type
        if self.update_time is not None:
            result['UpdateTime'] = self.update_time
        if self.update_timestamp is not None:
            result['UpdateTimestamp'] = self.update_timestamp
        if self.value is not None:
            result['Value'] = self.value
        if self.weight is not None:
            result['Weight'] = self.weight
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        if m.get('Line') is not None:
            self.line = m.get('Line')
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        if m.get('RecordId') is not None:
            self.record_id = m.get('RecordId')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        if m.get('Rr') is not None:
            self.rr = m.get('Rr')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('Ttl') is not None:
            self.ttl = m.get('Ttl')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('UpdateTime') is not None:
            self.update_time = m.get('UpdateTime')
        if m.get('UpdateTimestamp') is not None:
            self.update_timestamp = m.get('UpdateTimestamp')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Weight') is not None:
            self.weight = m.get('Weight')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        return self


class DescribeZoneRecordsResponseBodyRecords(TeaModel):
    def __init__(self, record=None):
        self.record = record  # type: list[DescribeZoneRecordsResponseBodyRecordsRecord]

    def validate(self):
        if self.record:
            for k in self.record:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(DescribeZoneRecordsResponseBodyRecords, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Record'] = []
        if self.record is not None:
            for k in self.record:
                result['Record'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        self.record = []
        if m.get('Record') is not None:
            for k in m.get('Record'):
                temp_model = DescribeZoneRecordsResponseBodyRecordsRecord()
                self.record.append(temp_model.from_map(k))
        return self


class DescribeZoneRecordsResponseBody(TeaModel):
    def __init__(self, page_number=None, page_size=None, records=None, request_id=None, total_items=None,
                 total_pages=None):
        self.page_number = page_number  # type: int
        self.page_size = page_size  # type: int
        self.records = records  # type: DescribeZoneRecordsResponseBodyRecords
        self.request_id = request_id  # type: str
        self.total_items = total_items  # type: int
        self.total_pages = total_pages  # type: int

    def validate(self):
        if self.records:
            self.records.validate()

    def to_map(self):
        _map = super(DescribeZoneRecordsResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.records is not None:
            result['Records'] = self.records.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_items is not None:
            result['TotalItems'] = self.total_items
        if self.total_pages is not None:
            result['TotalPages'] = self.total_pages
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Records') is not None:
            temp_model = DescribeZoneRecordsResponseBodyRecords()
            self.records = temp_model.from_map(m['Records'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalItems') is not None:
            self.total_items = m.get('TotalItems')
        if m.get('TotalPages') is not None:
            self.total_pages = m.get('TotalPages')
        return self


class DescribeZoneRecordsResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: DescribeZoneRecordsResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(DescribeZoneRecordsResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeZoneRecordsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeZoneVpcTreeRequest(TeaModel):
    def __init__(self, lang=None, user_client_ip=None):
        self.lang = lang  # type: str
        self.user_client_ip = user_client_ip  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeZoneVpcTreeRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        return self


class DescribeZoneVpcTreeResponseBodyZonesZoneVpcsVpc(TeaModel):
    def __init__(self, region_id=None, region_name=None, vpc_id=None, vpc_name=None, vpc_type=None):
        # region Id
        self.region_id = region_id  # type: str
        self.region_name = region_name  # type: str
        # vpc id
        self.vpc_id = vpc_id  # type: str
        self.vpc_name = vpc_name  # type: str
        self.vpc_type = vpc_type  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeZoneVpcTreeResponseBodyZonesZoneVpcsVpc, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.region_name is not None:
            result['RegionName'] = self.region_name
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.vpc_name is not None:
            result['VpcName'] = self.vpc_name
        if self.vpc_type is not None:
            result['VpcType'] = self.vpc_type
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('RegionName') is not None:
            self.region_name = m.get('RegionName')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('VpcName') is not None:
            self.vpc_name = m.get('VpcName')
        if m.get('VpcType') is not None:
            self.vpc_type = m.get('VpcType')
        return self


class DescribeZoneVpcTreeResponseBodyZonesZoneVpcs(TeaModel):
    def __init__(self, vpc=None):
        self.vpc = vpc  # type: list[DescribeZoneVpcTreeResponseBodyZonesZoneVpcsVpc]

    def validate(self):
        if self.vpc:
            for k in self.vpc:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(DescribeZoneVpcTreeResponseBodyZonesZoneVpcs, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Vpc'] = []
        if self.vpc is not None:
            for k in self.vpc:
                result['Vpc'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        self.vpc = []
        if m.get('Vpc') is not None:
            for k in m.get('Vpc'):
                temp_model = DescribeZoneVpcTreeResponseBodyZonesZoneVpcsVpc()
                self.vpc.append(temp_model.from_map(k))
        return self


class DescribeZoneVpcTreeResponseBodyZonesZone(TeaModel):
    def __init__(self, create_time=None, create_timestamp=None, creator=None, creator_type=None, dns_group=None,
                 dns_group_changing=None, is_ptr=None, record_count=None, remark=None, update_time=None, update_timestamp=None,
                 vpcs=None, zone_id=None, zone_name=None, zone_tag=None, zone_type=None):
        self.create_time = create_time  # type: str
        self.create_timestamp = create_timestamp  # type: long
        self.creator = creator  # type: str
        self.creator_type = creator_type  # type: str
        self.dns_group = dns_group  # type: str
        self.dns_group_changing = dns_group_changing  # type: bool
        self.is_ptr = is_ptr  # type: bool
        self.record_count = record_count  # type: int
        self.remark = remark  # type: str
        self.update_time = update_time  # type: str
        self.update_timestamp = update_timestamp  # type: long
        self.vpcs = vpcs  # type: DescribeZoneVpcTreeResponseBodyZonesZoneVpcs
        # Zone id
        self.zone_id = zone_id  # type: str
        self.zone_name = zone_name  # type: str
        self.zone_tag = zone_tag  # type: str
        self.zone_type = zone_type  # type: str

    def validate(self):
        if self.vpcs:
            self.vpcs.validate()

    def to_map(self):
        _map = super(DescribeZoneVpcTreeResponseBodyZonesZone, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        if self.creator is not None:
            result['Creator'] = self.creator
        if self.creator_type is not None:
            result['CreatorType'] = self.creator_type
        if self.dns_group is not None:
            result['DnsGroup'] = self.dns_group
        if self.dns_group_changing is not None:
            result['DnsGroupChanging'] = self.dns_group_changing
        if self.is_ptr is not None:
            result['IsPtr'] = self.is_ptr
        if self.record_count is not None:
            result['RecordCount'] = self.record_count
        if self.remark is not None:
            result['Remark'] = self.remark
        if self.update_time is not None:
            result['UpdateTime'] = self.update_time
        if self.update_timestamp is not None:
            result['UpdateTimestamp'] = self.update_timestamp
        if self.vpcs is not None:
            result['Vpcs'] = self.vpcs.to_map()
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        if self.zone_name is not None:
            result['ZoneName'] = self.zone_name
        if self.zone_tag is not None:
            result['ZoneTag'] = self.zone_tag
        if self.zone_type is not None:
            result['ZoneType'] = self.zone_type
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        if m.get('Creator') is not None:
            self.creator = m.get('Creator')
        if m.get('CreatorType') is not None:
            self.creator_type = m.get('CreatorType')
        if m.get('DnsGroup') is not None:
            self.dns_group = m.get('DnsGroup')
        if m.get('DnsGroupChanging') is not None:
            self.dns_group_changing = m.get('DnsGroupChanging')
        if m.get('IsPtr') is not None:
            self.is_ptr = m.get('IsPtr')
        if m.get('RecordCount') is not None:
            self.record_count = m.get('RecordCount')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        if m.get('UpdateTime') is not None:
            self.update_time = m.get('UpdateTime')
        if m.get('UpdateTimestamp') is not None:
            self.update_timestamp = m.get('UpdateTimestamp')
        if m.get('Vpcs') is not None:
            temp_model = DescribeZoneVpcTreeResponseBodyZonesZoneVpcs()
            self.vpcs = temp_model.from_map(m['Vpcs'])
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        if m.get('ZoneName') is not None:
            self.zone_name = m.get('ZoneName')
        if m.get('ZoneTag') is not None:
            self.zone_tag = m.get('ZoneTag')
        if m.get('ZoneType') is not None:
            self.zone_type = m.get('ZoneType')
        return self


class DescribeZoneVpcTreeResponseBodyZones(TeaModel):
    def __init__(self, zone=None):
        self.zone = zone  # type: list[DescribeZoneVpcTreeResponseBodyZonesZone]

    def validate(self):
        if self.zone:
            for k in self.zone:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(DescribeZoneVpcTreeResponseBodyZones, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Zone'] = []
        if self.zone is not None:
            for k in self.zone:
                result['Zone'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        self.zone = []
        if m.get('Zone') is not None:
            for k in m.get('Zone'):
                temp_model = DescribeZoneVpcTreeResponseBodyZonesZone()
                self.zone.append(temp_model.from_map(k))
        return self


class DescribeZoneVpcTreeResponseBody(TeaModel):
    def __init__(self, request_id=None, zones=None):
        self.request_id = request_id  # type: str
        self.zones = zones  # type: DescribeZoneVpcTreeResponseBodyZones

    def validate(self):
        if self.zones:
            self.zones.validate()

    def to_map(self):
        _map = super(DescribeZoneVpcTreeResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.zones is not None:
            result['Zones'] = self.zones.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Zones') is not None:
            temp_model = DescribeZoneVpcTreeResponseBodyZones()
            self.zones = temp_model.from_map(m['Zones'])
        return self


class DescribeZoneVpcTreeResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: DescribeZoneVpcTreeResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(DescribeZoneVpcTreeResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeZoneVpcTreeResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeZonesRequestResourceTag(TeaModel):
    def __init__(self, key=None, value=None):
        self.key = key  # type: str
        self.value = value  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeZonesRequestResourceTag, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class DescribeZonesRequest(TeaModel):
    def __init__(self, keyword=None, lang=None, page_number=None, page_size=None, query_region_id=None,
                 query_vpc_id=None, resource_group_id=None, resource_tag=None, search_mode=None, zone_tag=None, zone_type=None):
        self.keyword = keyword  # type: str
        self.lang = lang  # type: str
        self.page_number = page_number  # type: int
        self.page_size = page_size  # type: int
        self.query_region_id = query_region_id  # type: str
        # VPC ID。
        self.query_vpc_id = query_vpc_id  # type: str
        self.resource_group_id = resource_group_id  # type: str
        self.resource_tag = resource_tag  # type: list[DescribeZonesRequestResourceTag]
        self.search_mode = search_mode  # type: str
        self.zone_tag = zone_tag  # type: list[str]
        self.zone_type = zone_type  # type: str

    def validate(self):
        if self.resource_tag:
            for k in self.resource_tag:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(DescribeZonesRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.keyword is not None:
            result['Keyword'] = self.keyword
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.query_region_id is not None:
            result['QueryRegionId'] = self.query_region_id
        if self.query_vpc_id is not None:
            result['QueryVpcId'] = self.query_vpc_id
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        result['ResourceTag'] = []
        if self.resource_tag is not None:
            for k in self.resource_tag:
                result['ResourceTag'].append(k.to_map() if k else None)
        if self.search_mode is not None:
            result['SearchMode'] = self.search_mode
        if self.zone_tag is not None:
            result['ZoneTag'] = self.zone_tag
        if self.zone_type is not None:
            result['ZoneType'] = self.zone_type
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Keyword') is not None:
            self.keyword = m.get('Keyword')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('QueryRegionId') is not None:
            self.query_region_id = m.get('QueryRegionId')
        if m.get('QueryVpcId') is not None:
            self.query_vpc_id = m.get('QueryVpcId')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        self.resource_tag = []
        if m.get('ResourceTag') is not None:
            for k in m.get('ResourceTag'):
                temp_model = DescribeZonesRequestResourceTag()
                self.resource_tag.append(temp_model.from_map(k))
        if m.get('SearchMode') is not None:
            self.search_mode = m.get('SearchMode')
        if m.get('ZoneTag') is not None:
            self.zone_tag = m.get('ZoneTag')
        if m.get('ZoneType') is not None:
            self.zone_type = m.get('ZoneType')
        return self


class DescribeZonesResponseBodyZonesZoneResourceTagsResourceTag(TeaModel):
    def __init__(self, key=None, value=None):
        self.key = key  # type: str
        self.value = value  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(DescribeZonesResponseBodyZonesZoneResourceTagsResourceTag, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class DescribeZonesResponseBodyZonesZoneResourceTags(TeaModel):
    def __init__(self, resource_tag=None):
        self.resource_tag = resource_tag  # type: list[DescribeZonesResponseBodyZonesZoneResourceTagsResourceTag]

    def validate(self):
        if self.resource_tag:
            for k in self.resource_tag:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(DescribeZonesResponseBodyZonesZoneResourceTags, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        result['ResourceTag'] = []
        if self.resource_tag is not None:
            for k in self.resource_tag:
                result['ResourceTag'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        self.resource_tag = []
        if m.get('ResourceTag') is not None:
            for k in m.get('ResourceTag'):
                temp_model = DescribeZonesResponseBodyZonesZoneResourceTagsResourceTag()
                self.resource_tag.append(temp_model.from_map(k))
        return self


class DescribeZonesResponseBodyZonesZone(TeaModel):
    def __init__(self, create_time=None, create_timestamp=None, creator=None, creator_sub_type=None, dns_group=None,
                 dns_group_changing=None, is_ptr=None, proxy_pattern=None, record_count=None, remark=None, resource_group_id=None,
                 resource_tags=None, update_time=None, update_timestamp=None, zone_id=None, zone_name=None, zone_tag=None,
                 zone_type=None):
        self.create_time = create_time  # type: str
        self.create_timestamp = create_timestamp  # type: long
        self.creator = creator  # type: str
        self.creator_sub_type = creator_sub_type  # type: str
        self.dns_group = dns_group  # type: str
        self.dns_group_changing = dns_group_changing  # type: bool
        self.is_ptr = is_ptr  # type: bool
        self.proxy_pattern = proxy_pattern  # type: str
        self.record_count = record_count  # type: int
        self.remark = remark  # type: str
        self.resource_group_id = resource_group_id  # type: str
        self.resource_tags = resource_tags  # type: DescribeZonesResponseBodyZonesZoneResourceTags
        self.update_time = update_time  # type: str
        self.update_timestamp = update_timestamp  # type: long
        # zone ID。
        self.zone_id = zone_id  # type: str
        self.zone_name = zone_name  # type: str
        self.zone_tag = zone_tag  # type: str
        self.zone_type = zone_type  # type: str

    def validate(self):
        if self.resource_tags:
            self.resource_tags.validate()

    def to_map(self):
        _map = super(DescribeZonesResponseBodyZonesZone, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.create_timestamp is not None:
            result['CreateTimestamp'] = self.create_timestamp
        if self.creator is not None:
            result['Creator'] = self.creator
        if self.creator_sub_type is not None:
            result['CreatorSubType'] = self.creator_sub_type
        if self.dns_group is not None:
            result['DnsGroup'] = self.dns_group
        if self.dns_group_changing is not None:
            result['DnsGroupChanging'] = self.dns_group_changing
        if self.is_ptr is not None:
            result['IsPtr'] = self.is_ptr
        if self.proxy_pattern is not None:
            result['ProxyPattern'] = self.proxy_pattern
        if self.record_count is not None:
            result['RecordCount'] = self.record_count
        if self.remark is not None:
            result['Remark'] = self.remark
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.resource_tags is not None:
            result['ResourceTags'] = self.resource_tags.to_map()
        if self.update_time is not None:
            result['UpdateTime'] = self.update_time
        if self.update_timestamp is not None:
            result['UpdateTimestamp'] = self.update_timestamp
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        if self.zone_name is not None:
            result['ZoneName'] = self.zone_name
        if self.zone_tag is not None:
            result['ZoneTag'] = self.zone_tag
        if self.zone_type is not None:
            result['ZoneType'] = self.zone_type
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('CreateTimestamp') is not None:
            self.create_timestamp = m.get('CreateTimestamp')
        if m.get('Creator') is not None:
            self.creator = m.get('Creator')
        if m.get('CreatorSubType') is not None:
            self.creator_sub_type = m.get('CreatorSubType')
        if m.get('DnsGroup') is not None:
            self.dns_group = m.get('DnsGroup')
        if m.get('DnsGroupChanging') is not None:
            self.dns_group_changing = m.get('DnsGroupChanging')
        if m.get('IsPtr') is not None:
            self.is_ptr = m.get('IsPtr')
        if m.get('ProxyPattern') is not None:
            self.proxy_pattern = m.get('ProxyPattern')
        if m.get('RecordCount') is not None:
            self.record_count = m.get('RecordCount')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('ResourceTags') is not None:
            temp_model = DescribeZonesResponseBodyZonesZoneResourceTags()
            self.resource_tags = temp_model.from_map(m['ResourceTags'])
        if m.get('UpdateTime') is not None:
            self.update_time = m.get('UpdateTime')
        if m.get('UpdateTimestamp') is not None:
            self.update_timestamp = m.get('UpdateTimestamp')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        if m.get('ZoneName') is not None:
            self.zone_name = m.get('ZoneName')
        if m.get('ZoneTag') is not None:
            self.zone_tag = m.get('ZoneTag')
        if m.get('ZoneType') is not None:
            self.zone_type = m.get('ZoneType')
        return self


class DescribeZonesResponseBodyZones(TeaModel):
    def __init__(self, zone=None):
        self.zone = zone  # type: list[DescribeZonesResponseBodyZonesZone]

    def validate(self):
        if self.zone:
            for k in self.zone:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(DescribeZonesResponseBodyZones, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Zone'] = []
        if self.zone is not None:
            for k in self.zone:
                result['Zone'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        self.zone = []
        if m.get('Zone') is not None:
            for k in m.get('Zone'):
                temp_model = DescribeZonesResponseBodyZonesZone()
                self.zone.append(temp_model.from_map(k))
        return self


class DescribeZonesResponseBody(TeaModel):
    def __init__(self, page_number=None, page_size=None, request_id=None, total_items=None, total_pages=None,
                 zones=None):
        self.page_number = page_number  # type: int
        self.page_size = page_size  # type: int
        self.request_id = request_id  # type: str
        self.total_items = total_items  # type: int
        self.total_pages = total_pages  # type: int
        self.zones = zones  # type: DescribeZonesResponseBodyZones

    def validate(self):
        if self.zones:
            self.zones.validate()

    def to_map(self):
        _map = super(DescribeZonesResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_items is not None:
            result['TotalItems'] = self.total_items
        if self.total_pages is not None:
            result['TotalPages'] = self.total_pages
        if self.zones is not None:
            result['Zones'] = self.zones.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalItems') is not None:
            self.total_items = m.get('TotalItems')
        if m.get('TotalPages') is not None:
            self.total_pages = m.get('TotalPages')
        if m.get('Zones') is not None:
            temp_model = DescribeZonesResponseBodyZones()
            self.zones = temp_model.from_map(m['Zones'])
        return self


class DescribeZonesResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: DescribeZonesResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(DescribeZonesResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DescribeZonesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListTagResourcesRequestTag(TeaModel):
    def __init__(self, key=None, value=None):
        self.key = key  # type: str
        self.value = value  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(ListTagResourcesRequestTag, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class ListTagResourcesRequest(TeaModel):
    def __init__(self, lang=None, next_token=None, resource_id=None, resource_type=None, size=None, tag=None):
        self.lang = lang  # type: str
        self.next_token = next_token  # type: str
        self.resource_id = resource_id  # type: list[str]
        self.resource_type = resource_type  # type: str
        self.size = size  # type: int
        self.tag = tag  # type: list[ListTagResourcesRequestTag]

    def validate(self):
        if self.tag:
            for k in self.tag:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(ListTagResourcesRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.size is not None:
            result['Size'] = self.size
        result['Tag'] = []
        if self.tag is not None:
            for k in self.tag:
                result['Tag'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('Size') is not None:
            self.size = m.get('Size')
        self.tag = []
        if m.get('Tag') is not None:
            for k in m.get('Tag'):
                temp_model = ListTagResourcesRequestTag()
                self.tag.append(temp_model.from_map(k))
        return self


class ListTagResourcesResponseBodyTagResources(TeaModel):
    def __init__(self, resource_id=None, resource_type=None, tag_key=None, tag_value=None):
        self.resource_id = resource_id  # type: str
        self.resource_type = resource_type  # type: str
        self.tag_key = tag_key  # type: str
        self.tag_value = tag_value  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(ListTagResourcesResponseBodyTagResources, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.tag_key is not None:
            result['TagKey'] = self.tag_key
        if self.tag_value is not None:
            result['TagValue'] = self.tag_value
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('TagKey') is not None:
            self.tag_key = m.get('TagKey')
        if m.get('TagValue') is not None:
            self.tag_value = m.get('TagValue')
        return self


class ListTagResourcesResponseBody(TeaModel):
    def __init__(self, next_token=None, request_id=None, tag_resources=None):
        self.next_token = next_token  # type: str
        self.request_id = request_id  # type: str
        self.tag_resources = tag_resources  # type: list[ListTagResourcesResponseBodyTagResources]

    def validate(self):
        if self.tag_resources:
            for k in self.tag_resources:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(ListTagResourcesResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['TagResources'] = []
        if self.tag_resources is not None:
            for k in self.tag_resources:
                result['TagResources'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.tag_resources = []
        if m.get('TagResources') is not None:
            for k in m.get('TagResources'):
                temp_model = ListTagResourcesResponseBodyTagResources()
                self.tag_resources.append(temp_model.from_map(k))
        return self


class ListTagResourcesResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: ListTagResourcesResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(ListTagResourcesResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ListTagResourcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class MoveResourceGroupRequest(TeaModel):
    def __init__(self, client_token=None, lang=None, new_resource_group_id=None, resource_id=None):
        self.client_token = client_token  # type: str
        self.lang = lang  # type: str
        self.new_resource_group_id = new_resource_group_id  # type: str
        # Zone Id。
        self.resource_id = resource_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(MoveResourceGroupRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.new_resource_group_id is not None:
            result['NewResourceGroupId'] = self.new_resource_group_id
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('NewResourceGroupId') is not None:
            self.new_resource_group_id = m.get('NewResourceGroupId')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        return self


class MoveResourceGroupResponseBody(TeaModel):
    def __init__(self, request_id=None):
        self.request_id = request_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(MoveResourceGroupResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class MoveResourceGroupResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: MoveResourceGroupResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(MoveResourceGroupResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = MoveResourceGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SetProxyPatternRequest(TeaModel):
    def __init__(self, client_token=None, lang=None, proxy_pattern=None, user_client_ip=None, zone_id=None):
        self.client_token = client_token  # type: str
        self.lang = lang  # type: str
        self.proxy_pattern = proxy_pattern  # type: str
        self.user_client_ip = user_client_ip  # type: str
        self.zone_id = zone_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(SetProxyPatternRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.proxy_pattern is not None:
            result['ProxyPattern'] = self.proxy_pattern
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('ProxyPattern') is not None:
            self.proxy_pattern = m.get('ProxyPattern')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        return self


class SetProxyPatternResponseBody(TeaModel):
    def __init__(self, request_id=None, zone_id=None):
        self.request_id = request_id  # type: str
        self.zone_id = zone_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(SetProxyPatternResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        return self


class SetProxyPatternResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: SetProxyPatternResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(SetProxyPatternResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = SetProxyPatternResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SetZoneRecordStatusRequest(TeaModel):
    def __init__(self, client_token=None, lang=None, record_id=None, status=None, user_client_ip=None):
        self.client_token = client_token  # type: str
        self.lang = lang  # type: str
        self.record_id = record_id  # type: long
        self.status = status  # type: str
        self.user_client_ip = user_client_ip  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(SetZoneRecordStatusRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.record_id is not None:
            result['RecordId'] = self.record_id
        if self.status is not None:
            result['Status'] = self.status
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('RecordId') is not None:
            self.record_id = m.get('RecordId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        return self


class SetZoneRecordStatusResponseBody(TeaModel):
    def __init__(self, record_id=None, request_id=None, status=None):
        self.record_id = record_id  # type: long
        self.request_id = request_id  # type: str
        self.status = status  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(SetZoneRecordStatusResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.record_id is not None:
            result['RecordId'] = self.record_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RecordId') is not None:
            self.record_id = m.get('RecordId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class SetZoneRecordStatusResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: SetZoneRecordStatusResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(SetZoneRecordStatusResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = SetZoneRecordStatusResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class TagResourcesRequestTag(TeaModel):
    def __init__(self, key=None, value=None):
        self.key = key  # type: str
        self.value = value  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(TagResourcesRequestTag, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class TagResourcesRequest(TeaModel):
    def __init__(self, lang=None, over_write=None, resource_id=None, resource_type=None, tag=None):
        self.lang = lang  # type: str
        self.over_write = over_write  # type: bool
        self.resource_id = resource_id  # type: list[str]
        self.resource_type = resource_type  # type: str
        self.tag = tag  # type: list[TagResourcesRequestTag]

    def validate(self):
        if self.tag:
            for k in self.tag:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(TagResourcesRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.over_write is not None:
            result['OverWrite'] = self.over_write
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        result['Tag'] = []
        if self.tag is not None:
            for k in self.tag:
                result['Tag'].append(k.to_map() if k else None)
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('OverWrite') is not None:
            self.over_write = m.get('OverWrite')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        self.tag = []
        if m.get('Tag') is not None:
            for k in m.get('Tag'):
                temp_model = TagResourcesRequestTag()
                self.tag.append(temp_model.from_map(k))
        return self


class TagResourcesResponseBody(TeaModel):
    def __init__(self, request_id=None):
        self.request_id = request_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(TagResourcesResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class TagResourcesResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: TagResourcesResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(TagResourcesResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = TagResourcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UntagResourcesRequest(TeaModel):
    def __init__(self, all=None, lang=None, resource_id=None, resource_type=None, tag_key=None):
        self.all = all  # type: bool
        self.lang = lang  # type: str
        self.resource_id = resource_id  # type: list[str]
        self.resource_type = resource_type  # type: str
        self.tag_key = tag_key  # type: list[str]

    def validate(self):
        pass

    def to_map(self):
        _map = super(UntagResourcesRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.all is not None:
            result['All'] = self.all
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.tag_key is not None:
            result['TagKey'] = self.tag_key
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('All') is not None:
            self.all = m.get('All')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('TagKey') is not None:
            self.tag_key = m.get('TagKey')
        return self


class UntagResourcesResponseBody(TeaModel):
    def __init__(self, request_id=None):
        self.request_id = request_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(UntagResourcesResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UntagResourcesResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: UntagResourcesResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(UntagResourcesResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UntagResourcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateRecordRemarkRequest(TeaModel):
    def __init__(self, client_token=None, lang=None, record_id=None, remark=None):
        self.client_token = client_token  # type: str
        self.lang = lang  # type: str
        self.record_id = record_id  # type: long
        self.remark = remark  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(UpdateRecordRemarkRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.record_id is not None:
            result['RecordId'] = self.record_id
        if self.remark is not None:
            result['Remark'] = self.remark
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('RecordId') is not None:
            self.record_id = m.get('RecordId')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        return self


class UpdateRecordRemarkResponseBody(TeaModel):
    def __init__(self, record_id=None, request_id=None):
        self.record_id = record_id  # type: long
        self.request_id = request_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(UpdateRecordRemarkResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.record_id is not None:
            result['RecordId'] = self.record_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RecordId') is not None:
            self.record_id = m.get('RecordId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateRecordRemarkResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: UpdateRecordRemarkResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(UpdateRecordRemarkResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateRecordRemarkResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateResolverEndpointRequestIpConfig(TeaModel):
    def __init__(self, az_id=None, cidr_block=None, ip=None, v_switch_id=None):
        self.az_id = az_id  # type: str
        self.cidr_block = cidr_block  # type: str
        self.ip = ip  # type: str
        self.v_switch_id = v_switch_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(UpdateResolverEndpointRequestIpConfig, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.az_id is not None:
            result['AzId'] = self.az_id
        if self.cidr_block is not None:
            result['CidrBlock'] = self.cidr_block
        if self.ip is not None:
            result['Ip'] = self.ip
        if self.v_switch_id is not None:
            result['VSwitchId'] = self.v_switch_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('AzId') is not None:
            self.az_id = m.get('AzId')
        if m.get('CidrBlock') is not None:
            self.cidr_block = m.get('CidrBlock')
        if m.get('Ip') is not None:
            self.ip = m.get('Ip')
        if m.get('VSwitchId') is not None:
            self.v_switch_id = m.get('VSwitchId')
        return self


class UpdateResolverEndpointRequest(TeaModel):
    def __init__(self, endpoint_id=None, ip_config=None, lang=None, name=None):
        self.endpoint_id = endpoint_id  # type: str
        self.ip_config = ip_config  # type: list[UpdateResolverEndpointRequestIpConfig]
        self.lang = lang  # type: str
        self.name = name  # type: str

    def validate(self):
        if self.ip_config:
            for k in self.ip_config:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(UpdateResolverEndpointRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.endpoint_id is not None:
            result['EndpointId'] = self.endpoint_id
        result['IpConfig'] = []
        if self.ip_config is not None:
            for k in self.ip_config:
                result['IpConfig'].append(k.to_map() if k else None)
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('EndpointId') is not None:
            self.endpoint_id = m.get('EndpointId')
        self.ip_config = []
        if m.get('IpConfig') is not None:
            for k in m.get('IpConfig'):
                temp_model = UpdateResolverEndpointRequestIpConfig()
                self.ip_config.append(temp_model.from_map(k))
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class UpdateResolverEndpointResponseBody(TeaModel):
    def __init__(self, request_id=None):
        self.request_id = request_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(UpdateResolverEndpointResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateResolverEndpointResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: UpdateResolverEndpointResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(UpdateResolverEndpointResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateResolverEndpointResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateResolverRuleRequestForwardIp(TeaModel):
    def __init__(self, ip=None, port=None):
        self.ip = ip  # type: str
        self.port = port  # type: int

    def validate(self):
        pass

    def to_map(self):
        _map = super(UpdateResolverRuleRequestForwardIp, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.ip is not None:
            result['Ip'] = self.ip
        if self.port is not None:
            result['Port'] = self.port
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Ip') is not None:
            self.ip = m.get('Ip')
        if m.get('Port') is not None:
            self.port = m.get('Port')
        return self


class UpdateResolverRuleRequest(TeaModel):
    def __init__(self, forward_ip=None, lang=None, name=None, rule_id=None):
        self.forward_ip = forward_ip  # type: list[UpdateResolverRuleRequestForwardIp]
        self.lang = lang  # type: str
        self.name = name  # type: str
        self.rule_id = rule_id  # type: str

    def validate(self):
        if self.forward_ip:
            for k in self.forward_ip:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(UpdateResolverRuleRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        result['ForwardIp'] = []
        if self.forward_ip is not None:
            for k in self.forward_ip:
                result['ForwardIp'].append(k.to_map() if k else None)
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.name is not None:
            result['Name'] = self.name
        if self.rule_id is not None:
            result['RuleId'] = self.rule_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        self.forward_ip = []
        if m.get('ForwardIp') is not None:
            for k in m.get('ForwardIp'):
                temp_model = UpdateResolverRuleRequestForwardIp()
                self.forward_ip.append(temp_model.from_map(k))
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('RuleId') is not None:
            self.rule_id = m.get('RuleId')
        return self


class UpdateResolverRuleResponseBody(TeaModel):
    def __init__(self, request_id=None):
        self.request_id = request_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(UpdateResolverRuleResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateResolverRuleResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: UpdateResolverRuleResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(UpdateResolverRuleResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateResolverRuleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateSyncEcsHostTaskRequestRegion(TeaModel):
    def __init__(self, region_id=None, user_id=None):
        self.region_id = region_id  # type: str
        self.user_id = user_id  # type: long

    def validate(self):
        pass

    def to_map(self):
        _map = super(UpdateSyncEcsHostTaskRequestRegion, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.user_id is not None:
            result['UserId'] = self.user_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('UserId') is not None:
            self.user_id = m.get('UserId')
        return self


class UpdateSyncEcsHostTaskRequest(TeaModel):
    def __init__(self, lang=None, region=None, status=None, zone_id=None):
        self.lang = lang  # type: str
        self.region = region  # type: list[UpdateSyncEcsHostTaskRequestRegion]
        self.status = status  # type: str
        self.zone_id = zone_id  # type: str

    def validate(self):
        if self.region:
            for k in self.region:
                if k:
                    k.validate()

    def to_map(self):
        _map = super(UpdateSyncEcsHostTaskRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lang is not None:
            result['Lang'] = self.lang
        result['Region'] = []
        if self.region is not None:
            for k in self.region:
                result['Region'].append(k.to_map() if k else None)
        if self.status is not None:
            result['Status'] = self.status
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        self.region = []
        if m.get('Region') is not None:
            for k in m.get('Region'):
                temp_model = UpdateSyncEcsHostTaskRequestRegion()
                self.region.append(temp_model.from_map(k))
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        return self


class UpdateSyncEcsHostTaskResponseBody(TeaModel):
    def __init__(self, request_id=None, success=None):
        self.request_id = request_id  # type: str
        self.success = success  # type: bool

    def validate(self):
        pass

    def to_map(self):
        _map = super(UpdateSyncEcsHostTaskResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class UpdateSyncEcsHostTaskResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: UpdateSyncEcsHostTaskResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(UpdateSyncEcsHostTaskResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateSyncEcsHostTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateZoneRecordRequest(TeaModel):
    def __init__(self, client_token=None, lang=None, line=None, priority=None, record_id=None, rr=None, ttl=None,
                 type=None, user_client_ip=None, value=None, weight=None):
        self.client_token = client_token  # type: str
        self.lang = lang  # type: str
        self.line = line  # type: str
        self.priority = priority  # type: int
        self.record_id = record_id  # type: long
        self.rr = rr  # type: str
        self.ttl = ttl  # type: int
        self.type = type  # type: str
        self.user_client_ip = user_client_ip  # type: str
        self.value = value  # type: str
        self.weight = weight  # type: int

    def validate(self):
        pass

    def to_map(self):
        _map = super(UpdateZoneRecordRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.line is not None:
            result['Line'] = self.line
        if self.priority is not None:
            result['Priority'] = self.priority
        if self.record_id is not None:
            result['RecordId'] = self.record_id
        if self.rr is not None:
            result['Rr'] = self.rr
        if self.ttl is not None:
            result['Ttl'] = self.ttl
        if self.type is not None:
            result['Type'] = self.type
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.value is not None:
            result['Value'] = self.value
        if self.weight is not None:
            result['Weight'] = self.weight
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('Line') is not None:
            self.line = m.get('Line')
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        if m.get('RecordId') is not None:
            self.record_id = m.get('RecordId')
        if m.get('Rr') is not None:
            self.rr = m.get('Rr')
        if m.get('Ttl') is not None:
            self.ttl = m.get('Ttl')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        if m.get('Weight') is not None:
            self.weight = m.get('Weight')
        return self


class UpdateZoneRecordResponseBody(TeaModel):
    def __init__(self, record_id=None, request_id=None):
        self.record_id = record_id  # type: long
        self.request_id = request_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(UpdateZoneRecordResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.record_id is not None:
            result['RecordId'] = self.record_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RecordId') is not None:
            self.record_id = m.get('RecordId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateZoneRecordResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: UpdateZoneRecordResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(UpdateZoneRecordResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateZoneRecordResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateZoneRemarkRequest(TeaModel):
    def __init__(self, client_token=None, lang=None, remark=None, user_client_ip=None, zone_id=None):
        self.client_token = client_token  # type: str
        self.lang = lang  # type: str
        self.remark = remark  # type: str
        self.user_client_ip = user_client_ip  # type: str
        # Zone ID。
        self.zone_id = zone_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(UpdateZoneRemarkRequest, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.lang is not None:
            result['Lang'] = self.lang
        if self.remark is not None:
            result['Remark'] = self.remark
        if self.user_client_ip is not None:
            result['UserClientIp'] = self.user_client_ip
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('Lang') is not None:
            self.lang = m.get('Lang')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        if m.get('UserClientIp') is not None:
            self.user_client_ip = m.get('UserClientIp')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        return self


class UpdateZoneRemarkResponseBody(TeaModel):
    def __init__(self, request_id=None, zone_id=None):
        self.request_id = request_id  # type: str
        # Zone ID。
        self.zone_id = zone_id  # type: str

    def validate(self):
        pass

    def to_map(self):
        _map = super(UpdateZoneRemarkResponseBody, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        return self


class UpdateZoneRemarkResponse(TeaModel):
    def __init__(self, headers=None, status_code=None, body=None):
        self.headers = headers  # type: dict[str, str]
        self.status_code = status_code  # type: int
        self.body = body  # type: UpdateZoneRemarkResponseBody

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super(UpdateZoneRemarkResponse, self).to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateZoneRemarkResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


