'''
# `data_mongodbatlas_backup_compliance_policy`

Refer to the Terraform Registory for docs: [`data_mongodbatlas_backup_compliance_policy`](https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class DataMongodbatlasBackupCompliancePolicy(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasBackupCompliancePolicy.DataMongodbatlasBackupCompliancePolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy mongodbatlas_backup_compliance_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        project_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        on_demand_policy_item: typing.Optional[typing.Union["DataMongodbatlasBackupCompliancePolicyOnDemandPolicyItem", typing.Dict[builtins.str, typing.Any]]] = None,
        policy_item_daily: typing.Optional[typing.Union["DataMongodbatlasBackupCompliancePolicyPolicyItemDaily", typing.Dict[builtins.str, typing.Any]]] = None,
        policy_item_hourly: typing.Optional[typing.Union["DataMongodbatlasBackupCompliancePolicyPolicyItemHourly", typing.Dict[builtins.str, typing.Any]]] = None,
        policy_item_monthly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataMongodbatlasBackupCompliancePolicyPolicyItemMonthly", typing.Dict[builtins.str, typing.Any]]]]] = None,
        policy_item_weekly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataMongodbatlasBackupCompliancePolicyPolicyItemWeekly", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy mongodbatlas_backup_compliance_policy} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#project_id DataMongodbatlasBackupCompliancePolicy#project_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#id DataMongodbatlasBackupCompliancePolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param on_demand_policy_item: on_demand_policy_item block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#on_demand_policy_item DataMongodbatlasBackupCompliancePolicy#on_demand_policy_item}
        :param policy_item_daily: policy_item_daily block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#policy_item_daily DataMongodbatlasBackupCompliancePolicy#policy_item_daily}
        :param policy_item_hourly: policy_item_hourly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#policy_item_hourly DataMongodbatlasBackupCompliancePolicy#policy_item_hourly}
        :param policy_item_monthly: policy_item_monthly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#policy_item_monthly DataMongodbatlasBackupCompliancePolicy#policy_item_monthly}
        :param policy_item_weekly: policy_item_weekly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#policy_item_weekly DataMongodbatlasBackupCompliancePolicy#policy_item_weekly}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__204e5e646fda1cf3ca8ca6909f19fdbad271c335c0812f2957771944799e900d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataMongodbatlasBackupCompliancePolicyConfig(
            project_id=project_id,
            id=id,
            on_demand_policy_item=on_demand_policy_item,
            policy_item_daily=policy_item_daily,
            policy_item_hourly=policy_item_hourly,
            policy_item_monthly=policy_item_monthly,
            policy_item_weekly=policy_item_weekly,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a DataMongodbatlasBackupCompliancePolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataMongodbatlasBackupCompliancePolicy to import.
        :param import_from_id: The id of the existing DataMongodbatlasBackupCompliancePolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataMongodbatlasBackupCompliancePolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92c5f0c941a284e1eec2ecac970194e8763354e822cba406c9a5e1d327ef14c2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putOnDemandPolicyItem")
    def put_on_demand_policy_item(self) -> None:
        value = DataMongodbatlasBackupCompliancePolicyOnDemandPolicyItem()

        return typing.cast(None, jsii.invoke(self, "putOnDemandPolicyItem", [value]))

    @jsii.member(jsii_name="putPolicyItemDaily")
    def put_policy_item_daily(
        self,
        *,
        frequency_interval: jsii.Number,
        retention_unit: builtins.str,
        retention_value: jsii.Number,
    ) -> None:
        '''
        :param frequency_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#frequency_interval DataMongodbatlasBackupCompliancePolicy#frequency_interval}.
        :param retention_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#retention_unit DataMongodbatlasBackupCompliancePolicy#retention_unit}.
        :param retention_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#retention_value DataMongodbatlasBackupCompliancePolicy#retention_value}.
        '''
        value = DataMongodbatlasBackupCompliancePolicyPolicyItemDaily(
            frequency_interval=frequency_interval,
            retention_unit=retention_unit,
            retention_value=retention_value,
        )

        return typing.cast(None, jsii.invoke(self, "putPolicyItemDaily", [value]))

    @jsii.member(jsii_name="putPolicyItemHourly")
    def put_policy_item_hourly(
        self,
        *,
        frequency_interval: jsii.Number,
        retention_unit: builtins.str,
        retention_value: jsii.Number,
    ) -> None:
        '''
        :param frequency_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#frequency_interval DataMongodbatlasBackupCompliancePolicy#frequency_interval}.
        :param retention_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#retention_unit DataMongodbatlasBackupCompliancePolicy#retention_unit}.
        :param retention_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#retention_value DataMongodbatlasBackupCompliancePolicy#retention_value}.
        '''
        value = DataMongodbatlasBackupCompliancePolicyPolicyItemHourly(
            frequency_interval=frequency_interval,
            retention_unit=retention_unit,
            retention_value=retention_value,
        )

        return typing.cast(None, jsii.invoke(self, "putPolicyItemHourly", [value]))

    @jsii.member(jsii_name="putPolicyItemMonthly")
    def put_policy_item_monthly(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataMongodbatlasBackupCompliancePolicyPolicyItemMonthly", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8a3578d669d9123f43a93e5eaaab59a7fbc137310a75deb2e964175c96e84ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPolicyItemMonthly", [value]))

    @jsii.member(jsii_name="putPolicyItemWeekly")
    def put_policy_item_weekly(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataMongodbatlasBackupCompliancePolicyPolicyItemWeekly", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80b4d296f6e9c037af2ac095ad1ce1b26dd9f48af6a11a6d29d5bf101422d52f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPolicyItemWeekly", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOnDemandPolicyItem")
    def reset_on_demand_policy_item(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnDemandPolicyItem", []))

    @jsii.member(jsii_name="resetPolicyItemDaily")
    def reset_policy_item_daily(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyItemDaily", []))

    @jsii.member(jsii_name="resetPolicyItemHourly")
    def reset_policy_item_hourly(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyItemHourly", []))

    @jsii.member(jsii_name="resetPolicyItemMonthly")
    def reset_policy_item_monthly(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyItemMonthly", []))

    @jsii.member(jsii_name="resetPolicyItemWeekly")
    def reset_policy_item_weekly(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyItemWeekly", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="authorizedEmail")
    def authorized_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizedEmail"))

    @builtins.property
    @jsii.member(jsii_name="copyProtectionEnabled")
    def copy_protection_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "copyProtectionEnabled"))

    @builtins.property
    @jsii.member(jsii_name="encryptionAtRestEnabled")
    def encryption_at_rest_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "encryptionAtRestEnabled"))

    @builtins.property
    @jsii.member(jsii_name="onDemandPolicyItem")
    def on_demand_policy_item(
        self,
    ) -> "DataMongodbatlasBackupCompliancePolicyOnDemandPolicyItemOutputReference":
        return typing.cast("DataMongodbatlasBackupCompliancePolicyOnDemandPolicyItemOutputReference", jsii.get(self, "onDemandPolicyItem"))

    @builtins.property
    @jsii.member(jsii_name="pitEnabled")
    def pit_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "pitEnabled"))

    @builtins.property
    @jsii.member(jsii_name="policyItemDaily")
    def policy_item_daily(
        self,
    ) -> "DataMongodbatlasBackupCompliancePolicyPolicyItemDailyOutputReference":
        return typing.cast("DataMongodbatlasBackupCompliancePolicyPolicyItemDailyOutputReference", jsii.get(self, "policyItemDaily"))

    @builtins.property
    @jsii.member(jsii_name="policyItemHourly")
    def policy_item_hourly(
        self,
    ) -> "DataMongodbatlasBackupCompliancePolicyPolicyItemHourlyOutputReference":
        return typing.cast("DataMongodbatlasBackupCompliancePolicyPolicyItemHourlyOutputReference", jsii.get(self, "policyItemHourly"))

    @builtins.property
    @jsii.member(jsii_name="policyItemMonthly")
    def policy_item_monthly(
        self,
    ) -> "DataMongodbatlasBackupCompliancePolicyPolicyItemMonthlyList":
        return typing.cast("DataMongodbatlasBackupCompliancePolicyPolicyItemMonthlyList", jsii.get(self, "policyItemMonthly"))

    @builtins.property
    @jsii.member(jsii_name="policyItemWeekly")
    def policy_item_weekly(
        self,
    ) -> "DataMongodbatlasBackupCompliancePolicyPolicyItemWeeklyList":
        return typing.cast("DataMongodbatlasBackupCompliancePolicyPolicyItemWeeklyList", jsii.get(self, "policyItemWeekly"))

    @builtins.property
    @jsii.member(jsii_name="restoreWindowDays")
    def restore_window_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "restoreWindowDays"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="updatedDate")
    def updated_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedDate"))

    @builtins.property
    @jsii.member(jsii_name="updatedUser")
    def updated_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedUser"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="onDemandPolicyItemInput")
    def on_demand_policy_item_input(
        self,
    ) -> typing.Optional["DataMongodbatlasBackupCompliancePolicyOnDemandPolicyItem"]:
        return typing.cast(typing.Optional["DataMongodbatlasBackupCompliancePolicyOnDemandPolicyItem"], jsii.get(self, "onDemandPolicyItemInput"))

    @builtins.property
    @jsii.member(jsii_name="policyItemDailyInput")
    def policy_item_daily_input(
        self,
    ) -> typing.Optional["DataMongodbatlasBackupCompliancePolicyPolicyItemDaily"]:
        return typing.cast(typing.Optional["DataMongodbatlasBackupCompliancePolicyPolicyItemDaily"], jsii.get(self, "policyItemDailyInput"))

    @builtins.property
    @jsii.member(jsii_name="policyItemHourlyInput")
    def policy_item_hourly_input(
        self,
    ) -> typing.Optional["DataMongodbatlasBackupCompliancePolicyPolicyItemHourly"]:
        return typing.cast(typing.Optional["DataMongodbatlasBackupCompliancePolicyPolicyItemHourly"], jsii.get(self, "policyItemHourlyInput"))

    @builtins.property
    @jsii.member(jsii_name="policyItemMonthlyInput")
    def policy_item_monthly_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataMongodbatlasBackupCompliancePolicyPolicyItemMonthly"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataMongodbatlasBackupCompliancePolicyPolicyItemMonthly"]]], jsii.get(self, "policyItemMonthlyInput"))

    @builtins.property
    @jsii.member(jsii_name="policyItemWeeklyInput")
    def policy_item_weekly_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataMongodbatlasBackupCompliancePolicyPolicyItemWeekly"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataMongodbatlasBackupCompliancePolicyPolicyItemWeekly"]]], jsii.get(self, "policyItemWeeklyInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8885b99871b2e778892a82c023abfda802b948130efbf2d9db902eca04b9b51f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69c6aca2ecf285e25e7b8ff1faafd0814be7c3a3736d1d1b99d11bf69d83b0fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasBackupCompliancePolicy.DataMongodbatlasBackupCompliancePolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "project_id": "projectId",
        "id": "id",
        "on_demand_policy_item": "onDemandPolicyItem",
        "policy_item_daily": "policyItemDaily",
        "policy_item_hourly": "policyItemHourly",
        "policy_item_monthly": "policyItemMonthly",
        "policy_item_weekly": "policyItemWeekly",
    },
)
class DataMongodbatlasBackupCompliancePolicyConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        project_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        on_demand_policy_item: typing.Optional[typing.Union["DataMongodbatlasBackupCompliancePolicyOnDemandPolicyItem", typing.Dict[builtins.str, typing.Any]]] = None,
        policy_item_daily: typing.Optional[typing.Union["DataMongodbatlasBackupCompliancePolicyPolicyItemDaily", typing.Dict[builtins.str, typing.Any]]] = None,
        policy_item_hourly: typing.Optional[typing.Union["DataMongodbatlasBackupCompliancePolicyPolicyItemHourly", typing.Dict[builtins.str, typing.Any]]] = None,
        policy_item_monthly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataMongodbatlasBackupCompliancePolicyPolicyItemMonthly", typing.Dict[builtins.str, typing.Any]]]]] = None,
        policy_item_weekly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataMongodbatlasBackupCompliancePolicyPolicyItemWeekly", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#project_id DataMongodbatlasBackupCompliancePolicy#project_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#id DataMongodbatlasBackupCompliancePolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param on_demand_policy_item: on_demand_policy_item block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#on_demand_policy_item DataMongodbatlasBackupCompliancePolicy#on_demand_policy_item}
        :param policy_item_daily: policy_item_daily block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#policy_item_daily DataMongodbatlasBackupCompliancePolicy#policy_item_daily}
        :param policy_item_hourly: policy_item_hourly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#policy_item_hourly DataMongodbatlasBackupCompliancePolicy#policy_item_hourly}
        :param policy_item_monthly: policy_item_monthly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#policy_item_monthly DataMongodbatlasBackupCompliancePolicy#policy_item_monthly}
        :param policy_item_weekly: policy_item_weekly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#policy_item_weekly DataMongodbatlasBackupCompliancePolicy#policy_item_weekly}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(on_demand_policy_item, dict):
            on_demand_policy_item = DataMongodbatlasBackupCompliancePolicyOnDemandPolicyItem(**on_demand_policy_item)
        if isinstance(policy_item_daily, dict):
            policy_item_daily = DataMongodbatlasBackupCompliancePolicyPolicyItemDaily(**policy_item_daily)
        if isinstance(policy_item_hourly, dict):
            policy_item_hourly = DataMongodbatlasBackupCompliancePolicyPolicyItemHourly(**policy_item_hourly)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd7753e410e6e7def8c8fe7bedc3684f7483267bfb563801a71615b68ca9846f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument on_demand_policy_item", value=on_demand_policy_item, expected_type=type_hints["on_demand_policy_item"])
            check_type(argname="argument policy_item_daily", value=policy_item_daily, expected_type=type_hints["policy_item_daily"])
            check_type(argname="argument policy_item_hourly", value=policy_item_hourly, expected_type=type_hints["policy_item_hourly"])
            check_type(argname="argument policy_item_monthly", value=policy_item_monthly, expected_type=type_hints["policy_item_monthly"])
            check_type(argname="argument policy_item_weekly", value=policy_item_weekly, expected_type=type_hints["policy_item_weekly"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project_id": project_id,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if id is not None:
            self._values["id"] = id
        if on_demand_policy_item is not None:
            self._values["on_demand_policy_item"] = on_demand_policy_item
        if policy_item_daily is not None:
            self._values["policy_item_daily"] = policy_item_daily
        if policy_item_hourly is not None:
            self._values["policy_item_hourly"] = policy_item_hourly
        if policy_item_monthly is not None:
            self._values["policy_item_monthly"] = policy_item_monthly
        if policy_item_weekly is not None:
            self._values["policy_item_weekly"] = policy_item_weekly

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#project_id DataMongodbatlasBackupCompliancePolicy#project_id}.'''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#id DataMongodbatlasBackupCompliancePolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_demand_policy_item(
        self,
    ) -> typing.Optional["DataMongodbatlasBackupCompliancePolicyOnDemandPolicyItem"]:
        '''on_demand_policy_item block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#on_demand_policy_item DataMongodbatlasBackupCompliancePolicy#on_demand_policy_item}
        '''
        result = self._values.get("on_demand_policy_item")
        return typing.cast(typing.Optional["DataMongodbatlasBackupCompliancePolicyOnDemandPolicyItem"], result)

    @builtins.property
    def policy_item_daily(
        self,
    ) -> typing.Optional["DataMongodbatlasBackupCompliancePolicyPolicyItemDaily"]:
        '''policy_item_daily block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#policy_item_daily DataMongodbatlasBackupCompliancePolicy#policy_item_daily}
        '''
        result = self._values.get("policy_item_daily")
        return typing.cast(typing.Optional["DataMongodbatlasBackupCompliancePolicyPolicyItemDaily"], result)

    @builtins.property
    def policy_item_hourly(
        self,
    ) -> typing.Optional["DataMongodbatlasBackupCompliancePolicyPolicyItemHourly"]:
        '''policy_item_hourly block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#policy_item_hourly DataMongodbatlasBackupCompliancePolicy#policy_item_hourly}
        '''
        result = self._values.get("policy_item_hourly")
        return typing.cast(typing.Optional["DataMongodbatlasBackupCompliancePolicyPolicyItemHourly"], result)

    @builtins.property
    def policy_item_monthly(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataMongodbatlasBackupCompliancePolicyPolicyItemMonthly"]]]:
        '''policy_item_monthly block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#policy_item_monthly DataMongodbatlasBackupCompliancePolicy#policy_item_monthly}
        '''
        result = self._values.get("policy_item_monthly")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataMongodbatlasBackupCompliancePolicyPolicyItemMonthly"]]], result)

    @builtins.property
    def policy_item_weekly(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataMongodbatlasBackupCompliancePolicyPolicyItemWeekly"]]]:
        '''policy_item_weekly block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#policy_item_weekly DataMongodbatlasBackupCompliancePolicy#policy_item_weekly}
        '''
        result = self._values.get("policy_item_weekly")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataMongodbatlasBackupCompliancePolicyPolicyItemWeekly"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataMongodbatlasBackupCompliancePolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasBackupCompliancePolicy.DataMongodbatlasBackupCompliancePolicyOnDemandPolicyItem",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataMongodbatlasBackupCompliancePolicyOnDemandPolicyItem:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataMongodbatlasBackupCompliancePolicyOnDemandPolicyItem(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataMongodbatlasBackupCompliancePolicyOnDemandPolicyItemOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasBackupCompliancePolicy.DataMongodbatlasBackupCompliancePolicyOnDemandPolicyItemOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e80c52b311c6dd4933bde567debf3b6252133e5a71a0b63fc5e8a6e9eff8c472)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="frequencyInterval")
    def frequency_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "frequencyInterval"))

    @builtins.property
    @jsii.member(jsii_name="frequencyType")
    def frequency_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequencyType"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="retentionUnit")
    def retention_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionUnit"))

    @builtins.property
    @jsii.member(jsii_name="retentionValue")
    def retention_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionValue"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataMongodbatlasBackupCompliancePolicyOnDemandPolicyItem]:
        return typing.cast(typing.Optional[DataMongodbatlasBackupCompliancePolicyOnDemandPolicyItem], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataMongodbatlasBackupCompliancePolicyOnDemandPolicyItem],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e09ff5753bc7478aee21eac2209b1e47008bea5275503f59eda5d6725e725364)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasBackupCompliancePolicy.DataMongodbatlasBackupCompliancePolicyPolicyItemDaily",
    jsii_struct_bases=[],
    name_mapping={
        "frequency_interval": "frequencyInterval",
        "retention_unit": "retentionUnit",
        "retention_value": "retentionValue",
    },
)
class DataMongodbatlasBackupCompliancePolicyPolicyItemDaily:
    def __init__(
        self,
        *,
        frequency_interval: jsii.Number,
        retention_unit: builtins.str,
        retention_value: jsii.Number,
    ) -> None:
        '''
        :param frequency_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#frequency_interval DataMongodbatlasBackupCompliancePolicy#frequency_interval}.
        :param retention_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#retention_unit DataMongodbatlasBackupCompliancePolicy#retention_unit}.
        :param retention_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#retention_value DataMongodbatlasBackupCompliancePolicy#retention_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44a5a055accbe62329a01661094d5fa2a3184b5a1897d44766793ca8737bf45f)
            check_type(argname="argument frequency_interval", value=frequency_interval, expected_type=type_hints["frequency_interval"])
            check_type(argname="argument retention_unit", value=retention_unit, expected_type=type_hints["retention_unit"])
            check_type(argname="argument retention_value", value=retention_value, expected_type=type_hints["retention_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "frequency_interval": frequency_interval,
            "retention_unit": retention_unit,
            "retention_value": retention_value,
        }

    @builtins.property
    def frequency_interval(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#frequency_interval DataMongodbatlasBackupCompliancePolicy#frequency_interval}.'''
        result = self._values.get("frequency_interval")
        assert result is not None, "Required property 'frequency_interval' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def retention_unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#retention_unit DataMongodbatlasBackupCompliancePolicy#retention_unit}.'''
        result = self._values.get("retention_unit")
        assert result is not None, "Required property 'retention_unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention_value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#retention_value DataMongodbatlasBackupCompliancePolicy#retention_value}.'''
        result = self._values.get("retention_value")
        assert result is not None, "Required property 'retention_value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataMongodbatlasBackupCompliancePolicyPolicyItemDaily(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataMongodbatlasBackupCompliancePolicyPolicyItemDailyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasBackupCompliancePolicy.DataMongodbatlasBackupCompliancePolicyPolicyItemDailyOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be6acb166248b97590ab48578b4fbbb1f460044c43287cc1c33dbc9e14d96078)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="frequencyType")
    def frequency_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequencyType"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="frequencyIntervalInput")
    def frequency_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "frequencyIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionUnitInput")
    def retention_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retentionUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionValueInput")
    def retention_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionValueInput"))

    @builtins.property
    @jsii.member(jsii_name="frequencyInterval")
    def frequency_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "frequencyInterval"))

    @frequency_interval.setter
    def frequency_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf17368f29372bf563d323fd12ce83497271c0c5deea69783c5650e6a891c5bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequencyInterval", value)

    @builtins.property
    @jsii.member(jsii_name="retentionUnit")
    def retention_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionUnit"))

    @retention_unit.setter
    def retention_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcc464f1ac31f5c276b9470f4c7dd932ea187d5307263c20cf677e1a4d1bf410)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionUnit", value)

    @builtins.property
    @jsii.member(jsii_name="retentionValue")
    def retention_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionValue"))

    @retention_value.setter
    def retention_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffb96545e5bb5bd4af04842d3f00b3bd76ff1f0eee4b08f46653d536784eb00f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionValue", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataMongodbatlasBackupCompliancePolicyPolicyItemDaily]:
        return typing.cast(typing.Optional[DataMongodbatlasBackupCompliancePolicyPolicyItemDaily], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataMongodbatlasBackupCompliancePolicyPolicyItemDaily],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d98448042b7d8b5df07062499c727b547a2ff26a25611ff33699194d2996af4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasBackupCompliancePolicy.DataMongodbatlasBackupCompliancePolicyPolicyItemHourly",
    jsii_struct_bases=[],
    name_mapping={
        "frequency_interval": "frequencyInterval",
        "retention_unit": "retentionUnit",
        "retention_value": "retentionValue",
    },
)
class DataMongodbatlasBackupCompliancePolicyPolicyItemHourly:
    def __init__(
        self,
        *,
        frequency_interval: jsii.Number,
        retention_unit: builtins.str,
        retention_value: jsii.Number,
    ) -> None:
        '''
        :param frequency_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#frequency_interval DataMongodbatlasBackupCompliancePolicy#frequency_interval}.
        :param retention_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#retention_unit DataMongodbatlasBackupCompliancePolicy#retention_unit}.
        :param retention_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#retention_value DataMongodbatlasBackupCompliancePolicy#retention_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9ca6a42f11cded9857e456fce581f3b2b784d81c3d6b46f40ce763bea067729)
            check_type(argname="argument frequency_interval", value=frequency_interval, expected_type=type_hints["frequency_interval"])
            check_type(argname="argument retention_unit", value=retention_unit, expected_type=type_hints["retention_unit"])
            check_type(argname="argument retention_value", value=retention_value, expected_type=type_hints["retention_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "frequency_interval": frequency_interval,
            "retention_unit": retention_unit,
            "retention_value": retention_value,
        }

    @builtins.property
    def frequency_interval(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#frequency_interval DataMongodbatlasBackupCompliancePolicy#frequency_interval}.'''
        result = self._values.get("frequency_interval")
        assert result is not None, "Required property 'frequency_interval' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def retention_unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#retention_unit DataMongodbatlasBackupCompliancePolicy#retention_unit}.'''
        result = self._values.get("retention_unit")
        assert result is not None, "Required property 'retention_unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention_value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#retention_value DataMongodbatlasBackupCompliancePolicy#retention_value}.'''
        result = self._values.get("retention_value")
        assert result is not None, "Required property 'retention_value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataMongodbatlasBackupCompliancePolicyPolicyItemHourly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataMongodbatlasBackupCompliancePolicyPolicyItemHourlyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasBackupCompliancePolicy.DataMongodbatlasBackupCompliancePolicyPolicyItemHourlyOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98a3c110a0fd9feb71e0c7d27af6566aa2bb9898f16791051ab5f878c2e60b25)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="frequencyType")
    def frequency_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequencyType"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="frequencyIntervalInput")
    def frequency_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "frequencyIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionUnitInput")
    def retention_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retentionUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionValueInput")
    def retention_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionValueInput"))

    @builtins.property
    @jsii.member(jsii_name="frequencyInterval")
    def frequency_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "frequencyInterval"))

    @frequency_interval.setter
    def frequency_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbca4113efe5f838ea62d8b7f3e872cf2aadb6bf3f55a2bf5e3660bdee4a5a7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequencyInterval", value)

    @builtins.property
    @jsii.member(jsii_name="retentionUnit")
    def retention_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionUnit"))

    @retention_unit.setter
    def retention_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca4d106cf6e14bdb9b758c3c11801f408215f99e744755d3bf781ddb8f5276f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionUnit", value)

    @builtins.property
    @jsii.member(jsii_name="retentionValue")
    def retention_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionValue"))

    @retention_value.setter
    def retention_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f770a9d3f64ab9f9d342424049f07fbcc59a301cc8239ee8e8b0073a2ff8b0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionValue", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataMongodbatlasBackupCompliancePolicyPolicyItemHourly]:
        return typing.cast(typing.Optional[DataMongodbatlasBackupCompliancePolicyPolicyItemHourly], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataMongodbatlasBackupCompliancePolicyPolicyItemHourly],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5322a85df88083f1f51e3ca587f4bcb2d88cbc1e127ef424725059a942e365a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasBackupCompliancePolicy.DataMongodbatlasBackupCompliancePolicyPolicyItemMonthly",
    jsii_struct_bases=[],
    name_mapping={
        "frequency_interval": "frequencyInterval",
        "retention_unit": "retentionUnit",
        "retention_value": "retentionValue",
    },
)
class DataMongodbatlasBackupCompliancePolicyPolicyItemMonthly:
    def __init__(
        self,
        *,
        frequency_interval: jsii.Number,
        retention_unit: builtins.str,
        retention_value: jsii.Number,
    ) -> None:
        '''
        :param frequency_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#frequency_interval DataMongodbatlasBackupCompliancePolicy#frequency_interval}.
        :param retention_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#retention_unit DataMongodbatlasBackupCompliancePolicy#retention_unit}.
        :param retention_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#retention_value DataMongodbatlasBackupCompliancePolicy#retention_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1a006a2fce87394b883e3c120bb771eb39db2fd2882d193ee8ef3c3c96099fc)
            check_type(argname="argument frequency_interval", value=frequency_interval, expected_type=type_hints["frequency_interval"])
            check_type(argname="argument retention_unit", value=retention_unit, expected_type=type_hints["retention_unit"])
            check_type(argname="argument retention_value", value=retention_value, expected_type=type_hints["retention_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "frequency_interval": frequency_interval,
            "retention_unit": retention_unit,
            "retention_value": retention_value,
        }

    @builtins.property
    def frequency_interval(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#frequency_interval DataMongodbatlasBackupCompliancePolicy#frequency_interval}.'''
        result = self._values.get("frequency_interval")
        assert result is not None, "Required property 'frequency_interval' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def retention_unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#retention_unit DataMongodbatlasBackupCompliancePolicy#retention_unit}.'''
        result = self._values.get("retention_unit")
        assert result is not None, "Required property 'retention_unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention_value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#retention_value DataMongodbatlasBackupCompliancePolicy#retention_value}.'''
        result = self._values.get("retention_value")
        assert result is not None, "Required property 'retention_value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataMongodbatlasBackupCompliancePolicyPolicyItemMonthly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataMongodbatlasBackupCompliancePolicyPolicyItemMonthlyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasBackupCompliancePolicy.DataMongodbatlasBackupCompliancePolicyPolicyItemMonthlyList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e520199b0de31284ab67b8d2f7681c94e685cb2f46097ae0b66bfd5ba65e692c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataMongodbatlasBackupCompliancePolicyPolicyItemMonthlyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85758687c8a571239c68b3c90cbdd22a8b0f92712b2a58602e2f745bcc6a5ea8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataMongodbatlasBackupCompliancePolicyPolicyItemMonthlyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b798dedd9e95d0db84fe2669348fe17a40dc5f557c62ff8f278b52d982af3bed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f72b4cec34a9a113ac73a8507a9f3c304b9ce3b5436b3d400389e2a25a51b09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7e1464f467dfcc8665b44e11f9436e3342216353d1771fd0575297d07861bfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataMongodbatlasBackupCompliancePolicyPolicyItemMonthly]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataMongodbatlasBackupCompliancePolicyPolicyItemMonthly]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataMongodbatlasBackupCompliancePolicyPolicyItemMonthly]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a14d35d740f105551faaef3ee490aaabc38bc0b91ad3c66f8d9949d28c01613d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataMongodbatlasBackupCompliancePolicyPolicyItemMonthlyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasBackupCompliancePolicy.DataMongodbatlasBackupCompliancePolicyPolicyItemMonthlyOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73fc9b4de20e25ecd53115e748dc1db380e82d11891c7f9f4dc9d5b4ba04d73a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="frequencyType")
    def frequency_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequencyType"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="frequencyIntervalInput")
    def frequency_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "frequencyIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionUnitInput")
    def retention_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retentionUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionValueInput")
    def retention_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionValueInput"))

    @builtins.property
    @jsii.member(jsii_name="frequencyInterval")
    def frequency_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "frequencyInterval"))

    @frequency_interval.setter
    def frequency_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d647383209ac4f748261bad8fc79318a7ca56890fb0630bbb6ec1229ec219ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequencyInterval", value)

    @builtins.property
    @jsii.member(jsii_name="retentionUnit")
    def retention_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionUnit"))

    @retention_unit.setter
    def retention_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a8dcb78d6c4a2c5ef86baeb741696f9480a97edd44c733dddf2166eefd135f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionUnit", value)

    @builtins.property
    @jsii.member(jsii_name="retentionValue")
    def retention_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionValue"))

    @retention_value.setter
    def retention_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a8581b12b52dd25c0cc3f6e1a93562f90b2c418175177df52ecbeee8b13ef5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionValue", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataMongodbatlasBackupCompliancePolicyPolicyItemMonthly]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataMongodbatlasBackupCompliancePolicyPolicyItemMonthly]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataMongodbatlasBackupCompliancePolicyPolicyItemMonthly]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1237fa61874107c205ce70532b7ff875d233aa56727caea61a9752a083a54de4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasBackupCompliancePolicy.DataMongodbatlasBackupCompliancePolicyPolicyItemWeekly",
    jsii_struct_bases=[],
    name_mapping={
        "frequency_interval": "frequencyInterval",
        "retention_unit": "retentionUnit",
        "retention_value": "retentionValue",
    },
)
class DataMongodbatlasBackupCompliancePolicyPolicyItemWeekly:
    def __init__(
        self,
        *,
        frequency_interval: jsii.Number,
        retention_unit: builtins.str,
        retention_value: jsii.Number,
    ) -> None:
        '''
        :param frequency_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#frequency_interval DataMongodbatlasBackupCompliancePolicy#frequency_interval}.
        :param retention_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#retention_unit DataMongodbatlasBackupCompliancePolicy#retention_unit}.
        :param retention_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#retention_value DataMongodbatlasBackupCompliancePolicy#retention_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9784bc1c85298dd2e0fbb3b52346a1345366e84d6b7d0c06fa37d33779020f1)
            check_type(argname="argument frequency_interval", value=frequency_interval, expected_type=type_hints["frequency_interval"])
            check_type(argname="argument retention_unit", value=retention_unit, expected_type=type_hints["retention_unit"])
            check_type(argname="argument retention_value", value=retention_value, expected_type=type_hints["retention_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "frequency_interval": frequency_interval,
            "retention_unit": retention_unit,
            "retention_value": retention_value,
        }

    @builtins.property
    def frequency_interval(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#frequency_interval DataMongodbatlasBackupCompliancePolicy#frequency_interval}.'''
        result = self._values.get("frequency_interval")
        assert result is not None, "Required property 'frequency_interval' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def retention_unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#retention_unit DataMongodbatlasBackupCompliancePolicy#retention_unit}.'''
        result = self._values.get("retention_unit")
        assert result is not None, "Required property 'retention_unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention_value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.12.2/docs/data-sources/backup_compliance_policy#retention_value DataMongodbatlasBackupCompliancePolicy#retention_value}.'''
        result = self._values.get("retention_value")
        assert result is not None, "Required property 'retention_value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataMongodbatlasBackupCompliancePolicyPolicyItemWeekly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataMongodbatlasBackupCompliancePolicyPolicyItemWeeklyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasBackupCompliancePolicy.DataMongodbatlasBackupCompliancePolicyPolicyItemWeeklyList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e55fa4a2a9b39ed427670d0d6b1743228b9c89a4fa1f6a037564c9c747e30c6d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataMongodbatlasBackupCompliancePolicyPolicyItemWeeklyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bde5a60b8336031769512f1aea04531099384a84cb1a3daa7ae41bfe2539d24d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataMongodbatlasBackupCompliancePolicyPolicyItemWeeklyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f7326cccae053366ecb3797220f6e48a90a6a65e336e4a7a8f1bf265fa9f074)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__247cd7dfe140eb598b2b1d682f8dfae48ccaecacadfc93f090e1fa892f010ac0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7142fb275807a9f590d069a0fbb9c6daf07ae42bb554ee3352bd97af3f83dfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataMongodbatlasBackupCompliancePolicyPolicyItemWeekly]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataMongodbatlasBackupCompliancePolicyPolicyItemWeekly]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataMongodbatlasBackupCompliancePolicyPolicyItemWeekly]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48f9317afc179126ac44ccc99ac6102ac61717db517a25613140350a6e043ffa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataMongodbatlasBackupCompliancePolicyPolicyItemWeeklyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasBackupCompliancePolicy.DataMongodbatlasBackupCompliancePolicyPolicyItemWeeklyOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2c7d7ef6b45c627ed1cdac7002e86cb65a0520721e3cf7e0c3d4c57eda67b40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="frequencyType")
    def frequency_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequencyType"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="frequencyIntervalInput")
    def frequency_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "frequencyIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionUnitInput")
    def retention_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retentionUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionValueInput")
    def retention_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionValueInput"))

    @builtins.property
    @jsii.member(jsii_name="frequencyInterval")
    def frequency_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "frequencyInterval"))

    @frequency_interval.setter
    def frequency_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f8b40675c1fd15bedd8561d316be146eee3d6dcc117e46962922c77cc856ad4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequencyInterval", value)

    @builtins.property
    @jsii.member(jsii_name="retentionUnit")
    def retention_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionUnit"))

    @retention_unit.setter
    def retention_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecd4994a20a2e65561353262c3aee7ca6b294e0da47a8fce8cd1db60ee28e2e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionUnit", value)

    @builtins.property
    @jsii.member(jsii_name="retentionValue")
    def retention_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionValue"))

    @retention_value.setter
    def retention_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5be5414e4300f5a9e7131f8970d16d6f4f408af0c8415378735a6d34e384109a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionValue", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataMongodbatlasBackupCompliancePolicyPolicyItemWeekly]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataMongodbatlasBackupCompliancePolicyPolicyItemWeekly]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataMongodbatlasBackupCompliancePolicyPolicyItemWeekly]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3dc0327e00125ffec5f7e6c43865511e8f18e67a5554a12c1f12ab016db0bbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataMongodbatlasBackupCompliancePolicy",
    "DataMongodbatlasBackupCompliancePolicyConfig",
    "DataMongodbatlasBackupCompliancePolicyOnDemandPolicyItem",
    "DataMongodbatlasBackupCompliancePolicyOnDemandPolicyItemOutputReference",
    "DataMongodbatlasBackupCompliancePolicyPolicyItemDaily",
    "DataMongodbatlasBackupCompliancePolicyPolicyItemDailyOutputReference",
    "DataMongodbatlasBackupCompliancePolicyPolicyItemHourly",
    "DataMongodbatlasBackupCompliancePolicyPolicyItemHourlyOutputReference",
    "DataMongodbatlasBackupCompliancePolicyPolicyItemMonthly",
    "DataMongodbatlasBackupCompliancePolicyPolicyItemMonthlyList",
    "DataMongodbatlasBackupCompliancePolicyPolicyItemMonthlyOutputReference",
    "DataMongodbatlasBackupCompliancePolicyPolicyItemWeekly",
    "DataMongodbatlasBackupCompliancePolicyPolicyItemWeeklyList",
    "DataMongodbatlasBackupCompliancePolicyPolicyItemWeeklyOutputReference",
]

