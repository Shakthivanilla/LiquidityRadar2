
import streamlit as st
import os
from datetime import datetime
from io import BytesIO
from fpdf import FPDF
from data import fetch_member_data, calculate_risk_metrics

st.set_page_config(layout='wide')
st.title('Reports & Export')

df = fetch_member_data()
if df is None or df.empty:
    st.error("❌ No data available")
    st.stop()
df = calculate_risk_metrics(df)

st.markdown('### Generate comprehensive reports for stakeholders')

# PDF Report Generation
col1, col2 = st.columns(2)

with col1:
    st.markdown('#### 📄 PDF Report')
    st.markdown('Generate a comprehensive liquidity risk report in PDF format.')
    
    if st.button('Generate PDF Report', type='primary'):
        try:
            # Create PDF
            pdf = FPDF()
            pdf.add_page()
            
            # Title
            pdf.set_font('Arial', 'B', 20)
            pdf.set_text_color(0, 120, 215)
            pdf.cell(0, 10, 'Smart Liquidity Monitor Report', ln=True, align='C')
            pdf.ln(5)
            
            # Timestamp
            pdf.set_font('Arial', '', 10)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 10, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', ln=True, align='C')
            pdf.ln(10)
            
            # Summary Statistics
            pdf.set_font('Arial', 'B', 14)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 10, 'Executive Summary', ln=True)
            pdf.ln(3)
            
            pdf.set_font('Arial', '', 11)
            total_members = len(df)
            high_risk = len(df[df['risk_level'] == 'High Risk'])
            medium_risk = len(df[df['risk_level'] == 'Medium Risk'])
            low_risk = len(df[df['risk_level'] == 'Low Risk'])
            
            pdf.cell(0, 8, f'Total Members Monitored: {total_members}', ln=True)
            pdf.cell(0, 8, f'High Risk Members: {high_risk} ({high_risk/total_members*100:.1f}%)', ln=True)
            pdf.cell(0, 8, f'Medium Risk Members: {medium_risk} ({medium_risk/total_members*100:.1f}%)', ln=True)
            pdf.cell(0, 8, f'Low Risk Members: {low_risk} ({low_risk/total_members*100:.1f}%)', ln=True)
            pdf.ln(10)
            
            # Top 10 High Risk Members
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, 'Top 10 High Risk Members', ln=True)
            pdf.ln(3)
            
            # Table header
            pdf.set_font('Arial', 'B', 9)
            pdf.set_fill_color(0, 120, 215)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(60, 8, 'Member Name', 1, 0, 'C', True)
            pdf.cell(35, 8, 'Cash Buffer', 1, 0, 'C', True)
            pdf.cell(35, 8, 'Exposure', 1, 0, 'C', True)
            pdf.cell(30, 8, 'Risk Ratio', 1, 0, 'C', True)
            pdf.cell(30, 8, 'Risk Level', 1, 1, 'C', True)
            
            # Table data
            pdf.set_font('Arial', '', 8)
            pdf.set_text_color(0, 0, 0)
            
            top_risk = df.nlargest(10, 'risk_ratio')
            for _, row in top_risk.iterrows():
                pdf.cell(60, 7, str(row['name'])[:25], 1, 0, 'L')
                pdf.cell(35, 7, f"${row['cash_buffer_usd']:,.0f}", 1, 0, 'R')
                pdf.cell(35, 7, f"${row['exposure_usd']:,.0f}", 1, 0, 'R')
                pdf.cell(30, 7, f"{row['risk_ratio']:.2f}", 1, 0, 'C')
                pdf.cell(30, 7, str(row['risk_level']), 1, 1, 'C')
            
            pdf.ln(10)
            
            # Recommendations
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, 'Key Recommendations', ln=True)
            pdf.ln(3)
            
            pdf.set_font('Arial', '', 11)
            if high_risk > 0:
                pdf.multi_cell(0, 7, f'- {high_risk} members require immediate attention due to high risk ratios')
            if medium_risk > 5:
                pdf.multi_cell(0, 7, f'- Monitor {medium_risk} medium-risk members for potential escalation')
            pdf.multi_cell(0, 7, '- Consider implementing automated alerts for members crossing risk thresholds')
            pdf.multi_cell(0, 7, '- Review liquidity policies and credit limits for high-risk members')
            
            # Save PDF to bytes using BytesIO
            pdf_bytes = BytesIO()
            pdf_output = pdf.output(dest='S')
            if isinstance(pdf_output, str):
                pdf_bytes.write(pdf_output.encode('latin-1'))
            else:
                pdf_bytes.write(pdf_output)
            pdf_data = pdf_bytes.getvalue()
            
            st.success('✅ PDF Report generated successfully!')
            st.download_button(
                label='📥 Download PDF Report',
                data=pdf_data,
                file_name=f'liquidity_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
                mime='application/pdf'
            )
        except Exception as e:
            st.error(f'❌ Error generating PDF: {str(e)}')

with col2:
    st.markdown('#### 📊 CSV Export')
    st.markdown('Export raw data for further analysis in spreadsheet applications.')
    
    csv = df.to_csv(index=False)
    st.download_button(
        label='📥 Download CSV Data',
        data=csv,
        file_name=f'liquidity_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
        mime='text/csv'
    )
