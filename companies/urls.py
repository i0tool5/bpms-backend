from rest_framework.routers import DefaultRouter

import companies.views as views


router = DefaultRouter()
router.register(r'companies', views.CompanyApiView)
router.register(r'contacts', views.ContactApiView)