publication.publish()

def _typecheckingstub__204e5e646fda1cf3ca8ca6909f19fdbad271c335c0812f2957771944799e900d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    project_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    on_demand_policy_item: typing.Optional[typing.Union[DataMongodbatlasBackupCompliancePolicyOnDemandPolicyItem, typing.Dict[builtins.str, typing.Any]]] = None,
    policy_item_daily: typing.Optional[typing.Union[DataMongodbatlasBackupCompliancePolicyPolicyItemDaily, typing.Dict[builtins.str, typing.Any]]] = None,
    policy_item_hourly: typing.Optional[typing.Union[DataMongodbatlasBackupCompliancePolicyPolicyItemHourly, typing.Dict[builtins.str, typing.Any]]] = None,
    policy_item_monthly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataMongodbatlasBackupCompliancePolicyPolicyItemMonthly, typing.Dict[builtins.str, typing.Any]]]]] = None,
    policy_item_weekly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataMongodbatlasBackupCompliancePolicyPolicyItemWeekly, typing.Dict[builtins.str, typing.Any]]]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c5f0c941a284e1eec2ecac970194e8763354e822cba406c9a5e1d327ef14c2(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a3578d669d9123f43a93e5eaaab59a7fbc137310a75deb2e964175c96e84ae(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataMongodbatlasBackupCompliancePolicyPolicyItemMonthly, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80b4d296f6e9c037af2ac095ad1ce1b26dd9f48af6a11a6d29d5bf101422d52f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataMongodbatlasBackupCompliancePolicyPolicyItemWeekly, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8885b99871b2e778892a82c023abfda802b948130efbf2d9db902eca04b9b51f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c6aca2ecf285e25e7b8ff1faafd0814be7c3a3736d1d1b99d11bf69d83b0fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd7753e410e6e7def8c8fe7bedc3684f7483267bfb563801a71615b68ca9846f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    on_demand_policy_item: typing.Optional[typing.Union[DataMongodbatlasBackupCompliancePolicyOnDemandPolicyItem, typing.Dict[builtins.str, typing.Any]]] = None,
    policy_item_daily: typing.Optional[typing.Union[DataMongodbatlasBackupCompliancePolicyPolicyItemDaily, typing.Dict[builtins.str, typing.Any]]] = None,
    policy_item_hourly: typing.Optional[typing.Union[DataMongodbatlasBackupCompliancePolicyPolicyItemHourly, typing.Dict[builtins.str, typing.Any]]] = None,
    policy_item_monthly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataMongodbatlasBackupCompliancePolicyPolicyItemMonthly, typing.Dict[builtins.str, typing.Any]]]]] = None,
    policy_item_weekly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataMongodbatlasBackupCompliancePolicyPolicyItemWeekly, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e80c52b311c6dd4933bde567debf3b6252133e5a71a0b63fc5e8a6e9eff8c472(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e09ff5753bc7478aee21eac2209b1e47008bea5275503f59eda5d6725e725364(
    value: typing.Optional[DataMongodbatlasBackupCompliancePolicyOnDemandPolicyItem],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a5a055accbe62329a01661094d5fa2a3184b5a1897d44766793ca8737bf45f(
    *,
    frequency_interval: jsii.Number,
    retention_unit: builtins.str,
    retention_value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be6acb166248b97590ab48578b4fbbb1f460044c43287cc1c33dbc9e14d96078(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf17368f29372bf563d323fd12ce83497271c0c5deea69783c5650e6a891c5bf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc464f1ac31f5c276b9470f4c7dd932ea187d5307263c20cf677e1a4d1bf410(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffb96545e5bb5bd4af04842d3f00b3bd76ff1f0eee4b08f46653d536784eb00f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d98448042b7d8b5df07062499c727b547a2ff26a25611ff33699194d2996af4c(
    value: typing.Optional[DataMongodbatlasBackupCompliancePolicyPolicyItemDaily],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9ca6a42f11cded9857e456fce581f3b2b784d81c3d6b46f40ce763bea067729(
    *,
    frequency_interval: jsii.Number,
    retention_unit: builtins.str,
    retention_value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98a3c110a0fd9feb71e0c7d27af6566aa2bb9898f16791051ab5f878c2e60b25(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbca4113efe5f838ea62d8b7f3e872cf2aadb6bf3f55a2bf5e3660bdee4a5a7b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca4d106cf6e14bdb9b758c3c11801f408215f99e744755d3bf781ddb8f5276f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f770a9d3f64ab9f9d342424049f07fbcc59a301cc8239ee8e8b0073a2ff8b0c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5322a85df88083f1f51e3ca587f4bcb2d88cbc1e127ef424725059a942e365a1(
    value: typing.Optional[DataMongodbatlasBackupCompliancePolicyPolicyItemHourly],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1a006a2fce87394b883e3c120bb771eb39db2fd2882d193ee8ef3c3c96099fc(
    *,
    frequency_interval: jsii.Number,
    retention_unit: builtins.str,
    retention_value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e520199b0de31284ab67b8d2f7681c94e685cb2f46097ae0b66bfd5ba65e692c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85758687c8a571239c68b3c90cbdd22a8b0f92712b2a58602e2f745bcc6a5ea8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b798dedd9e95d0db84fe2669348fe17a40dc5f557c62ff8f278b52d982af3bed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f72b4cec34a9a113ac73a8507a9f3c304b9ce3b5436b3d400389e2a25a51b09(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7e1464f467dfcc8665b44e11f9436e3342216353d1771fd0575297d07861bfc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a14d35d740f105551faaef3ee490aaabc38bc0b91ad3c66f8d9949d28c01613d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataMongodbatlasBackupCompliancePolicyPolicyItemMonthly]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73fc9b4de20e25ecd53115e748dc1db380e82d11891c7f9f4dc9d5b4ba04d73a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d647383209ac4f748261bad8fc79318a7ca56890fb0630bbb6ec1229ec219ad(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a8dcb78d6c4a2c5ef86baeb741696f9480a97edd44c733dddf2166eefd135f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a8581b12b52dd25c0cc3f6e1a93562f90b2c418175177df52ecbeee8b13ef5d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1237fa61874107c205ce70532b7ff875d233aa56727caea61a9752a083a54de4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataMongodbatlasBackupCompliancePolicyPolicyItemMonthly]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9784bc1c85298dd2e0fbb3b52346a1345366e84d6b7d0c06fa37d33779020f1(
    *,
    frequency_interval: jsii.Number,
    retention_unit: builtins.str,
    retention_value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55fa4a2a9b39ed427670d0d6b1743228b9c89a4fa1f6a037564c9c747e30c6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bde5a60b8336031769512f1aea04531099384a84cb1a3daa7ae41bfe2539d24d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f7326cccae053366ecb3797220f6e48a90a6a65e336e4a7a8f1bf265fa9f074(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__247cd7dfe140eb598b2b1d682f8dfae48ccaecacadfc93f090e1fa892f010ac0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7142fb275807a9f590d069a0fbb9c6daf07ae42bb554ee3352bd97af3f83dfc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48f9317afc179126ac44ccc99ac6102ac61717db517a25613140350a6e043ffa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataMongodbatlasBackupCompliancePolicyPolicyItemWeekly]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2c7d7ef6b45c627ed1cdac7002e86cb65a0520721e3cf7e0c3d4c57eda67b40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f8b40675c1fd15bedd8561d316be146eee3d6dcc117e46962922c77cc856ad4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecd4994a20a2e65561353262c3aee7ca6b294e0da47a8fce8cd1db60ee28e2e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be5414e4300f5a9e7131f8970d16d6f4f408af0c8415378735a6d34e384109a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3dc0327e00125ffec5f7e6c43865511e8f18e67a5554a12c1f12ab016db0bbd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataMongodbatlasBackupCompliancePolicyPolicyItemWeekly]],
) -> None:
    """Type checking stubs"""
    pass
