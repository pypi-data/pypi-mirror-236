# coding: utf-8

import re
from typing import Optional

case_number_re = re.compile(r"(.+?ftp|.+?)\D(?P<casenum>\d{7,8})\D")


def get_case_number(bundle_path: str) -> Optional[str]:
    res = re.match(case_number_re, bundle_path)
    if res:
        return res.group("casenum")
    return None
