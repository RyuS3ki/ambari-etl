from __future__ import print_function

import sys
from operator import add
from pyspark import SparkContext
#from pyspark.sql import SparkSession

def GLibMapper(s):

    line = s.strip()

    check_GLib = 'GLib-CRITICAL' in line

    if check_GLib:
        list=line.split()
        month=list[0]
        day=list[1]
        host=list[3]
        #glib_date= day + '/' + month + "->" + host
        # Uid filename host s_date sid snoopy_pid tty cwd cmd
        #return '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (uid, host, s_date, hour, sid, snoopy_pid, cwd, filename, cmd)
        return '%s' % (host)


#def GLibHostReducer(data_acum, data):
#    data = yield s.rstrip().split('\t', 1)


def main(argv):

    sc = SparkContext("local", "GLib Error Host Count")

    data = sc.textFile("/user/etl/rejimene/*")

    mapped = data.map(GLibMapper)

    # count occurrences
    count = mapped.countByValue()

    # sort by num of occurrences
    sort_by_value = sorted(count.iteritems(),key=lambda (k,v): v,reverse=False)

    for item in sort_by_value:
        print('%s %d' % (item[0],item[1]))


if __name__ == "__main__":
    main(sys.argv[1:])
