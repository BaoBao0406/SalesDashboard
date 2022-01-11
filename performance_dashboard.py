#! python3
# main.py - 

import pyodbc
from datetime import date
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import numpy as np
from dateutil.relativedelta import relativedelta
import plotly.express as px


conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=VOPPSCLDBN01\VOPPSCLDBI01;'
                      'Database=SalesForce;'
                      'Trusted_Connection=yes;')


# FDC User ID and Name list
user = pd.read_sql('SELECT DISTINCT(Id), Name \
                    FROM dbo.[User]', conn)
user = user.set_index('Id')['Name'].to_dict()


# SM Production
# Set date range
now = datetime.datetime.now()
Start_year_prod = now - relativedelta(years=3)
Start_Date_prod = str(Start_year_prod.year) + '-01-01'
End_Date_prod = str(now.year) + '-12-31'
production = pd.read_sql("SELECT BK.OwnerId, BK.nihrm__Property__c, ac.Name, ac.BillingCountry, ag.Name, BK.Name, FORMAT(BK.nihrm__ArrivalDate__c, 'MM/dd/yyyy') AS ArrivalDate, FORMAT(BK.nihrm__DepartureDate__c, 'MM/dd/yyyy') AS DepartureDate, \
                                 BK.nihrm__CurrentBlendedRoomnightsTotal__c, BK.nihrm__BlendedGuestroomRevenueTotal__c, \
                                 BK.VCL_Blended_F_B_Revenue__c, BK.nihrm__CurrentBlendedEventRevenue7__c, BK.nihrm__BookingStatus__c, FORMAT(BK.nihrm__LastStatusDate__c, 'MM/dd/yyyy') AS LastStatusDate, \
                                 FORMAT(BK.nihrm__BookedDate__c, 'MM/dd/yyyy') AS BookedDate, BK.End_User_Region__c, BK.End_User_SIC__c, BK.nihrm__BookingTypeName__c, BK.Booking_ID_Number__c, FORMAT(BK.nihrm__DateDefinite__c, 'MM/dd/yyyy') AS DateDefinite, BK.Date_Definite_Month__c, BK.Date_Definite_Year__c \
                          FROM dbo.nihrm__Booking__c AS BK \
                          LEFT JOIN dbo.Account AS ac \
                              ON BK.nihrm__Account__c = ac.Id \
                          LEFT JOIN dbo.Account AS ag \
                              ON BK.nihrm__Agency__c = ag.Id \
                          WHERE (BK.nihrm__BookingTypeName__c NOT IN ('ALT Alternative', 'CN Concert', 'IN Internal')) AND \
                              (BK.nihrm__Property__c NOT IN ('Sands Macao Hotel')) AND (BK.nihrm__BookingStatus__c = 'Definite') AND \
                              (BK.nihrm__DateDefinite__c BETWEEN CONVERT(datetime, '" + Start_Date_prod + "') AND CONVERT(datetime, '" + End_Date_prod + "'))", conn)
production.columns = ['Owner Name', 'Property', 'Account', 'Company Country', 'Agency', 'Booking: Booking Post As', 'Arrival', 'Departure', 
                      'Blended Roomnights', 'Blended Guestroom Revenue Total', 'Blended F&B Revenue', 'Blended Rental Revenue', 'Status',
                      'Last Status Date', 'Booked', 'End User Region', 'End User SIC', 'Booking Type', 'Booking ID#', 'DateDefinite', 'Date Definite Month', 'Date Definite Year']
production['Owner Name'].replace(user, inplace=True)


