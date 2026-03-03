"""
Invoice Generation System
Generates PDF invoices for payments
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from django.conf import settings
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)


class InvoiceGenerator:
    """Generate PDF invoices"""
    
    def __init__(self, payment, pr):
        self.payment = payment
        self.pr = pr
        self.styles = getSampleStyleSheet()
        
    def generate(self, output_path=None):
        """
        Generate invoice PDF
        
        Args:
            output_path: Path to save PDF (optional)
            
        Returns:
            str: Path to generated PDF
        """
        try:
            # Create output directory if it doesn't exist
            if not output_path:
                invoice_dir = os.path.join(settings.MEDIA_ROOT, 'invoices')
                os.makedirs(invoice_dir, exist_ok=True)
                output_path = os.path.join(
                    invoice_dir,
                    f'invoice_{self.pr.pr_number}_{self.payment.id}.pdf'
                )
            
            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Build PDF content
            story = []
            
            # Add header
            story.extend(self._create_header())
            story.append(Spacer(1, 0.3*inch))
            
            # Add invoice details
            story.extend(self._create_invoice_details())
            story.append(Spacer(1, 0.3*inch))
            
            # Add billing information
            story.extend(self._create_billing_info())
            story.append(Spacer(1, 0.3*inch))
            
            # Add items table
            story.extend(self._create_items_table())
            story.append(Spacer(1, 0.3*inch))
            
            # Add payment details
            story.extend(self._create_payment_details())
            story.append(Spacer(1, 0.3*inch))
            
            # Add footer
            story.extend(self._create_footer())
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"Invoice generated: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Invoice generation failed: {str(e)}")
            raise
    
    def _create_header(self):
        """Create invoice header"""
        elements = []
        
        # Company name
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=12,
            alignment=TA_CENTER
        )
        
        elements.append(Paragraph("INVOICE", title_style))
        
        # Company info
        company_style = ParagraphStyle(
            'CompanyInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#666666')
        )
        
        company_info = """
        <b>Purchase Request Management System</b><br/>
        123 Business Street<br/>
        City, State 12345<br/>
        Phone: (555) 123-4567<br/>
        Email: info@prms.com
        """
        
        elements.append(Paragraph(company_info, company_style))
        
        return elements
    
    def _create_invoice_details(self):
        """Create invoice details section"""
        elements = []
        
        # Invoice info table
        data = [
            ['Invoice Number:', f'INV-{self.payment.id:06d}'],
            ['Invoice Date:', datetime.now().strftime('%B %d, %Y')],
            ['PR Number:', self.pr.pr_number],
            ['Payment Date:', self.payment.payment_date.strftime('%B %d, %Y')],
            ['Payment Status:', self.payment.status]
        ]
        
        table = Table(data, colWidths=[2*inch, 3*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#333333')),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _create_billing_info(self):
        """Create billing information section"""
        elements = []
        
        # Section title
        title_style = ParagraphStyle(
            'SectionTitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=12
        )
        
        elements.append(Paragraph("Billing Information", title_style))
        
        # Billing details
        vendor_name = self.pr.vendor.name if self.pr.vendor else self.pr.vendor_name
        vendor_contact = self.pr.vendor.contact_person if self.pr.vendor else self.pr.vendor_contact
        vendor_email = self.pr.vendor.email if self.pr.vendor else 'N/A'
        
        data = [
            ['Bill To:', 'Vendor:'],
            [f'{self.pr.author.get_full_name() or self.pr.author.username}', vendor_name],
            [f'{self.pr.author.email}', vendor_contact],
            ['', vendor_email]
        ]
        
        table = Table(data, colWidths=[2.5*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _create_items_table(self):
        """Create items/services table"""
        elements = []
        
        # Section title
        title_style = ParagraphStyle(
            'SectionTitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=12
        )
        
        elements.append(Paragraph("Items/Services", title_style))
        
        # Items table
        data = [
            ['Description', 'Quantity', 'Unit Price', 'Amount']
        ]
        
        # Add PR items
        description = f"{self.pr.item_type}\n{self.pr.items_description[:100]}"
        quantity = self.pr.quantity or '1'
        unit_price = f"${self.pr.total:,.2f}"
        amount = f"${self.pr.total:,.2f}"
        
        data.append([description, quantity, unit_price, amount])
        
        # Add totals
        data.append(['', '', 'Subtotal:', f"${self.pr.total:,.2f}"])
        data.append(['', '', 'Tax (0%):', '$0.00'])
        data.append(['', '', 'Total:', f"${self.pr.total:,.2f}"])
        
        table = Table(data, colWidths=[3*inch, 1*inch, 1.2*inch, 1.2*inch])
        table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Data rows
            ('FONTNAME', (0, 1), (-1, -4), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -4), 10),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            
            # Total rows
            ('FONTNAME', (2, -3), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (2, -3), (-1, -1), 11),
            ('LINEABOVE', (2, -3), (-1, -3), 1, colors.black),
            ('LINEABOVE', (2, -1), (-1, -1), 2, colors.black),
            
            # Grid
            ('GRID', (0, 0), (-1, -4), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _create_payment_details(self):
        """Create payment details section"""
        elements = []
        
        # Section title
        title_style = ParagraphStyle(
            'SectionTitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=12
        )
        
        elements.append(Paragraph("Payment Details", title_style))
        
        # Payment info
        data = [
            ['Payment Method:', self.payment.payment_method],
            ['Payment Amount:', f"${self.payment.amount:,.2f}"],
            ['Reference Number:', self.payment.reference_number or 'N/A'],
            ['Payment Status:', self.payment.status],
            ['Processed By:', self.payment.processed_by.username if self.payment.processed_by else 'System']
        ]
        
        table = Table(data, colWidths=[2*inch, 3*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _create_footer(self):
        """Create invoice footer"""
        elements = []
        
        footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#666666'),
            alignment=TA_CENTER
        )
        
        footer_text = """
        <b>Thank you for your business!</b><br/>
        For questions about this invoice, please contact us at info@prms.com<br/>
        <i>This is a computer-generated invoice and does not require a signature.</i>
        """
        
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph(footer_text, footer_style))
        
        return elements


def generate_invoice(payment, pr, output_path=None):
    """
    Convenience function to generate an invoice
    
    Args:
        payment: Payment object
        pr: Purchase Request object
        output_path: Optional output path
        
    Returns:
        str: Path to generated PDF
    """
    generator = InvoiceGenerator(payment, pr)
    return generator.generate(output_path)
