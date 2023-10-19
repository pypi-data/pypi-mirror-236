.. _using:

=============
Auto Cleaning
=============

By default buckaroo aggresively treis to type data and clean it up.

Better typing
-------------
What do I mean by cleaning types?  By default if an integer column contains a single missing value, pandas will use the ``float64`` dtype to represent that value as a NaN.  The autotyping functionality instead casts that as ``Int64`` a new type in pandas that allows ``NA`` values in Int columns.  Work is also done to constrain types to their narrowest, so if an int value is between 0 and 255, autotyping will cast that to `UInt8` using a single byte instead of 8 for a float64 or int64.


Heuristic cleaning
------------------
The autocleaning tool also heursitically removes errant mistyped values from column.  If a column is primarily Ints with a single string, that string is stripped so the column can be treated as numeric.

	
