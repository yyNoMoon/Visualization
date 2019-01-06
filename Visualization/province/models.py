from django.db import models

# coding: utf8
# Create your models here.
class DataProvince(models.Model):
    '''每一年各个省份的金融机构数据'''

    # id = models.IntegerField(max_length=10, unique=True, auto_created=True)
    year = models.IntegerField()
    province = models.CharField(max_length=255)
    num = models.IntegerField()

    def __str__(self):
        return str(self.year)+str(self.province)+str(self.num)

    class Meta:
        db_table = "data_province_count"

class AttributeData(models.Model):
    '''每一年各个省份的多维数据'''

    # id = models.IntegerField(max_length=10, unique=True, auto_created=True)
    year = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    GRP = models.FloatField(max_length=10)
    PI_VA = models.FloatField(max_length=10)
    SI_VA = models.FloatField(max_length=10)
    TI_VA = models.FloatField(max_length=10)
    FI_VA = models.FloatField(max_length=10)
    REI_VA = models.FloatField(max_length=10)
    AFAF_VA = models.FloatField(max_length=10)
    I_VA = models.FloatField(max_length=10)
    CI_VA = models.FloatField(max_length=10)
    WR_VA = models.FloatField(max_length=10)
    CIWR_VA = models.FloatField(max_length=10)
    TWPI_VA = models.FloatField(max_length=10)
    TWPT_VA = models.FloatField(max_length=10)
    ACI_VA = models.FloatField(max_length=10)
    OI_VA = models.FloatField(max_length=10)
    TI_LPUN = models.IntegerField()
    FI_LPUN = models.IntegerField()
    REI_LPUN = models.IntegerField()
    STG_LPUN = models.IntegerField()
    ICS_LPUN = models.IntegerField()
    AVG_GDP = models.IntegerField()
    IL_GDP = models.FloatField(max_length=10)
    E_GDP = models.FloatField(max_length=10)
    RCL = models.IntegerField()
    R_RCL = models.IntegerField()
    U_RCL = models.IntegerField()
    FC = models.FloatField(max_length=10)
    GC = models.FloatField(max_length=10)
    RC = models.FloatField(max_length=10)
    R_RC = models.FloatField(max_length=10)
    U_RC = models.FloatField(max_length=10)
    GDPI = models.FloatField(max_length=10)
    PI_VAI = models.FloatField(max_length=10)
    SI_VAI = models.FloatField(max_length=10)
    TI_VAI = models.FloatField(max_length=10)
    RCLI = models.FloatField(max_length=10)
    R_RCLI = models.FloatField(max_length=10)
    U_RCLI = models.FloatField(max_length=10)
    RW = models.FloatField(max_length=10)
    NPT = models.FloatField(max_length=10)
    FAD = models.FloatField(max_length=10)
    OS = models.FloatField(max_length=10)
    T_CF = models.FloatField(max_length=10)
    TF_CF = models.FloatField(max_length=10)
    S_VA = models.FloatField(max_length=10)
    GS_NO = models.FloatField(max_length=10)
    FCR = models.FloatField(max_length=10)
    CFR = models.FloatField(max_length=10)

    FI_VAI = models.FloatField(max_length=10)
    REI_VAI = models.FloatField(max_length=10)
    ACI_VAI = models.FloatField(max_length=10)
    OI_VAI = models.FloatField(max_length=10)
    FI_CR = models.FloatField(max_length=10)
    REI_CR = models.FloatField(max_length=10)
    STG_CR = models.FloatField(max_length=10)
    ICS_CR = models.FloatField(max_length=10)


    class Meta:
        db_table = "data_year"