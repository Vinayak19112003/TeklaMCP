"""
Report Generator - Generate professional PDF and Excel reports

This module creates client-ready PDF cost estimates and Excel BOQ (Bill of Quantities) reports.
"""

from typing import Dict
from datetime import datetime
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT


class ReportGenerator:
    """Generate professional PDF and Excel reports for cost estimates"""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        # Heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))

        # Right-aligned number style
        self.styles.add(ParagraphStyle(
            name='RightAlign',
            parent=self.styles['Normal'],
            alignment=TA_RIGHT
        ))

    def generate_pdf(self, estimate_data: Dict, project_name: str = "Structural Steel Project") -> str:
        """
        Generate professional PDF cost estimate report

        Args:
            estimate_data: Complete estimate dict from PricingEngine
            project_name: Name of the project

        Returns:
            Filename of generated PDF
        """
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"estimate_{timestamp}.pdf"

        # Create PDF document
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=0.75*inch
        )

        # Build content
        story = []

        # Header
        title = Paragraph("COST ESTIMATE", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.2*inch))

        # Company/Project Info
        project_info_data = [
            ['Project Name:', project_name],
            ['Date:', estimate_data['project_summary']['date']],
            ['Region:', estimate_data['project_summary']['region']],
            ['Currency:', estimate_data['project_summary']['currency']],
            ['Total Steel Weight:', f"{estimate_data['project_summary']['total_steel_weight_tonnes']} tonnes"],
        ]

        project_table = Table(project_info_data, colWidths=[2*inch, 4*inch])
        project_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0ff')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(project_table)
        story.append(Spacer(1, 0.3*inch))

        # Cost Summary
        heading = Paragraph("COST SUMMARY", self.styles['CustomHeading'])
        story.append(heading)

        currency = estimate_data.get('currency_symbol', estimate_data['project_summary']['currency'])
        summary = estimate_data['summary']

        summary_data = [
            ['Description', 'Amount'],
            ['Materials', f"{currency}{summary['materials']:,.2f}"],
            ['Labor', f"{currency}{summary['labor']:,.2f}"],
            ['Subtotal', f"{currency}{summary['subtotal']:,.2f}"],
            ['Overhead (10%)', f"{currency}{summary['overhead_10%']:,.2f}"],
            ['Profit (15%)', f"{currency}{summary['profit_15%']:,.2f}"],
            ['Contingency (5%)', f"{currency}{summary['contingency_5%']:,.2f}"],
            ['TOTAL ESTIMATE', f"{currency}{summary['total_estimate']:,.2f}"],
        ]

        summary_table = Table(summary_data, colWidths=[3.5*inch, 2.5*inch])
        summary_table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            # Data rows
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            # Subtotal row
            ('LINEABOVE', (0, 3), (-1, 3), 1, colors.grey),
            # Total row
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8f0ff')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 12),
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#1f4788')),
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))

        # Page break before detailed breakdown
        story.append(PageBreak())

        # Material Cost Breakdown
        heading = Paragraph("DETAILED MATERIAL BREAKDOWN", self.styles['CustomHeading'])
        story.append(heading)

        material_costs = estimate_data['material_costs']

        # Prepare material data
        material_data = [['Item', 'Quantity', 'Unit', 'Rate', 'Amount']]

        # Steel
        for item in material_costs.get('steel', []):
            material_data.append([
                item['item'],
                f"{item['quantity']:.3f}",
                item['unit'],
                f"{currency}{item['rate']:,.2f}",
                f"{currency}{item['amount']:,.2f}"
            ])

        # Bolts
        for item in material_costs.get('bolts', []):
            material_data.append([
                item['item'],
                str(item['quantity']),
                item['unit'],
                f"{currency}{item['rate']:,.2f}",
                f"{currency}{item['amount']:,.2f}"
            ])

        # Welding
        for item in material_costs.get('welding', []):
            material_data.append([
                item['item'],
                f"{item['quantity']:.1f}",
                item['unit'],
                f"{currency}{item['rate']:,.2f}",
                f"{currency}{item['amount']:,.2f}"
            ])

        # Concrete
        for item in material_costs.get('concrete', []):
            material_data.append([
                item['item'],
                f"{item['quantity']:.2f}",
                item['unit'],
                f"{currency}{item['rate']:,.2f}",
                f"{currency}{item['amount']:,.2f}"
            ])

        # Paint
        for item in material_costs.get('paint', []):
            material_data.append([
                item['item'],
                f"{item['quantity']:.2f}",
                item['unit'],
                f"{currency}{item['rate']:,.2f}",
                f"{currency}{item['amount']:,.2f}"
            ])

        # Total row
        material_data.append([
            'TOTAL MATERIALS',
            '',
            '',
            '',
            f"{currency}{material_costs['total']:,.2f}"
        ])

        material_table = Table(material_data, colWidths=[2.5*inch, 1*inch, 0.7*inch, 1.2*inch, 1.2*inch])
        material_table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            # Data rows
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -2), 9),
            # Total row
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8f0ff')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 10),
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#1f4788')),
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(material_table)
        story.append(Spacer(1, 0.3*inch))

        # Labor Cost Breakdown
        heading = Paragraph("LABOR COSTS", self.styles['CustomHeading'])
        story.append(heading)

        labor_costs = estimate_data['labor_costs']
        labor_data = [['Item', 'Quantity', 'Unit', 'Rate', 'Amount']]

        for item in labor_costs['items']:
            labor_data.append([
                item['item'],
                f"{item['quantity']:.3f}",
                item['unit'],
                f"{currency}{item['rate']:,.2f}",
                f"{currency}{item['amount']:,.2f}"
            ])

        # Total row
        labor_data.append([
            'TOTAL LABOR',
            '',
            '',
            '',
            f"{currency}{labor_costs['total']:,.2f}"
        ])

        labor_table = Table(labor_data, colWidths=[2.5*inch, 1*inch, 0.7*inch, 1.2*inch, 1.2*inch])
        labor_table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            # Data rows
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -2), 9),
            # Total row
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8f0ff')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 10),
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#1f4788')),
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(labor_table)

        # Build PDF
        doc.build(story)

        return filename

    def generate_excel(self, estimate_data: Dict, project_name: str = "Structural Steel Project") -> str:
        """
        Generate Excel BOQ (Bill of Quantities) report

        Args:
            estimate_data: Complete estimate dict from PricingEngine
            project_name: Name of the project

        Returns:
            Filename of generated Excel file
        """
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"boq_{timestamp}.xlsx"

        # Create Excel writer
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:

            # SHEET 1: Summary
            summary_data = {
                'Description': [
                    'Project Name',
                    'Date',
                    'Region',
                    'Currency',
                    'Total Steel Weight (tonnes)',
                    '',
                    'Materials',
                    'Labor',
                    'Subtotal',
                    'Overhead (10%)',
                    'Profit (15%)',
                    'Contingency (5%)',
                    'TOTAL ESTIMATE'
                ],
                'Value': [
                    project_name,
                    estimate_data['project_summary']['date'],
                    estimate_data['project_summary']['region'],
                    estimate_data['project_summary']['currency'],
                    estimate_data['project_summary']['total_steel_weight_tonnes'],
                    '',
                    estimate_data['summary']['materials'],
                    estimate_data['summary']['labor'],
                    estimate_data['summary']['subtotal'],
                    estimate_data['summary']['overhead_10%'],
                    estimate_data['summary']['profit_15%'],
                    estimate_data['summary']['contingency_5%'],
                    estimate_data['summary']['total_estimate']
                ]
            }

            df_summary = pd.DataFrame(summary_data)
            df_summary.to_excel(writer, sheet_name='Summary', index=False)

            # SHEET 2: Detailed Materials
            materials_list = []
            material_costs = estimate_data['material_costs']

            # Add steel items
            for item in material_costs.get('steel', []):
                materials_list.append({
                    'Category': 'Steel',
                    'Item': item['item'],
                    'Quantity': item['quantity'],
                    'Unit': item['unit'],
                    'Rate': item['rate'],
                    'Amount': item['amount']
                })

            # Add bolt items
            for item in material_costs.get('bolts', []):
                materials_list.append({
                    'Category': 'Bolts',
                    'Item': item['item'],
                    'Quantity': item['quantity'],
                    'Unit': item['unit'],
                    'Rate': item['rate'],
                    'Amount': item['amount']
                })

            # Add welding items
            for item in material_costs.get('welding', []):
                materials_list.append({
                    'Category': 'Welding',
                    'Item': item['item'],
                    'Quantity': item['quantity'],
                    'Unit': item['unit'],
                    'Rate': item['rate'],
                    'Amount': item['amount']
                })

            # Add concrete items
            for item in material_costs.get('concrete', []):
                materials_list.append({
                    'Category': 'Concrete',
                    'Item': item['item'],
                    'Quantity': item['quantity'],
                    'Unit': item['unit'],
                    'Rate': item['rate'],
                    'Amount': item['amount']
                })

            # Add paint items
            for item in material_costs.get('paint', []):
                materials_list.append({
                    'Category': 'Paint',
                    'Item': item['item'],
                    'Quantity': item['quantity'],
                    'Unit': item['unit'],
                    'Rate': item['rate'],
                    'Amount': item['amount']
                })

            # Add labor items
            labor_costs = estimate_data['labor_costs']
            for item in labor_costs['items']:
                materials_list.append({
                    'Category': 'Labor',
                    'Item': item['item'],
                    'Quantity': item['quantity'],
                    'Unit': item['unit'],
                    'Rate': item['rate'],
                    'Amount': item['amount']
                })

            df_materials = pd.DataFrame(materials_list)
            df_materials.to_excel(writer, sheet_name='Materials', index=False)

        return filename