# SM history vs now
Start_year_hist = now - relativedelta(years=3)
Start_Date_hist = str(Start_year_hist.year) + '-01-01'
End_Date_hist = str(now.year) + '-12-31'
history_compare = pd.read_sql("SELECT BK.OwnerId, BK.nihrm__Property__c, ac.Name, ac.BillingCountry, ag.Name, BK.Name, FORMAT(BK.nihrm__ArrivalDate__c, 'MM/dd/yyyy') AS ArrivalDate, BK.VCL_Arrival_Year__c, BK.VCL_Arrival_Month__c, FORMAT(BK.nihrm__DepartureDate__c, 'MM/dd/yyyy') AS DepartureDate, \
                                 BK.nihrm__CurrentBlendedRoomnightsTotal__c, BK.nihrm__BlendedGuestroomRevenueTotal__c, \
                                 BK.VCL_Blended_F_B_Revenue__c, BK.nihrm__CurrentBlendedEventRevenue7__c, BK.nihrm__BookingStatus__c, FORMAT(BK.nihrm__LastStatusDate__c, 'MM/dd/yyyy') AS LastStatusDate, \
                                 FORMAT(BK.nihrm__BookedDate__c, 'MM/dd/yyyy') AS BookedDate, BK.Booked_Year__c, BK.Booked_Month__c, BK.End_User_Region__c, BK.End_User_SIC__c, BK.nihrm__BookingTypeName__c, BK.Booking_ID_Number__c, FORMAT(BK.nihrm__DateDefinite__c, 'MM/dd/yyyy') AS DateDefinite, BK.Date_Definite_Month__c, BK.Date_Definite_Year__c \
                          FROM dbo.nihrm__Booking__c AS BK \
                          LEFT JOIN dbo.Account AS ac \
                              ON BK.nihrm__Account__c = ac.Id \
                          LEFT JOIN dbo.Account AS ag \
                              ON BK.nihrm__Agency__c = ag.Id \
                          WHERE (BK.nihrm__BookingTypeName__c NOT IN ('ALT Alternative', 'CN Concert', 'IN Internal')) AND \
                              (BK.nihrm__Property__c NOT IN ('Sands Macao Hotel')) AND \
                              (BK.nihrm__BookedDate__c BETWEEN CONVERT(datetime, '" + Start_Date_hist + "') AND CONVERT(datetime, '" + End_Date_hist + "'))", conn)
history_compare.columns = ['Owner Name', 'Property', 'Account', 'Company Country', 'Agency', 'Booking: Booking Post As', 'Arrival', 'Arrival Year', 'Arrival Month', 'Departure', 
                      'Blended Roomnights', 'Blended Guestroom Revenue Total', 'Blended F&B Revenue', 'Blended Rental Revenue', 'Status',
                      'Last Status Date', 'Booked', 'Booked Year', 'Booked Month', 'End User Region', 'End User SIC', 'Booking Type', 'Booking ID#', 'DateDefinite', 'Date Definite Month', 'Date Definite Year']
history_compare['Owner Name'].replace(user, inplace=True)


# SM current business
current_business = pd.read_sql("SELECT BK.OwnerId, BK.nihrm__Property__c, ac.Name, ac.BillingCountry, ag.Name, BK.Name, FORMAT(BK.nihrm__ArrivalDate__c, 'MM/dd/yyyy') AS ArrivalDate, FORMAT(BK.nihrm__DepartureDate__c, 'MM/dd/yyyy') AS DepartureDate, \
                                    BK.nihrm__CurrentBlendedRoomnightsTotal__c, BK.nihrm__BlendedGuestroomRevenueTotal__c, \
                                    BK.VCL_Blended_F_B_Revenue__c, BK.nihrm__CurrentBlendedEventRevenue7__c, BK.nihrm__BookingStatus__c, FORMAT(BK.nihrm__LastStatusDate__c, 'MM/dd/yyyy') AS LastStatusDate, \
                                    FORMAT(BK.nihrm__BookedDate__c, 'MM/dd/yyyy') AS BookedDate, BK.End_User_Region__c, BK.End_User_SIC__c, BK.nihrm__BookingTypeName__c, BK.Booking_ID_Number__c \
                                FROM dbo.nihrm__Booking__c AS BK \
                                LEFT JOIN dbo.Account AS ac \
                                    ON BK.nihrm__Account__c = ac.Id \
                                LEFT JOIN dbo.Account AS ag \
                                    ON BK.nihrm__Agency__c = ag.Id \
                                WHERE (BK.nihrm__BookingTypeName__c NOT IN ('ALT Alternative', 'CN Concert', 'IN Internal')) AND \
                                    (BK.nihrm__Property__c NOT IN ('Sands Macao Hotel')) AND (BK.nihrm__BookingStatus__c IN ('Tentative', 'Prospect'))", conn)
