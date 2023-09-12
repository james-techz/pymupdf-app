import fitz
from fitz import Widget, Rect

if __name__ == '__main__':
    pdf_file = 't244-fill-16e.pdf'
    out_pdf = 'out.pdf'

    context = {
        'form1[0].Page2[0].Section1_sf[0].RegistrationNumber[0]': '123456',
        'form1[0].Page2[0].Section1_sf[0].PlanType_sf[0].PlanType_rb[0]': '1', # 0=Defined benefit, 1=Money purchase, 2=Combination
        'form1[0].Page2[0].Section1_sf[0].ReportingPeriod[0]': '12', # It'd be better to insert text values, I've tried Int but it doesn't work
        'form1[0].Page2[0].Section1_sf[0].PlanYearEnd[0]': '2023-12-31',
        'form1[0].Page2[0].Section1_sf[0].PlanName[0]': 'RR-E of ABC inc. for Mr. John Doe',
        'form1[0].Page2[0].Section1_sf[0].PlanAdministrator[0]': 'ABC inc.',
        'form1[0].Page2[0].Section1_sf[0].Address[0]': '789, Main street',
        'form1[0].Page2[0].Section1_sf[0].City[0]': 'Montreal',
        'form1[0].Page2[0].Section1_sf[0].Privince[0]': 'QC', # The available values of this field are:
        # [ [ ( ) ( ) ] [ (AB) (Alberta) ] [ (BC) (British Columbia) ]
        #   [ (MB) (Manitoba) ] [ (NB) (New Brunswick) ] [ (NL) (Newfoundland and Labrador) ]
        #   [ (NT) (Northwest Territories) ] [ (NS) (Nova Scotia) ]
        #   [ (NU) (Nunavut) ] [ (ON) (Ontario) ] [ (PE) (Prince Edward Island) ]
        #   [ (QC) (Quebec) ] [ (SK) (Saskatchewan) ] [ (YT) (Yukon) ] ]
        #  for each item, e.g.: [ (QC) (Quebec) ] 
        #  we have to set field_value to the 1st item e.g. QC so it can work properly
        'form1[0].Page2[0].Section1_sf[0].PostalCode[0]': 'A1A 1A1',
        'form1[0].Page2[0].Section1_sf[0].PhoneNumber[0]': '(514) 123-4567',
        'form1[0].Page2[0].Section1_sf[0].BusinessNumber[0]': '987654321',
        'form1[0].Page2[0].Section1_sf[0].Contact[0]': 'Jane Smith',
        'form1[0].Page2[0].Section1_sf[0].LocationBooksRecords_sf[0].SameAddress[0]': True,
        # For checkbox, True = checked, False = unchecked
        'form1[0].Page2[0].Section1_sf[0].LocationBooksRecords_sf[0].Address[0]': None,
        'form1[0].Page2[0].Section1_sf[0].LocationBooksRecords_sf[0].City[0]': None,
        'form1[0].Page2[0].Section1_sf[0].LocationBooksRecords_sf[0].Prov_DropDown[0]': '',
        'form1[0].Page2[0].Section1_sf[0].LocationBooksRecords_sf[0].PostalCode_BordersAll[0]': None,
        'form1[0].Page2[0].Section2_sf[0].Line1[0].Line1_Amount[0]': '10000',
        'form1[0].Page2[0].Section2_sf[0].Line2[0].Line2_Amount[0]': '2000',
        'form1[0].Page2[0].Section2_sf[0].Line3[0].Line3_Amount[0]': '3000',
        'form1[0].Page2[0].Section2_sf[0].Line4[0].Line4_Amount[0]': '(500)',
        'form1[0].Page2[0].Section2_sf[0].Line5[0].Line5_Amount[0]': '300',
        'form1[0].Page2[0].Section2_sf[0].Line6[0].Line6_Amount[0]': '200',
        'form1[0].Page2[0].Section2_sf[0].Line7[0].Line7_Amount[0]': '123456',
        'form1[0].Page2[0].Section2_sf[0].Line8[0].Line8_Amount[0]': '137456',
        'form1[0].Page2[0].Section2_sf[0].Line9[0].Line9_Amount[0]': '115625',
        'form1[0].Page2[0].Section2_sf[0].Line10[0].Date[0]': '2022-12-31',
        'form1[0].Page3[0].Section3_sf[0].A_sf[0].A_rb[0]': '1', # 0 = Yes, 1  = No
        'form1[0].Page3[0].Section3_sf[0].A_sf[0].IfYes_Date[0].DateYYYYMMDD_Comb[0]': None, # Format: 20231231
        'form1[0].Page3[0].Section3_sf[0].B_sf[0].AB_rb[0]': '1', # 0 = Yes, 1  = No
        'form1[0].Page3[0].Section3_sf[0].B_sf[0].IfYes_Date[0].DateYYYYMMDD_Comb[0]': None, # Format: 20231231
        'form1[0].Page3[0].Section4_sf[0].A_Amount[0]': '2',
        'form1[0].Page3[0].Section4_sf[0].B_Amount[0]': '1',
        'form1[0].Page3[0].Section5_sf[0].Section5_Text[0]': '3',
        'form1[0].Page3[0].Section6_sf[0].List_sf[0].ListItem01_sf[0].Bullet_rb[0]': '1',  # 0 = Yes, 1  = No
        'form1[0].Page3[0].Section6_sf[0].List_sf[0].ListItem02_sf[0].Bullet_rb[0]': '1',  # 0 = Yes, 1  = No
        'form1[0].Page3[0].Section7_sf[0].Section7_rb[0]': '0',  # 0 = Yes, 1  = No
        'form1[0].Page3[0].Section8_sf[0].Section8_rb[0]': '1',  # 0 = Yes, 1  = No
        'form1[0].Page3[0].Section9_sf[0].Section9_rb[0]': '0',  # 0 = Yes, 1  = No
        'form1[0].Page3[0].Section10_sf[0].Section10_rb[0]': '0',  # 0 = Yes, 1  = No
        'form1[0].Page3[0].Section11_sf[0].Name[0]': 'Jane Doe',
        'form1[0].Page3[0].Section11_sf[0].Date[0]': '2024-02-12',
        'form1[0].Page3[0].Section11_sf[0].Signature[0]': './bill.png', # this field value is the signature image file path
        'form1[0].Page3[0].Section11_sf[0].Title[0]': 'Plan administrator',
        'form1[0].Page3[0].Section11_sf[0].PhoneNumber[0]': '(418) 765-4321'
    }

    with fitz.open(pdf_file) as f:
        # iterate over pages in the input file
        for page in f:
            # iterate over widgets (form fields) in a page
            for widget in page.widgets():
                # check if we define widget name in the context
                if widget.field_name in context:
                    # specially deal with signature field
                    if 'signature' in str(widget.field_name.split('.')[-1]).lower():
                        # x0, y0, x1, y1
                        # original widget position: 109.6520004272461, 593.7340087890625, 287.6520080566406, 604.7349853515625
                        # just a note
                        page.insert_image(
                            rect=widget.rect,
                            filename=context[widget.field_name]
                        )
                    # specially deal with RadioButtons
                    elif widget.field_type == fitz.PDF_WIDGET_TYPE_RADIOBUTTON:
                        if widget.on_state() == str(context[widget.field_name]):
                            widget.field_value = widget.on_state()
                        else:
                            widget.field_value = False
                    # set other fields
                    else:
                        widget.field_value = context[widget.field_name]
                    # dont forget to update the widget after change
                    widget.update()

        # save the PDF to output file
        f.save(out_pdf)