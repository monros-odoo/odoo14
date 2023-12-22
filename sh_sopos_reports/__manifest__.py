# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "All In One Sales & POS Reports",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "version": "14.0.9",
    "category": "Extra Tools",
    "summary": "Sales Report Based On Analysis,Compare Customer By Sales,Compare Products Based On Sell,Salesperson Wise Payment Report, Sales Report By Sales Person, Point Of Sale Report,sale reports,POS order report,point of sale order report POS Analysis Odoo",
    "description": """All in one Sales & POS (Point Of Sale) report useful to provide different POS and sales reports to do analysis. A sales &POS analysis report shows the trends that occur in a company's sales volume over time. In its most basic form, a sales & POS analysis report shows whether sales are increasing or declining.""",
    "depends": [
        'sale_management',
        'point_of_sale',
    ],
    "data": [
        "sh_payment_report_sopos/security/payment_report_security.xml",
        "sh_payment_report_sopos/security/ir.model.access.csv",
        "sh_payment_report_sopos/wizard/payment_report_wizard.xml",
        "sh_payment_report_sopos/report/payment_report.xml",
        "sh_payment_report_sopos/wizard/xls_report_view.xml",

        "sh_sopos_details_report/security/ir.model.access.csv",
        "sh_sopos_details_report/wizard/sale_pos_details_report_wizard.xml",
        "sh_sopos_details_report/report/sale_pos_details_report.xml",
        "sh_sopos_details_report/report/report_xlsx_view.xml",

        "sh_sopos_report_salesperson/security/ir.model.access.csv",
        "sh_sopos_report_salesperson/wizard/report_salesperson_wizard.xml",
        "sh_sopos_report_salesperson/views/xls_report_view.xml",
        "sh_sopos_report_salesperson/report/salesperson_report.xml",

        "sh_top_customers_sopos/security/ir.model.access.csv",
        "sh_top_customers_sopos/wizard/top_sopos_customer_wizard.xml",
        "sh_top_customers_sopos/report/top_sopos_customer_report.xml",
        "sh_top_customers_sopos/report/report_xlsx_view.xml",

        "sh_top_sopos_product/security/ir.model.access.csv",
        "sh_top_sopos_product/wizard/top_selling_wizard.xml",
        "sh_top_sopos_product/views/top_selling_view.xml",
        "sh_top_sopos_product/report/top_selling_product_report.xml",
        "sh_top_sopos_product/report/report_xlsx_view.xml",
        
        'sh_customer_sopos_analysis/security/ir.model.access.csv',
        'sh_customer_sopos_analysis/report/report_sales_analysis.xml',
        'sh_customer_sopos_analysis/wizard/customer_sales_analysis_wizard.xml',
        'sh_customer_sopos_analysis/report/report_sales_analysis_xls_view.xml',
        
        'sh_product_sopos_indent/security/ir.model.access.csv',
        'sh_product_sopos_indent/report/report_sales_product_indent.xml',
        'sh_product_sopos_indent/wizard/sale_product_indent_wizard.xml',
        'sh_product_sopos_indent/report/report_sale_product_indent_xls_view.xml',
        
        'sh_sopos_by_category/security/ir.model.access.csv',
        'sh_sopos_by_category/report/report_sale_by_category.xml',
        'sh_sopos_by_category/wizard/sale_by_category_wizard.xml',
        'sh_sopos_by_category/report/report_sale_category_xls_view.xml',
        
        'sh_sopos_invoice_summary/security/ir.model.access.csv',
        'sh_sopos_invoice_summary/report/report_sale_invoice_summary.xml',
        'sh_sopos_invoice_summary/wizard/sale_invoice_summary_wizard.xml',
        'sh_sopos_invoice_summary/report/report_sale_invoice_summary_xls_view.xml',
        
        'sh_sopos_product_profit/security/ir.model.access.csv',
        'sh_sopos_product_profit/report/report_sales_product_profit.xml',
        'sh_sopos_product_profit/wizard/sales_product_profit_wizard.xml',
        'sh_sopos_product_profit/report/report_sales_product_profit_xls_view.xml',
        
        "sh_sopos_profitability_report/security/sh_product_profitability_security.xml",
        "sh_sopos_profitability_report/report/sh_pos_profitability_report_view.xml",
        "sh_sopos_profitability_report/report/sh_product_profitability_report_view.xml",

        'sh_so_pos_sector_report/security/ir.model.access.csv',
        'sh_so_pos_sector_report/wizard/sector_report_wizard.xml',
        'sh_so_pos_sector_report/views/sector.xml',
    ],
    "images": ["static/description/background.gif", ],
    "installable": True,
    "license": "OPL-1",
    "auto_install": False,
    "application": True,
    "price": 110,
    "currency": "EUR"
}