current_business.columns = ['Owner Name', 'Property', 'Account', 'Company Country', 'Agency', 'Booking: Booking Post As', 'Arrival', 'Departure', 
                            'Blended Roomnights', 'Blended Guestroom Revenue Total', 'Blended F&B Revenue', 'Blended Rental Revenue', 'Status',
                            'Last Status Date', 'Booked', 'End User Region', 'End User SIC', 'Booking Type', 'Booking ID#']
current_business['Owner Name'].replace(user, inplace=True)
current_business['Days before Arrive'] = ((pd.to_datetime(current_business['Arrival']) - pd.Timestamp.now().normalize()).dt.days).astype(int)
current_business.sort_values(by=['Days before Arrive'], inplace=True)


# SM Inquiry
inquiry = pd.read_sql("SELECT inq.OwnerId, inq.nihrm__Property__c, inq.nihrm__Account__c, inq.nihrm__Company__c, inq.Name, inq.nihrm__ArrivalDate__c, inq.nihrm__Guests__c, inq.nihrm__TotalRooms__c, inq.nihrm__Status__c \
                       FROM dbo.nihrm__Inquiry__c AS inq", conn)
inquiry.columns = ['Owner Name', 'Property', 'Account', 'Company', 'Name', 'Arrival', 'Guests', 'Total Rooms', 'Status']
inquiry['Owner Name'].replace(user, inplace=True)


# Pre process data

# Definite
sm_production = production[production['Owner Name'] == 'Luis Wan']
current_year = 2021
sm_current_production = sm_production[sm_production['Date Definite Year'] == current_year]

# Tentaive and Prospect
sm_current_business = current_business[current_business['Owner Name'] == 'Luis Wan']
bk_display_col = ['Property', 'Account', 'Agency', 'Booking: Booking Post As', 'Arrival', 'Departure', 'Blended Roomnights', 'Days before Arrive']
sm_current_business_t = sm_current_business[(sm_current_business['Status'] == 'Tentative') & (sm_current_business['Owner Name'] == 'Luis Wan')][bk_display_col]
sm_current_business_p = sm_current_business[(sm_current_business['Status'] == 'Prospect') & (sm_current_business['Owner Name'] == 'Luis Wan')][bk_display_col]

# Inquiry
inq_display_col = ['Property', 'Account', 'Company', 'Name', 'Arrival', 'Guests', 'Total Rooms']
sm_inquiry = inquiry[(inquiry['Owner Name'] == 'Luis Wan') & (inquiry['Status'] == 'Opened')][inq_display_col]


# Plot 1

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

fig1 = make_subplots(rows=3, cols=1, 
                     column_widths=[0.5], row_heights=[0.8, 0.8, 0.8], shared_xaxes=True)


history_count = history_compare.groupby(['Booked Month', 'Booked Year']).size().reset_index(name='NumberOfBK')
history_count['to_sort']=history_count['Booked Month'].apply(lambda x: months.index(x))
history_count = history_count.sort_values('to_sort')

years = history_count['Booked Year'].unique().tolist()

for year in years:
    line1 = go.Scatter(x=history_count[history_count['Booked Year'] == int(year)]['Booked Month'], 
                       y=history_count[history_count['Booked Year'] == int(year)]['NumberOfBK'], 
                       mode='lines+markers', name=str(int(year)))
    fig1.add_trace(line1, row=1, col=1)


fig1.update_layout(title='3 years Demand History Comparsion', xaxis_title='Month', xaxis_showticklabels=True)



pyo.plot(fig1, filename='line.html')
