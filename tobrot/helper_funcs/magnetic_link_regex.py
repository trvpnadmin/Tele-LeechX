#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Shrimadhav U K
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

import re


MAGNETIC_LINK_REGEX = r"magnet\:\?xt\=urn\:btih\:([A-F\d]+)"


def extract_info_hash_from_ml(magnetic_link):
    ml_re_match = re.search(MAGNETIC_LINK_REGEX, magnetic_link)
    if ml_re_match is not None:
        return ml_re_match.group(1)
