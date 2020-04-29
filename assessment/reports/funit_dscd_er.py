from PollyReports import Element, SumElement, Rule, Band, Report
from django.db import models
from django.db.models import ExpressionWrapper, F
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas

from assessment.models import UnitSancDesg


def funit_dscd_er(self, format, param):
    print(param)
    print(format)
    report_data = UnitSancDesg.objects.values('u_id', 'd5', 'u_name', 'd_gdesig', 'd_id', 'd_rank', 'd_discp', 'd_name',
                                              'd_grade',
                                              'd_gcode', 'tot', 'san', 'req', 'comment', 'd_cadre').annotate(
        total_count=ExpressionWrapper(
            F('san') + F('tot') + F('req'),
            output_field=models.IntegerField()
        )
    ).filter(
        u_id=param['u_id'], total_count__gt=0).order_by('d5', 'd_gcode')
    print(report_data)
    rpt = Report(report_data)

    pos_x_start = 36
    pos_y_start = 24
    col_1_pos = (pos_x_start, pos_y_start)
    col_2_pos = (col_1_pos[0] + 200, pos_y_start)
    col_3_pos = (col_2_pos[0] + 100, pos_y_start)
    col_4_pos = (col_3_pos[0] + 50, pos_y_start)
    col_5_pos = (col_4_pos[0] + 50, pos_y_start)
    col_6_pos = (col_5_pos[0] + 50, pos_y_start)

    rpt.pageheader = Band([

        Element((36, 0), ("Times-Bold", 20), getvalue=lambda x: x["u_name"].upper(),
                format=lambda x: "Unit Summary : %s" % x),

        Element(col_1_pos, ("Helvetica-Bold", 12), text="Designation"),
        Element(col_2_pos, ("Helvetica-Bold", 12), text="Grade", align="center"),
        Element(col_3_pos, ("Helvetica-Bold", 12), text="Cadre", align="center"),
        Element(col_4_pos, ("Helvetica-Bold", 12), text="Ext 1.1.2019", align="center", width=50),
        Element(col_5_pos, ("Helvetica-Bold", 12), text="Req 20-21", align="center", width=50),
        # Element(col_6_pos, ("Helvetica-Bold", 12), text="Sanc 20-21", align="center",  width=50),

        Rule((36, 56), 7.5 * 72, thickness=2),
    ])

    rpt.groupheaders = [
        Band([
            # Rule((36, 20), 7.5 * 72),
            Element((36, 4), ("Helvetica-Bold", 10),
                    getvalue=lambda x: x["d_gdesig"].upper(),
                    # format=lambda x: "Group Designation : %s" % x
                    ),
        ], getvalue=lambda x: x["d_gdesig"].upper()),
    ]

    rpt.detailband = Band([
        Element((col_1_pos[0], 0), ("Helvetica", 10), getvalue=lambda x: x["d_name"].upper(), ),
        Element((col_2_pos[0], 0), ("Helvetica", 10), key="d_grade", align="left"),
        Element((col_3_pos[0], 0), ("Helvetica", 10), key="d_cadre", align="right"),
        Element((col_4_pos[0], 0), ("Helvetica", 10), getvalue=lambda x: x["tot"] or 0, align="right"),
        Element((col_5_pos[0], 0), ("Helvetica", 10), getvalue=lambda x: x["req"] or 0, align="right"),
        # Element((col_6_pos[0], 0), ("Helvetica", 10), getvalue=lambda x: x["san"] or 0, align="right"),
    ])

    rpt.groupfooters = [
        Band([
            Rule((col_4_pos[0] - 24, 4), 30),
            Rule((col_5_pos[0] - 24, 4), 30),
            # Rule((col_6_pos[0]-24, 4), 30),

            Element((col_1_pos[0], 4), ("Helvetica-Bold", 10),
                    getvalue=lambda x: x["d_gdesig"].upper(),
                    format=lambda x: "Subtotal"
                    # format=lambda x: "Subtotal for %s" % x
                    ),
            SumElement((col_4_pos[0], 4), ("Helvetica-Bold", 10),
                       key="tot", align="right"),
            SumElement((col_5_pos[0], 4), ("Helvetica-Bold", 10),
                       key="req", align="right"),
            # SumElement((col_6_pos[0], 4), ("Helvetica-Bold", 10),
            #            key="san", align="right"),
            Element((36, 16), ("Helvetica-Bold", 10),
                    text=""),
        ],
            getvalue=lambda x: x["d_gdesig"].upper(),
            newpageafter=0),
    ]

    rpt.reportfooter = Band([
        Rule((col_4_pos[0] - 24, 4), 30),
        Rule((col_5_pos[0] - 24, 4), 30),
        # Rule((col_6_pos[0] - 24, 4), 30),

        Element((240, 4), ("Helvetica-Bold", 10), text="Unit Total"),
        SumElement((col_4_pos[0], 4), ("Helvetica-Bold", 10),
                   key="tot", align="right"),
        SumElement((col_5_pos[0], 4), ("Helvetica-Bold", 10),
                   key="req", align="right"),
        # SumElement((col_6_pos[0], 4), ("Helvetica-Bold", 10),
        #            key="san", align="right"),
        Element((36, 16), ("Helvetica-Bold", 10), text=""),
    ])

    rpt.pagefooter = Band([
        Element((400, 16), ("Times-Bold", 10), text="Industrial Engineering Dept, WCL HQ", align="right"),
        Element((36, 16), ("Helvetica-Bold", 10), sysvar="pagenumber", format=lambda x: "Page %d" % x),
    ])

    file_loc = "./report_folder/" + param['u_id'] + ".pdf"
    canvas = Canvas(file_loc, (210 * mm, 297 * mm))
    rpt.generate(canvas)
    print("report generated at %s" % file_loc)
    canvas.save()

    return file_loc
