from unittest import TestCase

from app.wrapper_kafka.data_helpers import get_case_number


class TestDataHelpers(TestCase):

    def setUp(self) -> None:
        self.case_num = '01234567'
        self.s3_bundle_path = (f'ticket/{self.case_num}/'
                               f'upload/201-01-01T123456_VeeamBackupLogs.zip')
        self.sftp_over_s3_bundle_path = (f'ticket/ftp{self.case_num}/'
                                         f'upload/201-01-01T123456_VeeamBackupLogs.zip')
        self.sftp_bundle_path = (f'sftp://supportftp1.veeam.com/'
                                 f'ftp{self.case_num}/2017-01-01T123456_VeeamBackupLogs.zip')

        self.all_bundle_sources = [
            self.s3_bundle_path,
            self.sftp_bundle_path,
            self.sftp_over_s3_bundle_path
        ]

    def test_get_case_number(self):
        for bundle_path in self.all_bundle_sources:
            case_num = get_case_number(bundle_path=bundle_path)
            self.assertEqual(case_num, self.case_num)
