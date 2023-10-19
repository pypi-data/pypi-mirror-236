# 🔧 utilita
[![PyPI version](https://badge.fury.io/py/utilita.svg)](https://badge.fury.io/py/utilita)
[![Build Status](https://travis-ci.com/json2d/utilita.svg?branch=master)](https://travis-ci.com/json2d/utilita) [![Coverage Status](https://coveralls.io/repos/github/json2d/utilita/badge.svg?branch=master)](https://coveralls.io/github/json2d/utilita?branch=master)

a utility library

## Quick install
```bash
pip install utilita
```

## Basic usage

[decent pitch]. Let's dive in.

Out-of-the-box you get some stuff you can do with utilita:

```py
import datetime
from utilita import date_fns

w52d7 = datetime.date(2020,12,27)
w53d1 = datetime.date(2020,12,28)

date_fns.is_in_leap_week(w52d7) # => False
date_fns.is_in_leap_week(w53d1) # => True

date_fns.days_since_same_date_last_year(w52d7) # => 364 (days in non-leep-week years)
date_fns.days_since_same_date_last_year(w53d1) # => 371 (days in leep-week years)

```

more about ISO 8601 leap weeks: https://en.wikipedia.org/wiki/ISO_week_date
