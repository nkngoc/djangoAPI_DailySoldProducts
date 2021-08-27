from django.db import models

# Create your models here.
class productSold(models.Model):
    salesdate = models.DateField() 
    pid = models.IntegerField(default=-1)
    total_qty = models.IntegerField(default=0) 
    def __str__(seft):
        return str(seft.salesdate) + ' ' + str(seft.pid) + ' ' + str(seft.total_qty) 

    @classmethod
    def create(cls, salesdate, pid, total_qty):
        aproduct = cls(salesdate=salesdate, pid=pid, total_qty=total_qty)
        return aproduct

class transaction(models.Model):
    # default = -1: is invalid data for both Customer _ID and Product_ID
    # unique id to make sure not dup-records
    salesdate = models.DateField() 
    # cid: Customer ID
    cid = models.IntegerField(default=-1)
    # pid: Product ID
    pid = models.IntegerField(default = -1)
    # count the product in a day
    qty = models.IntegerField(default = 0)
    # data source file: to control versions
    sourcefile = models.CharField(max_length=100)
    # datetime at starting load data into model
    createddate = models.DateTimeField() 
    #class Meta:
    #    unique_together = (('salesdate', 'cid', 'pid', 'sourcefile', 'createdate'))

    def __str__(seft):
        return str(seft.salesdate) + ' : ' + str(seft.cid) + ' : ' + str(seft.pid)  + ' : ' + str(seft.qty) + ' : ' + seft.sourcefile + ' : ' + str(seft.createddate)
        

    @classmethod
    def create(cls, salesdate, cid, pid, qty, sourcefile, createddate):
        restapi = cls(salesdate=salesdate, cid=cid, pid=pid, qty=qty, sourcefile=sourcefile,  createddate=createddate)

        return restapi