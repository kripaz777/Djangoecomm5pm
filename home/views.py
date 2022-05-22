from django.shortcuts import render
from django.views import View

from .models import *
# Create your views here.

class Base(View):
	views = {}
	

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


