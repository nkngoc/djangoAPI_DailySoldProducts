from django.db.models import query
from django.shortcuts import render
from rest_framework import viewsets
from .models import transaction, productSold
from .serializers import rest_api_serializer


import json
import datetime
from time import sleep

from django.db import connection

# Create your views here.

class rest_api_view(viewsets.ModelViewSet):
    queryset = productSold.objects.all()
    serializer_class = rest_api_serializer

# you can also keep this inside a view

def emptyTables():
    
    # Empty tables:
    print('Empty 01 --------')
    countdata = transaction.objects.all().count()
    while countdata > 0:
        if countdata > 999:
            objects_to_keep = transaction.objects.all()[999:]
            transaction.objects.all().exclude(pk__in=objects_to_keep).delete()
            countdata = transaction.objects.all().count()
        else:
            transaction.objects.all().delete()
            countdata = transaction.objects.all().count()
                
    # Empty tables:
    print('Empty 02 --------')
    countdata = productSold.objects.all().count()
    while countdata > 0:
        if countdata > 999:
            objects_to_keep = productSold.objects.all()[999:]
            productSold.objects.all().exclude(pk__in=objects_to_keep).delete()
            countdata = productSold.objects.all().count()
        else:
            productSold.objects.all().delete()
            countdata = productSold.objects.all().count()


sql_0 = "INSERT INTO "
sql_1_tablename = "rest_api_transaction"
sql_2_columnSet="(salesdate, cid, pid, qty, sourcefile, createddate) VALUES "
sql_3_val="('{0:s}', {1:d}, {2:d}, {3:d}, '{4:s}', '{5:s}')"
sql_4_valSP=""


"""
Update Product Sold:
    - Calculate product sold and save to DB

Parameter
    salesdate <== it come from filenam '20190207_transactions.json' or from manual input

Notes:
    - updateProductSold(salesdate) to provice a method to update Product Sold at any-time we need do it.
"""

def updateProductSold(salesdate): 
    
    # connect to db:
    cursor = connection.cursor()

    #Calculate the product sold for the date=salesdate
    cursor.execute(
        sql_0 + 'rest_api_productSold' + '(salesdate, pid, total_qty) SELECT salesdate, pid, total_qty FROM ('
        " SELECT min(id) as id, pid, salesdate, sum(qty) as total_qty FROM "+sql_1_tablename+
        " WHERE salesdate ='" + str(salesdate) + 
        "' GROUP BY pid, salesdate)" # ORDER BY ID
        )

    cursor.fetchall()
    cursor.close()

    print("\n\nUpdate Product Sold Done!\n\n")

    return None


"""
Read the JsonL file to:
    - Get date from filename
    - Store data in DB

Parameter
    filename = '20190207_transactions.json'

Notes:
    - sourcefile & createddate are keys to control data versions
"""

def load_JSONL_by_sql(filename): 
    global sql_4_valSP
    
    with open(filename) as data_file:

        sdate = filename.split('_')[0].strip()
        salesdate = datetime.date(int(sdate[0:4]), int(sdate[4:6]), int(sdate[6:8]))
        json_lines = data_file.readlines()
        
        # connect to db:
        cursor = connection.cursor()
        sql_vals = ''

        cdatetime = datetime.datetime.now()
        id=0
        for json_record in json_lines:
            record = json.loads(json_record)
            uprod={}
            cus_id = record['id']
            for prod_id in record['products']:
                pid = int(prod_id)
                if pid in uprod: 
                    uprod[pid] += 1
                else:
                    uprod[pid] = 1
            
            # create distinct item/product for a source/day
            for prod_id, qty in uprod.items():
                # Slowly change
                #rcd = transaction.create(salesdate,cus_id,prod_id, qty, filename,cdatetime)
                #rcd.save()

                # Fast change
                #sql_vals+=sql_4_valSP + sql_3_val.format(str(salesdate),cus_id,prod_id, qty, filename,cdatetime.strftime("%Y-%m-%d, %H:%M:%S"))
                sql_vals+=sql_4_valSP + sql_3_val.format(str(salesdate),cus_id,prod_id, qty, filename,str(cdatetime))
                sql_4_valSP=','

            id+=1
            if id%100 ==0 or id == len(json_lines): 
                # Fast change
                cursor.execute(sql_0 + sql_1_tablename + sql_2_columnSet + sql_vals + ';')
                cursor.fetchall()

                sql_vals=''
                sql_4_valSP=''
                print(id,end=' ',flush = True)

        cursor.close()


    print("\n\n\nLoad %s done!\n\n" % filename)

    updateProductSold(salesdate)

    return salesdate

filename = '20190207_transactions.json'
#emptyTables()
#asalesdate = load_JSONL_by_sql(filename)
#updateProductSold(asalesdate)