# Example usage
if __name__ == "__main__":
    # Sample estimate data
    sample_estimate = {
        "project_summary": {
            "date": "2024-01-15 14:30:00",
            "region": "India",
            "currency": "INR",
            "total_steel_weight_tonnes": 2.501,
        },
        "material_costs": {
            "steel": [
                {"item": "Structural Steel - S355", "quantity": 2.501, "unit": "tonne", "rate": 65000, "amount": 162565.0}
            ],
            "bolts": [
                {"item": "Bolts - M20", "quantity": 96, "unit": "nos", "rate": 15, "amount": 1440.0},
                {"item": "Bolts - M24", "quantity": 16, "unit": "nos", "rate": 25, "amount": 400.0}
            ],
            "welding": [
                {"item": "Welding - Fillet 6mm", "quantity": 18.4, "unit": "m", "rate": 120, "amount": 2208.0},
                {"item": "Welding - Fillet 8mm", "quantity": 8.0, "unit": "m", "rate": 180, "amount": 1440.0}
            ],
            "concrete": [
                {"item": "Concrete - M30", "quantity": 4.0, "unit": "m³", "rate": 7000, "amount": 28000.0},
                {"item": "Reinforcement Steel", "quantity": 400.0, "unit": "kg", "rate": 65, "amount": 26000.0}
            ],
            "paint": [
                {"item": "Steel Painting (2 coats)", "quantity": 150.2, "unit": "m²", "rate": 250, "amount": 37550.0}
            ],
            "total": 259603.0
        },
        "labor_costs": {
            "items": [
                {"item": "Steel Fabrication", "quantity": 2.501, "unit": "tonne", "rate": 8000, "amount": 20008.0},
                {"item": "Steel Erection & Installation", "quantity": 2.501, "unit": "tonne", "rate": 12000, "amount": 30012.0}
            ],
            "total": 50020.0
        },
        "summary": {
            "materials": 259603.0,
            "labor": 50020.0,
            "subtotal": 309623.0,
            "overhead_10%": 30962.3,
            "profit_15%": 46443.45,
            "contingency_5%": 15481.15,
            "total_estimate": 402509.9
        },
        "currency_symbol": "₹"
    }

    # Create report generator
    reporter = ReportGenerator()

    # Generate reports
    print("🏗️  GENERATING REPORTS...\n")

    pdf_file = reporter.generate_pdf(sample_estimate, "Industrial Warehouse - Sample")
    print(f"✅ PDF Report generated: {pdf_file}")

    excel_file = reporter.generate_excel(sample_estimate, "Industrial Warehouse - Sample")
    print(f"✅ Excel BOQ generated: {excel_file}")

    print("\n📄 Reports created successfully!")
    print(f"   - PDF: {pdf_file}")
    print(f"   - Excel: {excel_file}")
