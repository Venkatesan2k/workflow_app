from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.db.models import Q, Count, Avg
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required  # Added missing login_required import
from django.core.paginator import Paginator  # Added missing Paginator import
from datetime import datetime, timedelta  # Added missing datetime imports
import json
import uuid

from .models import (
    NodeType, Workflow, WorkflowExecution, NodeExecution,
    WorkflowWebhook, WorkflowSchedule, WorkflowTemplate, WorkflowVariable
)
from .serializers import (
    NodeTypeSerializer, WorkflowSerializer, WorkflowExecutionSerializer,
    NodeExecutionSerializer, WorkflowWebhookSerializer, WorkflowScheduleSerializer,
    WorkflowTemplateSerializer, WorkflowVariableSerializer, WorkflowExecuteSerializer,
    WorkflowImportSerializer, WorkflowExportSerializer, NodeValidationSerializer
)
from .tasks import execute_workflow_task
from .permissions import IsWorkflowOwnerOrShared

class NodeTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for node types - read-only for users
    """
    queryset = NodeType.objects.filter(is_active=True)
    serializer_class = NodeTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset.order_by('category', 'display_name')

    @action(detail=False, methods=['post'])
    def validate_config(self, request):
        """Validate node configuration against schema"""
        serializer = NodeValidationSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'valid': True})
        return Response({'valid': False, 'errors': serializer.errors}, 
                       status=status.HTTP_400_BAD_REQUEST)

class WorkflowViewSet(viewsets.ModelViewSet):
    """
    ViewSet for workflows with full CRUD operations
    """
    serializer_class = WorkflowSerializer
    permission_classes = [IsAuthenticated, IsWorkflowOwnerOrShared]

    def get_queryset(self):
        user = self.request.user
        return Workflow.objects.filter(
            Q(created_by=user) | Q(shared_with=user)
        ).distinct().select_related('created_by').prefetch_related('shared_with', 'variables')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        """Execute a workflow"""
        workflow = self.get_object()
        serializer = WorkflowExecuteSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        input_data = serializer.validated_data.get('input_data', {})
        sync = serializer.validated_data.get('sync', False)
        test_mode = serializer.validated_data.get('test_mode', False)

        # Create execution record
        execution = WorkflowExecution.objects.create(
            workflow=workflow,
            triggered_by='manual',
            triggered_by_user=request.user,
            input_data=input_data,
            execution_context={'test_mode': test_mode}
        )

        if sync:
            # Execute synchronously (for testing small workflows)
            from .engine import WorkflowEngine
            engine = WorkflowEngine()
            engine.execute_workflow(str(execution.id))
            execution.refresh_from_db()
            serializer = WorkflowExecutionSerializer(execution)
            return Response(serializer.data)
        else:
            # Execute asynchronously
            execute_workflow_task.delay(str(execution.id))
            return Response({
                'execution_id': execution.id,
                'status': 'queued',
                'message': 'Workflow execution started'
            })

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a workflow"""
        workflow = self.get_object()
        workflow.status = 'active'
        workflow.save()
        
        # Set up triggers if needed
        self._setup_workflow_triggers(workflow)
        
        return Response({'status': 'activated', 'message': 'Workflow is now active'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a workflow"""
        workflow = self.get_object()
        workflow.status = 'inactive'
        workflow.save()
        
        # Remove triggers
        self._remove_workflow_triggers(workflow)
        
        return Response({'status': 'deactivated', 'message': 'Workflow is now inactive'})

    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Duplicate a workflow"""
        original_workflow = self.get_object()
        
        # Create a copy
        new_workflow = Workflow.objects.create(
            name=f"{original_workflow.name} (Copy)",
            description=original_workflow.description,
            definition=original_workflow.definition,
            timeout_seconds=original_workflow.timeout_seconds,
            max_retries=original_workflow.max_retries,
            retry_delay_seconds=original_workflow.retry_delay_seconds,
            created_by=request.user,
            status='draft'
        )
        
        serializer = self.get_serializer(new_workflow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def export(self, request, pk=None):
        """Export workflow as JSON"""
        workflow = self.get_object()
        serializer = WorkflowExportSerializer(data=request.query_params)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        export_data = {
            'workflow': {
                'name': workflow.name,
                'description': workflow.description,
                'definition': workflow.definition,
                'timeout_seconds': workflow.timeout_seconds,
                'max_retries': workflow.max_retries,
                'retry_delay_seconds': workflow.retry_delay_seconds,
                'tags': workflow.tags
            },
            'exported_at': timezone.now().isoformat(),
            'version': '1.0'
        }

        if serializer.validated_data.get('include_variables'):
            variables = WorkflowVariableSerializer(workflow.variables.all(), many=True)
            export_data['variables'] = variables.data

        if serializer.validated_data.get('include_executions'):
            executions = WorkflowExecutionSerializer(
                workflow.executions.all()[:10], many=True
            )
            export_data['recent_executions'] = executions.data

        return Response(export_data)

    @action(detail=False, methods=['post'])
    def import_workflow(self, request):
        """Import workflow from JSON"""
        serializer = WorkflowImportSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        workflow_data = serializer.validated_data['workflow_data']
        
        # Create workflow from imported data
        workflow = Workflow.objects.create(
            name=serializer.validated_data.get('name', workflow_data.get('workflow', {}).get('name', 'Imported Workflow')),
            description=serializer.validated_data.get('description', workflow_data.get('workflow', {}).get('description', '')),
            definition=workflow_data.get('workflow', {}).get('definition', {}),
            timeout_seconds=workflow_data.get('workflow', {}).get('timeout_seconds', 300),
            max_retries=workflow_data.get('workflow', {}).get('max_retries', 3),
            retry_delay_seconds=workflow_data.get('workflow', {}).get('retry_delay_seconds', 60),
            tags=workflow_data.get('workflow', {}).get('tags', []),
            created_by=request.user,
            status='draft'
        )

        # Import variables if present
        if 'variables' in workflow_data:
            for var_data in workflow_data['variables']:
                WorkflowVariable.objects.create(
                    workflow=workflow,
                    name=var_data['name'],
                    value=var_data['value'],
                    scope='workflow',
                    description=var_data.get('description', ''),
                    is_secret=var_data.get('is_secret', False),
                    created_by=request.user
                )

        serializer = WorkflowSerializer(workflow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def executions(self, request, pk=None):
        """Get workflow executions"""
        workflow = self.get_object()
        executions = workflow.executions.all()
        
        # Filter by status if provided
        status_filter = request.query_params.get('status')
        if status_filter:
            executions = executions.filter(status=status_filter)
        
        # Pagination
        page_size = int(request.query_params.get('page_size', 20))
        page = int(request.query_params.get('page', 1))
        start = (page - 1) * page_size
        end = start + page_size
        
        executions = executions[start:end]
        serializer = WorkflowExecutionSerializer(executions, many=True)
        
        return Response({
            'results': serializer.data,
            'count': workflow.executions.count(),
            'page': page,
            'page_size': page_size
        })

    def _setup_workflow_triggers(self, workflow):
        """Set up triggers for an active workflow"""
        # This would integrate with your scheduling system
        # For now, just a placeholder
        pass

    def _remove_workflow_triggers(self, workflow):
        """Remove triggers for an inactive workflow"""
        # This would remove from scheduling system
        # For now, just a placeholder
        pass

class WorkflowExecutionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for workflow executions - read-only
    """
    serializer_class = WorkflowExecutionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return WorkflowExecution.objects.filter(
            workflow__created_by=user
        ).select_related('workflow', 'triggered_by_user').prefetch_related('node_executions')

    @action(detail=True, methods=['get'])
    def logs(self, request, pk=None):
        """Get detailed execution logs"""
        execution = self.get_object()
        node_executions = execution.node_executions.all().order_by('execution_order', 'started_at')
        
        logs = []
        for node_exec in node_executions:
            logs.append({
                'timestamp': node_exec.started_at,
                'level': 'ERROR' if node_exec.status == 'failed' else 'INFO',
                'node_id': node_exec.node_id,
                'node_name': node_exec.node_name,
                'message': node_exec.error_message if node_exec.status == 'failed' else f"Node executed successfully",
                'duration_ms': node_exec.duration_ms,
                'input_data': node_exec.input_data,
                'output_data': node_exec.output_data if node_exec.status == 'success' else None
            })
        
        return Response({'logs': logs})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a running execution"""
        execution = self.get_object()
        
        if execution.status not in ['queued', 'running']:
            return Response(
                {'error': 'Can only cancel queued or running executions'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        execution.status = 'cancelled'
        execution.finished_at = timezone.now()
        execution.save()
        
        # TODO: Cancel the actual task if it's running
        
        return Response({'status': 'cancelled'})

class WorkflowVariableViewSet(viewsets.ModelViewSet):
    """
    ViewSet for workflow variables
    """
    serializer_class = WorkflowVariableSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        workflow_id = self.request.query_params.get('workflow')
        
        queryset = WorkflowVariable.objects.filter(created_by=user)
        
        if workflow_id:
            queryset = queryset.filter(workflow_id=workflow_id)
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class WorkflowWebhookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for workflow webhooks
    """
    serializer_class = WorkflowWebhookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return WorkflowWebhook.objects.filter(workflow__created_by=user)

    def perform_create(self, serializer):
        # Generate unique endpoint path if not provided
        if not serializer.validated_data.get('endpoint_path'):
            endpoint_path = f"/webhook/{uuid.uuid4().hex[:8]}"
            serializer.validated_data['endpoint_path'] = endpoint_path
        
        # Generate API key if required
        if serializer.validated_data.get('require_auth') and not serializer.validated_data.get('api_key'):
            api_key = f"wh_{uuid.uuid4().hex}"
            serializer.validated_data['api_key'] = api_key
        
        serializer.save()

class WorkflowTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for workflow templates
    """
    serializer_class = WorkflowTemplateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = WorkflowTemplate.objects.filter(
            Q(created_by=user) | Q(is_public=True)
        )
        
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset.order_by('-usage_count', 'name')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def use_template(self, request, pk=None):
        """Create a workflow from template"""
        template = self.get_object()
        
        # Increment usage count
        template.usage_count += 1
        template.save()
        
        # Create workflow from template
        workflow = Workflow.objects.create(
            name=f"{template.name} - {timezone.now().strftime('%Y%m%d_%H%M')}",
            description=template.description,
            definition=template.template_definition,
            created_by=request.user,
            status='draft')
        serializer = WorkflowSerializer(workflow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# API Views for specific functionality
@login_required
def workflow_editor_view(request, workflow_id=None):
    """Render the workflow editor page"""
    workflow = None
    workflow_json = {'nodes': [], 'connections': []}
    
    if workflow_id:
        try:
            workflow = Workflow.objects.get(
                id=workflow_id,
                created_by=request.user
            )
            workflow_json = workflow.definition
        except Workflow.DoesNotExist:
            pass
    
    context = {
        'workflow': workflow,
        'workflow_json': json.dumps(workflow_json)
    }
    
    return render(request, 'workflow_app/workflow_editor.html', context)

@login_required
def webhook_receiver(request, endpoint_path):
    """Generic webhook receiver"""
    try:
        webhook = WorkflowWebhook.objects.get(
            endpoint_path=f"/{endpoint_path}",
            is_active=True
        )
        
        # Validate request method
        if request.method != webhook.http_method:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        
        # Validate authentication if required
        if webhook.require_auth:
            api_key = request.headers.get('X-API-Key') or request.GET.get('api_key')
            if api_key != webhook.api_key:
                return JsonResponse({'error': 'Invalid API key'}, status=401)
        
        # Validate IP if restricted
        if webhook.allowed_ips:
            client_ip = request.META.get('REMOTE_ADDR')
            if client_ip not in webhook.allowed_ips:
                return JsonResponse({'error': 'IP not allowed'}, status=403)
        
        # Get request data
        if request.content_type == 'application/json':
            try:
                input_data = json.loads(request.body)
            except json.JSONDecodeError:
                input_data = {}
        else:
            input_data = dict(request.POST)
        
        # Create execution
        execution = WorkflowExecution.objects.create(
            workflow=webhook.workflow,
            triggered_by='webhook',
            input_data=input_data,
            execution_context={'webhook_id': str(webhook.id)}
        )
        
        # Update webhook stats
        webhook.last_triggered_at = timezone.now()
        webhook.trigger_count += 1
        webhook.save()
        
        # Execute workflow asynchronously
        execute_workflow_task.delay(str(execution.id))
        
        return JsonResponse({
            'status': 'success',
            'execution_id': str(execution.id),
            'message': 'Workflow triggered successfully'
        })
        
    except WorkflowWebhook.DoesNotExist:
        return JsonResponse({'error': 'Webhook not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def workflow_list_view(request):
    """Display list of user's workflows"""
    workflows = Workflow.objects.filter(
        Q(created_by=request.user) | Q(shared_with=request.user)
    ).distinct().select_related('created_by').annotate(
        execution_count=Count('executions')
    ).order_by('-updated_at')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        workflows = workflows.filter(status=status_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        workflows = workflows.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(workflows, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'workflows': page_obj,
        'status_filter': status_filter,
        'search_query': search_query,
        'total_workflows': workflows.count(),
        'active_workflows': workflows.filter(status='active').count(),
        'draft_workflows': workflows.filter(status='draft').count(),
    }
    
    return render(request, 'workflow_app/workflow_list.html', context)

@login_required
def workflow_detail_view(request, workflow_id):
    """Display detailed view of a workflow"""
    workflow = get_object_or_404(
        Workflow.objects.select_related('created_by').prefetch_related(
            'executions', 'variables', 'webhooks', 'shared_with'
        ),
        id=workflow_id,
        created_by=request.user
    )
    
    recent_executions = workflow.executions.all().order_by('-started_at')[:10]
    
    # Get execution statistics
    total_executions = workflow.executions.count()
    successful_executions = workflow.executions.filter(status='success').count()
    failed_executions = workflow.executions.filter(status='failed').count()
    success_rate = (successful_executions / total_executions * 100) if total_executions > 0 else 0
    
    # Get execution history for chart (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    execution_history = workflow.executions.filter(
        started_at__gte=thirty_days_ago
    ).extra(
        select={'day': 'date(started_at)'}
    ).values('day').annotate(
        total=Count('id'),
        successful=Count('id', filter=Q(status='success')),
        failed=Count('id', filter=Q(status='failed'))
    ).order_by('day')
    
    context = {
        'workflow': workflow,
        'recent_executions': recent_executions,
        'total_executions': total_executions,
        'successful_executions': successful_executions,
        'failed_executions': failed_executions,
        'success_rate': round(success_rate, 1),
        'execution_history': list(execution_history),
        'node_count': len(workflow.definition.get('nodes', [])),
        'connection_count': len(workflow.definition.get('connections', [])),
    }
    
    return render(request, 'workflow_app/workflow_detail.html', context)

@login_required
def dashboard_view(request):
    """Main dashboard view with overview statistics"""
    user = request.user
    
    # Get user's workflows
    workflows = Workflow.objects.filter(created_by=user)
    
    # Basic statistics
    total_workflows = workflows.count()
    active_workflows = workflows.filter(status='active').count()
    draft_workflows = workflows.filter(status='draft').count()
    inactive_workflows = workflows.filter(status='inactive').count()
    
    # Execution statistics
    executions = WorkflowExecution.objects.filter(workflow__created_by=user)
    total_executions = executions.count()
    successful_executions = executions.filter(status='success').count()
    failed_executions = executions.filter(status='failed').count()
    running_executions = executions.filter(status__in=['queued', 'running']).count()
    
    # Recent activity
    recent_executions = executions.select_related('workflow').order_by('-started_at')[:10]
    recent_workflows = workflows.order_by('-updated_at')[:5]
    
    # Execution trends (last 7 days)
    seven_days_ago = timezone.now() - timedelta(days=7)
    daily_executions = executions.filter(
        started_at__gte=seven_days_ago
    ).extra(
        select={'day': 'date(started_at)'}
    ).values('day').annotate(
        total=Count('id'),
        successful=Count('id', filter=Q(status='success')),
        failed=Count('id', filter=Q(status='failed'))
    ).order_by('day')
    
    # Top performing workflows
    top_workflows = workflows.annotate(
        execution_count=Count('executions')
    ).filter(execution_count__gt=0).order_by('-execution_count')[:5]
    
    # System health indicators
    error_rate = (failed_executions / total_executions * 100) if total_executions > 0 else 0
    avg_execution_time = executions.filter(
        status='success',
        finished_at__isnull=False
    ).aggregate(
        avg_duration=Avg('duration_seconds')
    )['avg_duration'] or 0
    
    context = {
        'total_workflows': total_workflows,
        'active_workflows': active_workflows,
        'draft_workflows': draft_workflows,
        'inactive_workflows': inactive_workflows,
        'total_executions': total_executions,
        'successful_executions': successful_executions,
        'failed_executions': failed_executions,
        'running_executions': running_executions,
        'recent_executions': recent_executions,
        'recent_workflows': recent_workflows,
        'daily_executions': list(daily_executions),
        'top_workflows': top_workflows,
        'error_rate': round(error_rate, 1),
        'avg_execution_time': round(avg_execution_time, 2) if avg_execution_time else 0,
        'success_rate': round((successful_executions / total_executions * 100), 1) if total_executions > 0 else 0,
    }
    
    return render(request, 'workflow_app/dashboard.html', context)

@login_required
def template_list_view(request):
    """Display list of workflow templates"""
    templates = WorkflowTemplate.objects.filter(
        Q(created_by=request.user) | Q(is_public=True)
    ).select_related('created_by').order_by('-usage_count', 'name')
    
    # Filter by category if provided
    category_filter = request.GET.get('category')
    if category_filter:
        templates = templates.filter(category=category_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        templates = templates.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    # Get available categories
    categories = WorkflowTemplate.objects.values_list('category', flat=True).distinct()
    
    # Pagination
    paginator = Paginator(templates, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'templates': page_obj,
        'categories': categories,
        'category_filter': category_filter,
        'search_query': search_query,
        'total_templates': templates.count(),
        'public_templates': templates.filter(is_public=True).count(),
        'my_templates': templates.filter(created_by=request.user).count(),
    }
    
    return render(request, 'workflow_app/template_list.html', context)

@login_required
def execution_list_view(request):
    """Display list of workflow executions"""
    executions = WorkflowExecution.objects.filter(
        workflow__created_by=request.user
    ).select_related('workflow', 'triggered_by_user').prefetch_related(
        'node_executions'
    ).order_by('-started_at')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        executions = executions.filter(status=status_filter)
    
    # Filter by workflow if provided
    workflow_filter = request.GET.get('workflow')
    if workflow_filter:
        executions = executions.filter(workflow_id=workflow_filter)
    
    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            executions = executions.filter(started_at__date__gte=date_from)
        except ValueError:
            pass
    if date_to:
        try:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            executions = executions.filter(started_at__date__lte=date_to)
        except ValueError:
            pass
    
    # Get user's workflows for filter dropdown
    user_workflows = Workflow.objects.filter(created_by=request.user).values('id', 'name')
    
    # Pagination
    paginator = Paginator(executions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    total_executions = executions.count()
    successful_executions = executions.filter(status='success').count()
    failed_executions = executions.filter(status='failed').count()
    running_executions = executions.filter(status__in=['queued', 'running']).count()
    
    context = {
        'page_obj': page_obj,
        'executions': page_obj,
        'user_workflows': user_workflows,
        'status_filter': status_filter,
        'workflow_filter': workflow_filter,
        'date_from': date_from,
        'date_to': date_to,
        'total_executions': total_executions,
        'successful_executions': successful_executions,
        'failed_executions': failed_executions,
        'running_executions': running_executions,
        'success_rate': round((successful_executions / total_executions * 100), 1) if total_executions > 0 else 0,
    }
    
    return render(request, 'workflow_app/execution_list.html', context)

@login_required
def template_create_view(request):
    """Create a new workflow template"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        category = request.POST.get('category', 'general')
        is_public = request.POST.get('is_public') == 'on'
        workflow_id = request.POST.get('workflow_id')
        
        if name and workflow_id:
            try:
                workflow = Workflow.objects.get(id=workflow_id, created_by=request.user)
                template = WorkflowTemplate.objects.create(
                    name=name,
                    description=description,
                    category=category,
                    template_definition=workflow.definition,
                    is_public=is_public,
                    created_by=request.user
                )
                return redirect('workflow_app:template_detail', template_id=template.id)
            except Workflow.DoesNotExist:
                pass
    
    # Get user's workflows for template creation
    workflows = Workflow.objects.filter(created_by=request.user).values('id', 'name', 'description')
    
    context = {
        'workflows': workflows,
        'categories': ['general', 'automation', 'data-processing', 'integration', 'notification']
    }
    
    return render(request, 'workflow_app/template_create.html', context)

@login_required
def template_detail_view(request, template_id):
    """Display detailed view of a workflow template"""
    template = get_object_or_404(
        WorkflowTemplate.objects.select_related('created_by'),
        id=template_id
    )
    
    # Check if user can view this template
    if not template.is_public and template.created_by != request.user:
        return redirect('workflow_app:template_list')
    
    context = {
        'template': template,
        'can_edit': template.created_by == request.user,
        'node_count': len(template.template_definition.get('nodes', [])),
        'connection_count': len(template.template_definition.get('connections', [])),
    }
    
    return render(request, 'workflow_app/template_detail.html', context)

@login_required
def template_edit_view(request, template_id):
    """Edit a workflow template"""
    template = get_object_or_404(
        WorkflowTemplate,
        id=template_id,
        created_by=request.user
    )
    
    if request.method == 'POST':
        template.name = request.POST.get('name', template.name)
        template.description = request.POST.get('description', template.description)
        template.category = request.POST.get('category', template.category)
        template.is_public = request.POST.get('is_public') == 'on'
        template.save()
        
        return redirect('workflow_app:template_detail', template_id=template.id)
    
    context = {
        'template': template,
        'categories': ['general', 'automation', 'data-processing', 'integration', 'notification']
    }
    
    return render(request, 'workflow_app/template_edit.html', context)

        
    # ... (other custom actions like activate, deactivate, etc.)
class WorkflowExecutionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for workflow executions - read-only
    """
    serializer_class = WorkflowExecutionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return WorkflowExecution.objects.filter(
            workflow__created_by=user
        ).select_related('workflow', 'triggered_by_user').prefetch_related('node_executions')

    @action(detail=True, methods=['get'])
    def logs(self, request, pk=None):
        """Get detailed execution logs"""
        execution = self.get_object()
        node_executions = execution.node_executions.all().order_by('execution_order', 'started_at')
        
        logs = []
        for node_exec in node_executions:
            logs.append({
                'timestamp': node_exec.started_at,
                'level': 'ERROR' if node_exec.status == 'failed' else 'INFO',
                'node_id': node_exec.node_id,
                'node_name': node_exec.node_name,
                'message': node_exec.error_message if node_exec.status == 'failed' else f"Node executed successfully",
                'duration_ms': node_exec.duration_ms,
                'input_data': node_exec.input_data,
                'output_data': node_exec.output_data if node_exec.status == 'success' else None
            })
        
        return Response({'logs': logs})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a running execution"""
        execution = self.get_object()
        
        if execution.status not in ['queued', 'running']:
            return Response(
                {'error': 'Can only cancel queued or running executions'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        execution.status = 'cancelled'
        execution.finished_at = timezone.now()
        execution.save()
        
        # TODO: Cancel the actual task if it's running
        
        return Response({'status': 'cancelled'})

class WorkflowVariableViewSet(viewsets.ModelViewSet):
    """
    ViewSet for workflow variables
    """
    serializer_class = WorkflowVariableSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        workflow_id = self.request.query_params.get('workflow')
        
        queryset = WorkflowVariable.objects.filter(created_by=user)
        
        if workflow_id:
            queryset = queryset.filter(workflow_id=workflow_id)
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class WorkflowWebhookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for workflow webhooks
    """
    serializer_class = WorkflowWebhookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return WorkflowWebhook.objects.filter(workflow__created_by=user)

    def perform_create(self, serializer):
        # Generate unique endpoint path if not provided
        if not serializer.validated_data.get('endpoint_path'):
            endpoint_path = f"/webhook/{uuid.uuid4().hex[:8]}"
            serializer.validated_data['endpoint_path'] = endpoint_path
        
        # Generate API key if required
        if serializer.validated_data.get('require_auth') and not serializer.validated_data.get('api_key'):
            api_key = f"wh_{uuid.uuid4().hex}"
            serializer.validated_data['api_key'] = api_key
        
        serializer.save()

class WorkflowTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for workflow templates
    """
    serializer_class = WorkflowTemplateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = WorkflowTemplate.objects.filter(
            Q(created_by=user) | Q(is_public=True)
        )
        
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset.order_by('-usage_count', 'name')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def use_template(self, request, pk=None):
        """Create a workflow from template"""
        template = self.get_object()
        
        # Increment usage count
        template.usage_count += 1
        template.save()
        
        # Create workflow from template
        workflow = Workflow.objects.create(
            name=f"{template.name} - {timezone.now().strftime('%Y%m%d_%H%M')}",
            description=template.description,
            definition=template.template_definition,
            created_by=request.user,
            status='draft'
        )
        
        serializer = WorkflowSerializer(workflow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# API Views for specific functionality
@login_required
def workflow_editor_view(request, workflow_id=None):
    """Render the workflow editor page"""
    workflow = None
    workflow_json = {'nodes': [], 'connections': []}
    
    if workflow_id:
        try:
            workflow = Workflow.objects.get(
                id=workflow_id,
                created_by=request.user
            )
            workflow_json = workflow.definition
        except Workflow.DoesNotExist:
            pass
    
    context = {
        'workflow': workflow,
        'workflow_json': json.dumps(workflow_json)
    }
    
    return render(request, 'workflow_app/workflow_editor.html', context)

@login_required
def webhook_receiver(request, endpoint_path):
    """Generic webhook receiver"""
    try:
        webhook = WorkflowWebhook.objects.get(
            endpoint_path=f"/{endpoint_path}",
            is_active=True
        )
        
        # Validate request method
        if request.method != webhook.http_method:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        
        # Validate authentication if required
        if webhook.require_auth:
            api_key = request.headers.get('X-API-Key') or request.GET.get('api_key')
            if api_key != webhook.api_key:
                return JsonResponse({'error': 'Invalid API key'}, status=401)
        
        # Validate IP if restricted
        if webhook.allowed_ips:
            client_ip = request.META.get('REMOTE_ADDR')
            if client_ip not in webhook.allowed_ips:
                return JsonResponse({'error': 'IP not allowed'}, status=403)
        
        # Get request data
        if request.content_type == 'application/json':
            try:
                input_data = json.loads(request.body)
            except json.JSONDecodeError:
                input_data = {}
        else:
            input_data = dict(request.POST)
        
        # Create execution
        execution = WorkflowExecution.objects.create(
            workflow=webhook.workflow,
            triggered_by='webhook',
            input_data=input_data,
            execution_context={'webhook_id': str(webhook.id)}
        )
        
        # Update webhook stats
        webhook.last_triggered_at = timezone.now()
        webhook.trigger_count += 1
        webhook.save()
        
        # Execute workflow asynchronously
        execute_workflow_task.delay(str(execution.id))
        
        return JsonResponse({
            'status': 'success',
            'execution_id': str(execution.id),
            'message': 'Workflow triggered successfully'
        })
        
    except WorkflowWebhook.DoesNotExist:
        return JsonResponse({'error': 'Webhook not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def workflow_list_view(request):
    """Display list of user's workflows"""
    workflows = Workflow.objects.filter(
        Q(created_by=request.user) | Q(shared_with=request.user)
    ).distinct().select_related('created_by').annotate(
        execution_count=Count('executions'),
        success_rate=Avg('executions__status')
    ).order_by('-updated_at')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        workflows = workflows.filter(status=status_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        workflows = workflows.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(workflows, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'workflows': page_obj,
        'status_filter': status_filter,
        'search_query': search_query,
        'total_workflows': workflows.count(),
        'active_workflows': workflows.filter(status='active').count(),
        'draft_workflows': workflows.filter(status='draft').count(),
    }
    
    return render(request, 'workflow_app/workflow_list.html', context)

@login_required
def workflow_detail_view(request, workflow_id):
    """Display detailed view of a workflow"""
    workflow = get_object_or_404(
        Workflow.objects.select_related('created_by').prefetch_related(
            'executions', 'variables', 'webhooks', 'shared_with'
        ),
        id=workflow_id,
        created_by=request.user
    )
    
    recent_executions = workflow.executions.all().order_by('-started_at')[:10]
    
    # Get execution statistics
    total_executions = workflow.executions.count()
    successful_executions = workflow.executions.filter(status='success').count()
    failed_executions = workflow.executions.filter(status='failed').count()
    success_rate = (successful_executions / total_executions * 100) if total_executions > 0 else 0
    
    # Get execution history for chart (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    execution_history = workflow.executions.filter(
        started_at__gte=thirty_days_ago
    ).extra(
        select={'day': 'date(started_at)'}
    ).values('day').annotate(
        total=Count('id'),
        successful=Count('id', filter=Q(status='success')),
        failed=Count('id', filter=Q(status='failed'))
    ).order_by('day')
    
    context = {
        'workflow': workflow,
        'recent_executions': recent_executions,
        'total_executions': total_executions,
        'successful_executions': successful_executions,
        'failed_executions': failed_executions,
        'success_rate': round(success_rate, 1),
        'execution_history': list(execution_history),
        'node_count': len(workflow.definition.get('nodes', [])),
        'connection_count': len(workflow.definition.get('connections', [])),
    }
    
    return render(request, 'workflow_app/workflow_detail.html', context)

@login_required
def dashboard_view(request):
    """Main dashboard view with overview statistics"""
    user = request.user
    
    # Get user's workflows
    workflows = Workflow.objects.filter(created_by=user)
    
    # Basic statistics
    total_workflows = workflows.count()
    active_workflows = workflows.filter(status='active').count()
    draft_workflows = workflows.filter(status='draft').count()
    inactive_workflows = workflows.filter(status='inactive').count()
    
    # Execution statistics
    executions = WorkflowExecution.objects.filter(workflow__created_by=user)
    total_executions = executions.count()
    successful_executions = executions.filter(status='success').count()
    failed_executions = executions.filter(status='failed').count()
    running_executions = executions.filter(status__in=['queued', 'running']).count()
    
    # Recent activity
    recent_executions = executions.select_related('workflow').order_by('-started_at')[:10]
    recent_workflows = workflows.order_by('-updated_at')[:5]
    
    # Execution trends (last 7 days)
    seven_days_ago = timezone.now() - timedelta(days=7)
    daily_executions = executions.filter(
        started_at__gte=seven_days_ago
    ).extra(
        select={'day': 'date(started_at)'}
    ).values('day').annotate(
        total=Count('id'),
        successful=Count('id', filter=Q(status='success')),
        failed=Count('id', filter=Q(status='failed'))
    ).order_by('day')
    
    # Top performing workflows
    top_workflows = workflows.annotate(
        execution_count=Count('executions'),
        success_rate=Avg('executions__status')
    ).filter(execution_count__gt=0).order_by('-execution_count')[:5]
    
    # System health indicators
    error_rate = (failed_executions / total_executions * 100) if total_executions > 0 else 0
    avg_execution_time = executions.filter(
        status='success',
        finished_at__isnull=False
    ).aggregate(
        avg_duration=Avg('duration_seconds')
    )['avg_duration'] or 0
    
    context = {
        'total_workflows': total_workflows,
        'active_workflows': active_workflows,
        'draft_workflows': draft_workflows,
        'inactive_workflows': inactive_workflows,
        'total_executions': total_executions,
        'successful_executions': successful_executions,
        'failed_executions': failed_executions,
        'running_executions': running_executions,
        'recent_executions': recent_executions,
        'recent_workflows': recent_workflows,
        'daily_executions': list(daily_executions),
        'top_workflows': top_workflows,
        'error_rate': round(error_rate, 1),
        'avg_execution_time': round(avg_execution_time / 1000, 2) if avg_execution_time else 0,
        'success_rate': round((successful_executions / total_executions * 100), 1) if total_executions > 0 else 0,
    }
    
    return render(request, 'workflow_app/dashboard.html', context)

@login_required
def template_list_view(request):
    """Display list of workflow templates"""
    templates = WorkflowTemplate.objects.filter(
        Q(created_by=request.user) | Q(is_public=True)
    ).select_related('created_by').order_by('-usage_count', 'name')
    
    # Filter by category if provided
    category_filter = request.GET.get('category')
    if category_filter:
        templates = templates.filter(category=category_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        templates = templates.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    # Get available categories
    categories = WorkflowTemplate.objects.values_list('category', flat=True).distinct()
    
    # Pagination
    paginator = Paginator(templates, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'templates': page_obj,
        'categories': categories,
        'category_filter': category_filter,
        'search_query': search_query,
        'total_templates': templates.count(),
        'public_templates': templates.filter(is_public=True).count(),
        'my_templates': templates.filter(created_by=request.user).count(),
    }
    
    return render(request, 'workflow_app/template_list.html', context)

@login_required
def execution_list_view(request):
    """Display list of workflow executions"""
    executions = WorkflowExecution.objects.filter(
        workflow__created_by=request.user
    ).select_related('workflow', 'triggered_by_user').prefetch_related(
        'node_executions'
    ).order_by('-started_at')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        executions = executions.filter(status=status_filter)
    
    # Filter by workflow if provided
    workflow_filter = request.GET.get('workflow')
    if workflow_filter:
        executions = executions.filter(workflow_id=workflow_filter)
    
    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            executions = executions.filter(started_at__date__gte=date_from)
        except ValueError:
            pass
    if date_to:
        try:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            executions = executions.filter(started_at__date__lte=date_to)
        except ValueError:
            pass
    
    # Get user's workflows for filter dropdown
    user_workflows = Workflow.objects.filter(created_by=request.user).values('id', 'name')
    
    # Pagination
    paginator = Paginator(executions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    total_executions = executions.count()
    successful_executions = executions.filter(status='success').count()
    failed_executions = executions.filter(status='failed').count()
    running_executions = executions.filter(status__in=['queued', 'running']).count()
    
    context = {
        'page_obj': page_obj,
        'executions': page_obj,
        'user_workflows': user_workflows,
        'status_filter': status_filter,
        'workflow_filter': workflow_filter,
        'date_from': date_from,
        'date_to': date_to,
        'total_executions': total_executions,
        'successful_executions': successful_executions,
        'failed_executions': failed_executions,
        'running_executions': running_executions,
        'success_rate': round((successful_executions / total_executions * 100), 1) if total_executions > 0 else 0,
    }
    
    return render(request, 'workflow_app/execution_list.html', context)

@login_required
def template_create_view(request):
    """Create a new workflow template"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        category = request.POST.get('category', 'general')
        is_public = request.POST.get('is_public') == 'on'
        workflow_id = request.POST.get('workflow_id')
        
        if name and workflow_id:
            try:
                workflow = Workflow.objects.get(id=workflow_id, created_by=request.user)
                template = WorkflowTemplate.objects.create(
                    name=name,
                    description=description,
                    category=category,
                    template_definition=workflow.definition,
                    is_public=is_public,
                    created_by=request.user
                )
                return redirect('workflow_app:template_detail', template_id=template.id)
            except Workflow.DoesNotExist:
                pass
    
    # Get user's workflows for template creation
    workflows = Workflow.objects.filter(created_by=request.user).values('id', 'name', 'description')
    
    context = {
        'workflows': workflows,
        'categories': ['general', 'automation', 'data-processing', 'integration', 'notification']
    }
    
    return render(request, 'workflow_app/template_create.html', context)

@login_required
def template_detail_view(request, template_id):
    """Display detailed view of a workflow template"""
    template = get_object_or_404(
        WorkflowTemplate.objects.select_related('created_by'),
        id=template_id
    )
    
    # Check if user can view this template
    if not template.is_public and template.created_by != request.user:
        return redirect('workflow_app:template_list')
    
    context = {
        'template': template,
        'can_edit': template.created_by == request.user,
        'node_count': len(template.template_definition.get('nodes', [])),
        'connection_count': len(template.template_definition.get('connections', [])),
    }
    
    return render(request, 'workflow_app/template_detail.html', context)

@login_required
def template_edit_view(request, template_id):
    """Edit a workflow template"""
    template = get_object_or_404(
        WorkflowTemplate,
        id=template_id,
        created_by=request.user
    )
    
    if request.method == 'POST':
        template.name = request.POST.get('name', template.name)
        template.description = request.POST.get('description', template.description)
        template.category = request.POST.get('category', template.category)
        template.is_public = request.POST.get('is_public') == 'on'
        template.save()
        
        return redirect('workflow_app:template_detail', template_id=template.id)
    
    context = {
        'template': template,
        'categories': ['general', 'automation', 'data-processing', 'integration', 'notification']
    }
    
    return render(request, 'workflow_app/template_edit.html', context)
