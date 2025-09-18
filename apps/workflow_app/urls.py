from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for API endpoints
router = DefaultRouter()
router.register(r'node-types', views.NodeTypeViewSet, basename='nodetype')
router.register(r'workflows', views.WorkflowViewSet, basename='workflow')
router.register(r'executions', views.WorkflowExecutionViewSet, basename='execution')
router.register(r'variables', views.WorkflowVariableViewSet, basename='variable')
router.register(r'webhooks', views.WorkflowWebhookViewSet, basename='webhook')
router.register(r'templates', views.WorkflowTemplateViewSet, basename='template')

app_name = 'workflow_app'

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Editor views
    path('', views.workflow_list_view, name='workflow_list'),
    path('create/', views.workflow_editor_view, name='workflow_create'),
    path('<uuid:workflow_id>/edit/', views.workflow_editor_view, name='workflow_edit'),
    path('<uuid:workflow_id>/', views.workflow_detail_view, name='workflow_detail'),
    
    # Webhook receiver
    path('webhook/<str:endpoint_path>/', views.webhook_receiver, name='webhook_receiver'),
    
    # Management views
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('templates/', views.template_list_view, name='template_list'),
    path('templates/create/', views.template_create_view, name='template_create'),
    path('templates/<uuid:template_id>/', views.template_detail_view, name='template_detail'),
    path('templates/<uuid:template_id>/edit/', views.template_edit_view, name='template_edit'),
    path('executions/', views.execution_list_view, name='execution_list'),
]
