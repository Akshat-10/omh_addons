
{
    "name": "OMH Addons Module",
    "summary": "OMH Addons Module",
    "category": "Report",
    "author": "Akshat Gupta",
    "website": "",
    "depends": [
        'base','report_xlsx','account'
    ],
	'version': '16.0.1',
    "data": [
        'security/ir.model.access.csv',
        'views/opd_report.xml',
        'views/menu.xml',
        'reports/pharmacy_report_xlsx.xml',
    ],

    "installable": True,
    "auto_install": False,
    "application": False,

}
