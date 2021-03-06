from django.shortcuts import render,redirect
from django.views import View

from .models import *
# Create your views here.

class Base(View):
	views = {}
	views['categories'] = Category.objects.all()
	views['subcategories']  = SubCategory.objects.all()


class HomeView(Base):
	def get(self,request):
		self.views['categories'] = Category.objects.all()
		self.views['subcategories']  = SubCategory.objects.all()
		self.views['sliders'] = Slider.objects.all()
		self.views['ads'] = Ad.objects.all()         #2
		self.views['brands'] = Brand.objects.all()   #1
		self.views['default_product'] = Product.objects.filter(labels = 'default')
		self.views['new_product'] = Product.objects.filter(labels = 'new')
		self.views['hot_product'] = Product.objects.filter(labels = 'hot')
		self.views['sale_product'] = Product.objects.filter(labels = 'sale')

		return render(request,'shop-index.html',self.views)

class CategoryView(Base):
	def get(self,request,slug):
		cat_id = Category.objects.get(slug = slug).id
		self.views['cat_products'] = Product.objects.filter(category_id=cat_id)
		self.views['subcategories']  = SubCategory.objects.filter(category_id = cat_id)

		return render(request,'category.html',self.views)


class SubCategoryView(Base):
	def get(self,request,slug):
		subcat_id = SubCategory.objects.get(slug = slug).id
		self.views['subcat_products'] = Product.objects.filter(subcategory_id=subcat_id)
		self.views['categories']  = Category.objects.all()

		return render(request,'subcategory.html',self.views)


class SearchView(Base):
	def get(self,request):
		if request.method == "GET":
			query = request.GET['query']
			self.views['search_product'] = Product.objects.filter(name__icontains = query)

		return render(request,'shop-search-result.html',self.views)

class ProductDetailView(Base):
	def get(self,request,slug):
		self.views['product_view'] = Product.objects.filter(slug = slug)

		return render(request,'shop-item.html',self.views)


from django.contrib.auth.models import User
from django.contrib import messages
def signup(request):
	if request.method == "POST":
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		cpassword = request.POST['cpassword']
		if password == cpassword:
			if User.objects.filter(username = username).exists():
				messages.error(request,'The username is already used.')
				return redirect('/signup')

			elif User.objects.filter(email = email).exists():
				messages.error(request,'The email is already used.')
				return redirect('/signup')

			else:
				user = User.objects.create(
					username = username,
					email = email,
					password = password
					)
				user.save()
				return redirect('/')
		else:
			messages.error(request,'The password doest not match.')
			return redirect('/signup')
	return render(request,'signup.html')


def filter_cart(request,slug):
	username = request.user.username
	try:
		quantity =Cart.objects.get(slug = slug,user = username,checkout = False).quantity
	except:
		quantity = 1
	price = Product.objects.get(slug = slug).price
	discounted_price = Product.objects.get(slug = slug).discounted_price
	if discounted_price > 0:
		original_price = discounted_price
		total = original_price*quantity
	else:
		original_price = price
		total = original_price*quantity
	return quantity,original_price

def cart(request,slug):
	username = request.user.username
	if Cart.objects.filter(slug = slug,user = username,checkout = False).exists():
		quantity,original_price = filter_cart(request,slug)
		quantity = quantity +1
		total = quantity*original_price
		Cart.objects.filter(slug = slug,user = username,checkout = False).update(quantity = quantity,total = total)

		return redirect('/mycart')

	else:
		quantity,total = filter_cart(request,slug)
		data =Cart.objects.create(
				user = username,
				slug = slug,
				items = Product.objects.filter(slug = slug)[0],
				quantity = quantity,
				total = total
			)
		data.save()
		return redirect('/mycart')


class CartView(Base):
	def get(self,request):
		username = request.user.username
		self.views['view_cart'] = Cart.objects.filter(user = username,checkout = False)

		return render(request,'shop-shopping-cart.html',self.views)


def delete_cart(request,slug):
	username = request.user.username
	Cart.objects.filter(user = username,checkout = False,slug = slug).delete()
	return redirect('/mycart')


def reduce_cart_quantity(request,slug):
	username = request.user.username
	if Cart.objects.filter(slug = slug,user = username,checkout = False).exists():
		quantity,original_price = filter_cart(request,slug)
		if quantity > 1:
			quantity = quantity -1
			total = quantity*original_price
			Cart.objects.filter(slug = slug,user = username,checkout = False).update(quantity = quantity,total = total)

	return redirect('/mycart')
