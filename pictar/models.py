from django.db import models



class Guide(models.Model):
    ''' function to create team table '''
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='photos/%y/%m/%d/')
    created_date = models.DateTimeField(null='True')

    def __str__(self):
        return self.first_name

   
