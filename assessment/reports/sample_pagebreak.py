import sys

from PollyReports import *
from reportlab.pdfgen.canvas import Canvas
from testdata import data


def pagecount(obj):
    sys.stdout.write("%d " % obj.parent.report.pagenumber)
    sys.stdout.flush()


rpt = Report(data)
rpt.detailband = Band([
    Element((36, 0), ("Helvetica", 11), key="name"),
    Element((400, 0), ("Helvetica", 11), key="amount"),
])
rpt.pageheader = Band([
    Element((36, 0), ("Times-Bold", 20), text="Page Header",
            onrender=pagecount),
    Element((36, 24), ("Helvetica", 12), text="Name"),
    Element((400, 24), ("Helvetica", 12), text="Amount", ),
    Rule((36, 42), 7.5 * 72, thickness=2),
])
rpt.pagefooter = Band([
    Element((72 * 8, 0), ("Times-Bold", 20), text="Page Footer", ),
    Element((36, 16), ("Helvetica-Bold", 12), sysvar="pagenumber", format=lambda x: "Page %d" % x),
])
rpt.reportfooter = Band([
    Rule((330, 4), 72),
    Element((240, 4), ("Helvetica-Bold", 12), text="Grand Total"),
    SumElement((400, 4), ("Helvetica-Bold", 12), key="amount", ),
    Element((36, 16), ("Helvetica-Bold", 12), text=""),
])
rpt.groupheaders = [
    Band([
        Rule((36, 20), 7.5 * 72),
        Element((36, 4), ("Helvetica-Bold", 12),
                getvalue=lambda x: x["name"][0].upper(),
                format=lambda x: "Names beginning with %s" % x),
    ], getvalue=lambda x: x["name"][0].upper()),
]
rpt.groupfooters = [
    Band([
        Rule((330, 4), 72),
        Element((36, 4), ("Helvetica-Bold", 12),
                getvalue=lambda x: x["name"][0].upper(),
                format=lambda x: "Subtotal for %s" % x),
        SumElement((400, 4), ("Helvetica-Bold", 12),
                   key="amount", ),
        Element((36, 16), ("Helvetica-Bold", 12),
                text=""),
    ],
        getvalue=lambda x: x["name"][0].upper(),
        newpageafter=0),
]

sys.stdout.write("Report Starting...\nPage ")
canvas = Canvas("sample07.pdf", (72 * 11, 72 * 8.5))
rpt.generate(canvas)
canvas.save()
print("\nDone.")
