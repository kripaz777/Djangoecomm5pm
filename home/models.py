from django.db import models
# Create your models here.
STATUS = (('active','active'),('','default'))
class Category(models.Model):
	name = models.CharField(max_length = 400)
	slug = models.CharField(max_length = 500,unique = True)

	def __str__(self):
		return self.name

class SubCategory(models.Model):
	name = models.CharField(max_length = 400)
	slug = models.CharField(max_length = 500,unique = True)
	category = models.ForeignKey(Category,on_delete = models.CASCADE)

	def __str__(self):
			return self.name

class Slider(models.Model):
	name = models.CharField(max_length = 400)
	slug = models.CharField(max_length = 500,unique = True)
	image = models.ImageField(upload_to = 'media')
	description = models.TextField(blank = True)
	rank = models.IntegerField()
	status = models.CharField(blank = True,choices = STATUS,max_length = 50)

	def __str__(self):
		return self.name

class Ad(models.Model):
	name = models.CharField(max_length = 400)
	image = models.ImageField(upload_to = 'media')
	rank = models.IntegerField()
	status = models.CharField(blank = True,choices = STATUS,max_length = 50)

	def __str__(self):
		return self.name


class Brand(models.Model):
	name = models.CharField(max_length = 400)
	image = models.ImageField(upload_to = 'media')

	def __str__(self):
		return self.name

STOCK = (('In Stock','In Stock'),('Out of Stock','Out of Stock'))
LABELS = (('new','New'),('hot','Hot'),('sale','Sale'),('','Defalt'))
class Product(models.Model):
	name = models.CharField(max_length = 300)
	slug = models.CharField(max_length = 300,unique = True)
	category = models.ForeignKey(Category,on_delete = models.CASCADE)
	subcategory = models.ForeignKey(SubCategory,on_delete = models.CASCADE)
	stock = models.CharField(choices = STOCK,max_length = 100)
	labels = models.CharField(choices = LABELS,max_length = 100,blank = True)
	price = models.IntegerField()
	discounted_price = models.IntegerField()
	image = models.ImageField(upload_to = 'media')
	description = models.TextField()

	def __str__(self):
		return self.name

class Contact(models.Model):
	name = models.CharField(max_length = 300)
	email = models.EmailField(max_length = 300,blank = True)
	message = models.TextField(max_length = 500)

	def __str__(self):
		return self.name