# TimeP
Set of datetime tools in Python, similar to Joda Time or Calendar

This is a library that provides convenient operations on datetime objects in Python.

## Example
```
a = Datum.parse('1560718800')
a.add_months(1)
a.add_days(1)
a.add_hours(1)
a.add_minutes(40)
a.substract_days(1)
print('[√]: ', a)
print('[√]: ', a.epoch_miliseconds)

a = Datum.parse('2019-07-17')
for lines in a.range(Datum.parse('2019-06-17').value).split_by('hour'):
    print('[√]: ', lines)

```
```
[√]:  2019-07-17 01:40:00
[√]:  1563316800000
```