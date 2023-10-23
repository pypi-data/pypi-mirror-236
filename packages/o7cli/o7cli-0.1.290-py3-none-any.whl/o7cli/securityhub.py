#************************************************************************
# Copyright 2023 O7 Conseils inc (Philippe Gosselin)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#************************************************************************
"""Module allows to view and access Security Hub resources"""


#--------------------------------
#
#--------------------------------
import pprint
import logging
import datetime
import pandas as pd


from o7util.table import TableParam, ColumnParam, Table
import o7util.menu as o7m
import o7util.terminal as o7t


import o7lib.aws.base


logger=logging.getLogger(__name__)



#*************************************************
#
#*************************************************
class SecurityHub(o7lib.aws.base.Base):
    """Class for SecurityHub """

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html

    #*************************************************
    #
    #*************************************************
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = self.session.client('securityhub')



        self.df_standards : pd.DataFrame = None
        self.dfs_controls : dict[str, pd.DataFrame] = {}
        self.df_findings : pd.DataFrame = None

        # self.description : dict = None
        # self.enabled_services : list = []
        # self.accounts : list = []
        # self.policies : list = None


    #*************************************************
    #
    #*************************************************
    def load_standards(self):
        """Load all standards"""

        logger.info('load_standards')

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/client/describe_standards.html
        paginator = self.client.get_paginator('describe_standards')

        standards = []

        for page in paginator.paginate():
            standards.extend(page.get('Standards', []))

        self.df_standards = pd.DataFrame(standards)
        self.df_standards.set_index('StandardsArn', inplace=True)

        logger.info(f'load_standards: Number of standards found {len(standards)}')
        return self

    #*************************************************
    #
    #*************************************************
    def load_enabled_standards(self):
        """Load enabled standards"""

        if self.df_standards is None:
            self.load_standards()

        logger.info('load_enabled_standards')

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/client/get_enabled_standards.html
        paginator = self.client.get_paginator('get_enabled_standards')
        standards = []

        for page in paginator.paginate():
            standards.extend(page.get('StandardsSubscriptions', []))

        # self.df_standards = pd.DataFrame(standards)
        logger.info(f'load_enabled_standards: Number of standards found {len(standards)}')

        df = pd.DataFrame(standards).set_index('StandardsArn')
        self.df_standards = self.df_standards.join(df, how='left', lsuffix='_left', rsuffix='_right')

        return self

    #*************************************************
    #
    #*************************************************
    def load_standard_controls(self):
        """Load all controles for each standards"""

        if self.df_standards is None:
            self.load_enabled_standards()

        df_ready = self.df_standards[self.df_standards['StandardsStatus'] == 'READY']

        for index, row in df_ready.iterrows():

            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/client/describe_standards_controls.html
            paginator = self.client.get_paginator('describe_standards_controls')
            controls = []

            for page in paginator.paginate(StandardsSubscriptionArn=row['StandardsSubscriptionArn']):
                controls.extend(page.get('Controls', []))

            df_controls = pd.DataFrame(controls)
            df_controls['ControlStatusUpdatedAt'] = df_controls['ControlStatusUpdatedAt'].dt.tz_localize(None)

            self.dfs_controls[index] = df_controls

            self.df_standards.loc[index, 'ControlsCount'] = len(df_controls.index)
            self.df_standards.loc[index, 'ControlsDisabled'] = len(df_controls[df_controls['ControlStatus'] == 'DISABLED'].index)
            self.df_standards.loc[index, 'ControlsPass'] = 'TBD'
            self.df_standards.loc[index, 'ControlsFailed'] = 'TBD'
            self.df_standards.loc[index, 'Score'] = 'TBD'


    #*************************************************
    #
    #*************************************************
    def load_findings(self, standard_arn : str = None):
        """Load findings"""

        logger.info(f'load_findings standard_arn={standard_arn}')


        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/client/get_findings.html
        paginator = self.client.get_paginator('get_findings')

        findings = []
        filters = {
            'RecordState' : [{
                'Comparison': 'EQUALS',
                'Value': 'ACTIVE'

            }]
        }
        if standard_arn is not None:
            filters['ComplianceStandardsArn'] = [{
                'Comparison': 'EQUALS',
                'Value': standard_arn.split(':')[-1]
            }]

        for page in paginator.paginate(Filters = filters, MaxResults=100):
            findings.extend(page.get('Findings', []))


        df = pd.DataFrame(findings)

        df['StandardsArn'] = df['ProductFields'].apply(lambda x: x.get('StandardsArn', x.get('StandardsGuideArn',None)))
        df['ControlId'] = df['ProductFields'].apply(lambda x: x.get('ControlId', x.get('RuleId',None)))
        df['Status'] = df['Compliance'].apply(lambda x: x.get('Status', None) if isinstance(x,dict) else x)
        df['SeverityL'] = df['Severity'].apply(lambda x: x.get('Label', None))
        df['SeverityN'] = df['Severity'].apply(lambda x: x.get('Normalized', None))


        self.df_findings = df
        logger.info(f'df_findings: Number of standards found {len(self.df_findings.index)}')
        return self


    #*************************************************
    #
    #*************************************************
    def update_findings(self):

        self.load_findings()

        self.df_findings['passed'] = the_obj.df_findings['Status'] == 'PASSED'

        df = self.df_findings[self.df_findings['ProductName'] == 'Security Hub']

        # Compile by Controls
        gb_ctrl = df.groupby(['StandardsArn', 'ControlId'])
        df_per_control = pd.DataFrame(index=gb_ctrl.groups.keys(),)
        df_per_control['f_count'] = gb_ctrl['passed'].count()
        df_per_control['f_passed'] = gb_ctrl['passed'].sum()
        df_per_control['passed'] = df_per_control['f_count'] == df_per_control['f_passed']

        # Compile by Standards
        gb_std = df.groupby(['StandardsArn'])
        df_per_standard = pd.DataFrame(index=gb_std.groups.keys(),)
        df_per_standard['f_count'] = gb_std['passed'].count()
        df_per_standard['f_passed'] = gb_std['passed'].sum()
        df_per_standard['f_score'] = df_per_standard['f_count'] == df_per_standard['f_passed']

        df_per_control = df_per_control.reset_index(drop=False)
        gb_std = df_per_control.groupby(['level_0'])
        df_per_standard['c_count'] = gb_std['passed'].count()
        df_per_standard['c_passed'] = gb_std['passed'].sum()
        df_per_standard['c_fail'] = df_per_standard['c_count'] - df_per_standard['c_passed']
        df_per_standard['c_score'] = df_per_standard['c_passed'] / df_per_standard['c_count']

        print(df_per_standard)





    #*************************************************
    #
    #*************************************************
    def display_overview(self):
        """Display Security Hub"""

        if len(self.dfs_controls.keys()) == 0:
            self.load_standard_controls()

        print('Available Standards')
        params = TableParam(
            columns = [
                ColumnParam(title = 'id',          type = 'i',    min_width = 4  ),
                ColumnParam(title = 'Name',     type = 'str',  data_col = 'Name'),
                ColumnParam(title = 'Status',     type = 'str',  data_col = 'StandardsStatus'),
                ColumnParam(title = 'Controls',     type = 'int',  data_col = 'ControlsCount'),
                ColumnParam(title = 'Disabled',     type = 'int',  data_col = 'ControlsDisabled')
            ]
        )
        Table(params, self.df_standards.to_dict(orient='records')).print()
        print()




    #*************************************************
    #
    #*************************************************
    def to_excel(self):
        """Save to Excel"""

        filename= f"aws-securityhub-{datetime.datetime.now().isoformat()[0:19].replace(':','-')}.xlsx"
        with pd.ExcelWriter(filename) as writer: # pylint: disable=abstract-class-instantiated

            df_parameters = pd.DataFrame([
                {'Parameter' : 'Date', 'Value' : datetime.datetime.now().isoformat()}
            ])
            df_parameters.to_excel(writer, sheet_name="Parameters")

            self.df_standards.to_excel(writer, sheet_name="Standards")

            count = 0
            for key, df in self.dfs_controls.items():
                count += 1
                df.to_excel(writer, sheet_name=f"Controls-{count}")

            if self.df_findings is not None:
                self.df_findings.to_excel(writer, sheet_name="Findings")



        print(f"Security Hub saved in file: {filename}")


    #*************************************************
    #
    #*************************************************
    def from_excel(self, filename):
        """Save to Excel"""

        print(f"Loading file: {filename}")
        self.df_standards = pd.read_excel(filename, sheet_name='Standards')
        self.df_findings = pd.read_excel(filename, sheet_name='Findings')

    #*************************************************
    #
    #*************************************************
    def menu_overview(self):
        """Organization menu"""


        obj = o7m.Menu(exit_option = 'b', title='Secutity Hub Overview', title_extra=self.session_info(), compact=False)

        obj.add_option(o7m.Option(
            key='f',
            name='Load Findings',
            short='Findings',
            callback=self.update_findings
        ))


        obj.display_callback = self.display_overview
        obj.loop()

        return self

#*************************************************
#
#*************************************************
def menu(**kwargs):
    """Run Main Menu"""
    SecurityHub(**kwargs).menu_overview()






#*************************************************
#
#*************************************************
if __name__ == "__main__":

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', o7t.get_width())
    pd.set_option('display.max_colwidth',  20)

    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)-5.5s] [%(name)s] %(message)s"
    )

    the_obj = SecurityHub()

    the_obj.menu_overview()

    exit(0)

    # the_obj.load_enabled_standards()
    # the_obj.load_standard_controls()
    # print(the_obj.df_standards)
    # # print(the_obj.dfs_controls)

    # the_obj.load_findings()
    # print(the_obj.df_findings.info())
    # the_obj.to_excel()

    # exit(0)
    the_obj.from_excel('aws-securityhub-2023-10-01T23-21-16.xlsx')


    the_obj.df_findings['passed'] = the_obj.df_findings['Status'] == 'PASSED'

    # group by 'StandardsArn', 'ControlId', give me the total count, and the sum of passed

    df = the_obj.df_findings[the_obj.df_findings['ProductName'] == 'Security Hub']

    gb = df.groupby(['StandardsArn', 'ControlId'])
    df_per_control = pd.DataFrame(index=gb.groups.keys(),)
    df_per_control['f_count'] = gb['passed'].count()
    df_per_control['f_passed'] = gb['passed'].sum()
    df_per_control['passed'] = df_per_control['f_count'] == df_per_control['f_passed']

    print(df_per_control)

    gb = df.groupby(['StandardsArn'])
    df_per_standard = pd.DataFrame(index=gb.groups.keys(),)
    df_per_standard['f_count'] = gb['passed'].count()
    df_per_standard['f_passed'] = gb['passed'].sum()
    df_per_standard['passed'] = df_per_standard['f_count'] == df_per_standard['f_passed']

    df_per_control = df_per_control.reset_index(drop=False)
    gb = df_per_control.groupby(['level_0'])
    df_per_standard['c_count'] = gb['passed'].count()
    df_per_standard['c_passed'] = gb['passed'].sum()
    df_per_standard['score'] = df_per_standard['c_passed'] / df_per_standard['c_count']


    print(df_per_standard)

    finding_total = df['passed'].count()
    finding_passed = df['passed'].sum()

    control_total = df_per_control['passed'].count()
    control_passed = df_per_control['passed'].sum()

    security_score = control_passed / control_total
    print(f'Security Score: {security_score:.2%}')



    # # print(the_obj.dfs_controls)

    # for key, df in the_obj.dfs_controls.items():
    #     print(key)
    #     print(df.iloc[0])

    # 'arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.2.0'
    # 'arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.2.0'
    # the_resp = the_obj.client.get_findings(
    #     Filters={
    #         'ComplianceAssociatedStandardsId': [{
    #             'Comparison': 'EQUALS',
    #             'Value':'ruleset/cis-aws-foundations-benchmark/v/1.2.0'
    #         }]
    #     }
    # )

    # the_resp = the_obj.client.list_standards_control_associations(SecurityControlId='ACM.1')


    # print('----------------------------------------------------')

    # the_resp = the_obj.client.get_findings(
    #     Filters={
    #         'ComplianceSecurityControlId': [{
    #             'Comparison': 'EQUALS',
    #             'Value': 'ACM.1'
    #         }]
    #     }
    # )

    # pprint.pprint(the_resp)
    # the_findings = the_resp.get('Findings', [])
    # print(len(the_findings))



    # the_obj.menu_overview()



