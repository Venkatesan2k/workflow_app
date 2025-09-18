/**
 * Complete Workflow Editor - N8N-like drag & drop workflow builder
 */
class WorkflowEditor {
    constructor(options = {}) {
        this.workflowId = options.workflowId || null;
        this.workflowData = options.workflowData || { nodes: [], connections: [] };
        this.csrfToken = options.csrfToken;
        this.apiBaseUrl = options.apiBaseUrl || '/workflow/api/workflows/';
        
        // Editor state
        this.selectedNode = null;
        this.selectedConnection = null;
        this.isDragging = false;
        this.isPanning = false;
        this.isConnecting = false;
        this.connectionStart = null;
        this.dragOffset = { x: 0, y: 0 };
        this.lastMousePos = { x: 0, y: 0 };
        this.nodeCounter = 0;
        this.clipboard = null;
        
        // Canvas state
        this.canvasOffset = { x: 0, y: 0 };
        this.zoomLevel = 1;
        this.gridSize = 20;
        
        // Node types registry
        this.nodeTypes = new Map();
        this.nodes = new Map();
        this.connections = new Map();
        
        this.init();
    }
    
    async init() {
        this.setupCanvas();
        this.setupEventListeners();
        await this.loadNodeTypes();
        this.renderNodePalette();
        this.loadWorkflow();
        this.setupKeyboardShortcuts();
        this.updateZoomDisplay();
    }
    
    setupCanvas() {
        const canvas = document.getElementById('workflow-canvas');
        if (!canvas) return;
        
        // Create canvas layers
        canvas.innerHTML = `
            <div class="canvas-grid"></div>
            <svg class="connections-layer" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1;">
                <defs>
                    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                        <polygon points="0 0, 10 3.5, 0 7" fill="#3b82f6" />
                    </marker>
                </defs>
            </svg>
            <div class="nodes-layer" style="position: relative; z-index: 2;"></div>
        `;
        
        this.connectionsLayer = canvas.querySelector('.connections-layer');
        this.nodesLayer = canvas.querySelector('.nodes-layer');
        this.gridLayer = canvas.querySelector('.canvas-grid');
        
        this.updateGrid();
    }
    
    setupEventListeners() {
        // Toolbar events
        document.getElementById('save-btn')?.addEventListener('click', () => this.saveWorkflow());
        document.getElementById('test-btn')?.addEventListener('click', () => this.testWorkflow());
        document.getElementById('deploy-btn')?.addEventListener('click', () => this.deployWorkflow());
        
        // Zoom controls
        document.getElementById('zoom-in')?.addEventListener('click', () => this.zoomIn());
        document.getElementById('zoom-out')?.addEventListener('click', () => this.zoomOut());
        document.getElementById('zoom-fit')?.addEventListener('click', () => this.fitToScreen());
        
        // Canvas controls
        document.getElementById('center-canvas')?.addEventListener('click', () => this.centerCanvas());
        document.getElementById('clear-canvas')?.addEventListener('click', () => this.clearCanvas());
        
        // Canvas events
        const canvas = document.getElementById('workflow-canvas');
        if (canvas) {
            canvas.addEventListener('mousedown', (e) => this.onCanvasMouseDown(e));
            canvas.addEventListener('mousemove', (e) => this.onCanvasMouseMove(e));
            canvas.addEventListener('mouseup', (e) => this.onCanvasMouseUp(e));
            canvas.addEventListener('wheel', (e) => this.onCanvasWheel(e));
            canvas.addEventListener('contextmenu', (e) => this.onCanvasContextMenu(e));
            canvas.addEventListener('dragover', (e) => e.preventDefault());
            canvas.addEventListener('drop', (e) => this.onCanvasDrop(e));
        }
        
        // Node search
        document.getElementById('node-search')?.addEventListener('input', (e) => {
            this.filterNodes(e.target.value);
        });
        
        // Category toggles
        document.querySelectorAll('.category-header').forEach(header => {
            header.addEventListener('click', () => {
                const category = header.parentElement;
                category.classList.toggle('collapsed');
            });
        });
        
        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', () => this.switchTab(btn.dataset.tab));
        });
        
        // Properties panel
        document.getElementById('close-panel')?.addEventListener('click', () => {
            this.deselectAll();
        });
        
        // Workflow name editing
        const nameInput = document.getElementById('workflow-name');
        if (nameInput) {
            nameInput.addEventListener('blur', () => this.updateWorkflowName());
            nameInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') nameInput.blur();
            });
        }
        
        // Back button
        document.getElementById('back-btn')?.addEventListener('click', () => {
            this.goBack();
        });
        
        // Menu actions
        document.getElementById('export-btn')?.addEventListener('click', () => this.exportWorkflow());
        document.getElementById('import-btn')?.addEventListener('click', () => this.importWorkflow());
        document.getElementById('duplicate-btn')?.addEventListener('click', () => this.duplicateWorkflow());
        
        // Context menu
        document.addEventListener('click', () => this.hideContextMenu());
    }
    
    async loadNodeTypes() {
        try {
            const response = await fetch('/workflow/api/node-types/', {
                headers: {
                    'X-CSRFToken': this.csrfToken
                }
            });
            
            if (response.ok) {
                const nodeTypes = await response.json();
                nodeTypes.forEach(nodeType => {
                    this.nodeTypes.set(nodeType.name, nodeType);
                });
            } else {
                this.loadDefaultNodeTypes();
            }
        } catch (error) {
            console.error('Failed to load node types:', error);
            this.loadDefaultNodeTypes();
        }
    }
    
    loadDefaultNodeTypes() {
        const defaultTypes = [
            {
                name: 'webhook_trigger',
                display_name: 'Webhook',
                category: 'trigger',
                icon: 'fa-globe',
                color: '#10b981',
                description: 'Trigger workflow via HTTP webhook',
                config_schema: {
                    fields: [
                        { name: 'method', type: 'select', options: ['GET', 'POST', 'PUT', 'DELETE'], default: 'POST', label: 'HTTP Method' },
                        { name: 'path', type: 'text', placeholder: '/webhook/my-endpoint', label: 'Endpoint Path' }
                    ]
                }
            },
            {
                name: 'schedule_trigger',
                display_name: 'Schedule',
                category: 'trigger',
                icon: 'fa-clock',
                color: '#f59e0b',
                description: 'Trigger workflow on schedule',
                config_schema: {
                    fields: [
                        { name: 'cron', type: 'text', placeholder: '0 9 * * *', label: 'Cron Expression' },
                        { name: 'timezone', type: 'select', options: ['UTC', 'America/New_York', 'Europe/London'], default: 'UTC', label: 'Timezone' }
                    ]
                }
            },
            {
                name: 'manual_trigger',
                display_name: 'Manual',
                category: 'trigger',
                icon: 'fa-hand-pointer',
                color: '#6366f1',
                description: 'Manually trigger workflow',
                config_schema: { fields: [] }
            },
            {
                name: 'http_request',
                display_name: 'HTTP Request',
                category: 'data',
                icon: 'fa-exchange-alt',
                color: '#3b82f6',
                description: 'Make HTTP requests to APIs',
                config_schema: {
                    fields: [
                        { name: 'method', type: 'select', options: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'], default: 'GET', label: 'Method' },
                        { name: 'url', type: 'text', placeholder: 'https://api.example.com/data', label: 'URL', required: true },
                        { name: 'headers', type: 'textarea', placeholder: '{"Content-Type": "application/json"}', label: 'Headers' },
                        { name: 'body', type: 'textarea', placeholder: 'Request body', label: 'Body' },
                        { name: 'timeout', type: 'number', default: 30, label: 'Timeout (seconds)' }
                    ]
                }
            },
            {
                name: 'database_query',
                display_name: 'Database Query',
                category: 'data',
                icon: 'fa-database',
                color: '#8b5cf6',
                description: 'Query database for data',
                config_schema: {
                    fields: [
                        { name: 'query_type', type: 'select', options: ['SELECT', 'INSERT', 'UPDATE', 'DELETE'], default: 'SELECT', label: 'Query Type' },
                        { name: 'table_name', type: 'text', placeholder: 'users', label: 'Table Name', required: true },
                        { name: 'conditions', type: 'text', placeholder: 'active = true', label: 'WHERE Conditions' },
                        { name: 'fields', type: 'text', placeholder: '*', default: '*', label: 'Fields' },
                        { name: 'limit', type: 'number', default: 100, label: 'Limit' }
                    ]
                }
            },
            {
                name: 'data_transform',
                display_name: 'Transform Data',
                category: 'transform',
                icon: 'fa-cogs',
                color: '#059669',
                description: 'Transform and map data',
                config_schema: {
                    fields: [
                        { name: 'transform_type', type: 'select', options: ['map', 'filter', 'aggregate'], default: 'map', label: 'Transform Type' },
                        { name: 'field_mappings', type: 'textarea', placeholder: '[{"source": "old_field", "target": "new_field"}]', label: 'Field Mappings' }
                    ]
                }
            },
            {
                name: 'json_parser',
                display_name: 'JSON Parser',
                category: 'transform',
                icon: 'fa-code',
                color: '#dc2626',
                description: 'Parse and manipulate JSON data',
                config_schema: {
                    fields: [
                        { name: 'operation', type: 'select', options: ['parse', 'stringify', 'extract'], default: 'parse', label: 'Operation' },
                        { name: 'json_field', type: 'text', placeholder: 'data', default: 'data', label: 'JSON Field' },
                        { name: 'fields', type: 'textarea', placeholder: '["field1", "field2.nested"]', label: 'Fields to Extract' }
                    ]
                }
            },
            {
                name: 'condition',
                display_name: 'Condition',
                category: 'condition',
                icon: 'fa-code-branch',
                color: '#ef4444',
                description: 'Branch workflow based on conditions',
                config_schema: {
                    fields: [
                        { name: 'field', type: 'text', placeholder: 'data.status', label: 'Field Path', required: true },
                        { name: 'operator', type: 'select', options: ['equals', 'not_equals', 'greater_than', 'less_than', 'contains', 'not_contains', 'is_empty', 'is_not_empty'], default: 'equals', label: 'Operator' },
                        { name: 'value', type: 'text', placeholder: 'expected value', label: 'Value' },
                        { name: 'logic_operator', type: 'select', options: ['AND', 'OR'], default: 'AND', label: 'Logic Operator' }
                    ]
                }
            },
            {
                name: 'switch',
                display_name: 'Switch',
                category: 'condition',
                icon: 'fa-random',
                color: '#f59e0b',
                description: 'Route to different paths based on value',
                config_schema: {
                    fields: [
                        { name: 'switch_field', type: 'text', placeholder: 'data.type', label: 'Switch Field', required: true },
                        { name: 'cases', type: 'textarea', placeholder: '{"case1": "output1", "case2": "output2", "default": "default_output"}', label: 'Cases (JSON)' }
                    ]
                }
            },
            {
                name: 'email_send',
                display_name: 'Send Email',
                category: 'action',
                icon: 'fa-envelope',
                color: '#06b6d4',
                description: 'Send email notifications',
                config_schema: {
                    fields: [
                        { name: 'to', type: 'text', placeholder: 'user@example.com', label: 'To', required: true },
                        { name: 'subject', type: 'text', placeholder: 'Email Subject', label: 'Subject', required: true },
                        { name: 'body', type: 'textarea', placeholder: 'Email body content...', label: 'Body', required: true },
                        { name: 'from_email', type: 'text', placeholder: 'noreply@example.com', label: 'From Email' }
                    ]
                }
            },
            {
                name: 'slack_notification',
                display_name: 'Slack Notification',
                category: 'action',
                icon: 'fa-slack',
                color: '#4a154b',
                description: 'Send Slack notifications',
                config_schema: {
                    fields: [
                        { name: 'webhook_url', type: 'text', placeholder: 'https://hooks.slack.com/...', label: 'Webhook URL', required: true },
                        { name: 'message', type: 'textarea', placeholder: 'Notification message', label: 'Message', required: true },
                        { name: 'channel', type: 'text', placeholder: '#general', label: 'Channel' },
                        { name: 'username', type: 'text', placeholder: 'Workflow Bot', default: 'Workflow Bot', label: 'Username' }
                    ]
                }
            },
            {
                name: 'delay',
                display_name: 'Delay',
                category: 'action',
                icon: 'fa-clock',
                color: '#f59e0b',
                description: 'Add delay to workflow execution',
                config_schema: {
                    fields: [
                        { name: 'delay_seconds', type: 'number', default: 1, label: 'Delay (seconds)', required: true },
                        { name: 'delay_type', type: 'select', options: ['fixed', 'random'], default: 'fixed', label: 'Delay Type' },
                        { name: 'min_delay', type: 'number', default: 1, label: 'Min Delay (for random)' },
                        { name: 'max_delay', type: 'number', default: 5, label: 'Max Delay (for random)' }
                    ]
                }
            },
            {
                name: 'database_save',
                display_name: 'Save to Database',
                category: 'output',
                icon: 'fa-save',
                color: '#059669',
                description: 'Save data to database',
                config_schema: {
                    fields: [
                        { name: 'table_name', type: 'text', placeholder: 'table_name', label: 'Table Name', required: true },
                        { name: 'operation', type: 'select', options: ['insert', 'update', 'upsert'], default: 'insert', label: 'Operation' },
                        { name: 'where_conditions', type: 'textarea', placeholder: '{"id": "{{input.id}}"}', label: 'WHERE Conditions (JSON)' },
                        { name: 'unique_columns', type: 'text', placeholder: 'id,email', label: 'Unique Columns (for upsert)' }
                    ]
                }
            },
            {
                name: 'file_export',
                display_name: 'Export to File',
                category: 'output',
                icon: 'fa-download',
                color: '#7c2d12',
                description: 'Export data to file',
                config_schema: {
                    fields: [
                        { name: 'file_path', type: 'text', placeholder: '/tmp/export.json', label: 'File Path', required: true },
                        { name: 'format', type: 'select', options: ['json', 'csv', 'txt'], default: 'json', label: 'Format' }
                    ]
                }
            }
        ];
        
        defaultTypes.forEach(nodeType => {
            this.nodeTypes.set(nodeType.name, nodeType);
        });
    }
    
    renderNodePalette() {
        const categories = ['trigger', 'data', 'transform', 'condition', 'action', 'output'];
        
        categories.forEach(category => {
            const categoryElement = document.querySelector(`[data-category="${category}"] .category-nodes`);
            if (!categoryElement) return;
            
            categoryElement.innerHTML = '';
            
            Array.from(this.nodeTypes.values())
                .filter(nodeType => nodeType.category === category)
                .forEach(nodeType => {
                    const nodeElement = this.createPaletteNode(nodeType);
                    categoryElement.appendChild(nodeElement);
                });
        });
    }
    
    createPaletteNode(nodeType) {
        const nodeElement = document.createElement('div');
        nodeElement.className = 'palette-node';
        nodeElement.draggable = true;
        nodeElement.dataset.nodeType = nodeType.name;
        nodeElement.title = nodeType.description;
        
        nodeElement.innerHTML = `
            <div class="node-icon" style="background-color: ${nodeType.color}">
                <i class="fas ${nodeType.icon}"></i>
            </div>
            <span class="node-name">${nodeType.display_name}</span>
        `;
        
        nodeElement.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('text/plain', nodeType.name);
            e.dataTransfer.setData('application/json', JSON.stringify(nodeType));
            nodeElement.classList.add('dragging');
        });
        
        nodeElement.addEventListener('dragend', () => {
            nodeElement.classList.remove('dragging');
        });
        
        return nodeElement;
    }
    
    onCanvasDrop(e) {
        e.preventDefault();
        const nodeTypeName = e.dataTransfer.getData('text/plain');
        const nodeType = this.nodeTypes.get(nodeTypeName);
        
        if (!nodeType) return;
        
        const rect = e.currentTarget.getBoundingClientRect();
        const x = (e.clientX - rect.left - this.canvasOffset.x) / this.zoomLevel;
        const y = (e.clientY - rect.top - this.canvasOffset.y) / this.zoomLevel;
        
        // Snap to grid
        const snappedX = Math.round(x / this.gridSize) * this.gridSize;
        const snappedY = Math.round(y / this.gridSize) * this.gridSize;
        
        this.createNode(nodeType, { x: snappedX, y: snappedY });
    }
    
    createNode(nodeType, position) {
        const nodeId = `node_${++this.nodeCounter}`;
        const node = {
            id: nodeId,
            type: nodeType.name,
            name: nodeType.display_name,
            position: position,
            config: this.getDefaultConfig(nodeType),
            inputs: this.getNodeInputs(nodeType),
            outputs: this.getNodeOutputs(nodeType)
        };
        
        this.nodes.set(nodeId, node);
        this.renderNode(node);
        this.selectNode(nodeId);
        this.markDirty();
        
        return nodeId;
    }
    
    getDefaultConfig(nodeType) {
        const config = {};
        if (nodeType.config_schema && nodeType.config_schema.fields) {
            nodeType.config_schema.fields.forEach(field => {
                if (field.default !== undefined) {
                    config[field.name] = field.default;
                }
            });
        }
        return config;
    }
    
    getNodeInputs(nodeType) {
        if (nodeType.category === 'trigger') {
            return [];
        }
        return ['input'];
    }
    
    getNodeOutputs(nodeType) {
        if (nodeType.name === 'condition') {
            return ['true', 'false'];
        } else if (nodeType.name === 'switch') {
            return ['output'];
        }
        return ['output'];
    }
    
    renderNode(node) {
        const nodeType = this.nodeTypes.get(node.type);
        if (!nodeType) return;
        
        let nodeElement = this.nodesLayer.querySelector(`[data-node-id="${node.id}"]`);
        
        if (!nodeElement) {
            nodeElement = document.createElement('div');
            nodeElement.className = 'workflow-node';
            nodeElement.dataset.nodeId = node.id;
            nodeElement.dataset.nodeType = node.type;
            this.nodesLayer.appendChild(nodeElement);
        }
        
        const isSelected = this.selectedNode === node.id;
        nodeElement.className = `workflow-node ${isSelected ? 'selected' : ''}`;
        
        nodeElement.style.left = `${node.position.x}px`;
        nodeElement.style.top = `${node.position.y}px`;
        
        nodeElement.innerHTML = `
            <div class="node-header">
                <div class="node-icon" style="background-color: ${nodeType.color}">
                    <i class="fas ${nodeType.icon}"></i>
                </div>
                <div class="node-title">${node.name}</div>
                <div class="node-status"></div>
            </div>
            <div class="node-body">
                ${this.getNodeDescription(node, nodeType)}
            </div>
            <div class="node-handles">
                ${node.inputs.map((input, index) => `
                    <div class="node-handle input" data-handle="${input}" data-index="${index}" style="left: -6px; top: ${50 + index * 20}%;"></div>
                `).join('')}
                ${node.outputs.map((output, index) => `
                    <div class="node-handle output" data-handle="${output}" data-index="${index}" style="right: -6px; top: ${50 + index * 20}%;"></div>
                `).join('')}
            </div>
        `;
        
        // Add event listeners
        nodeElement.addEventListener('mousedown', (e) => this.onNodeMouseDown(e, node.id));
        nodeElement.addEventListener('click', (e) => this.onNodeClick(e, node.id));
        nodeElement.addEventListener('contextmenu', (e) => this.onNodeContextMenu(e, node.id));
        
        // Handle events
        nodeElement.querySelectorAll('.node-handle').forEach(handle => {
            handle.addEventListener('mousedown', (e) => this.onHandleMouseDown(e, node.id, handle));
        });
    }
    
    getNodeDescription(node, nodeType) {
        if (node.config && Object.keys(node.config).length > 0) {
            const firstKey = Object.keys(node.config)[0];
            const value = node.config[firstKey];
            if (value) {
                return `${firstKey}: ${String(value).substring(0, 30)}${String(value).length > 30 ? '...' : ''}`;
            }
        }
        return nodeType.description || 'Click to configure';
    }
    
    onNodeMouseDown(e, nodeId) {
        e.stopPropagation();
        
        if (!this.selectedNode || this.selectedNode !== nodeId) {
            this.selectNode(nodeId);
        }
        
        this.isDragging = true;
        this.lastMousePos = { x: e.clientX, y: e.clientY };
        
        const nodeElement = e.currentTarget;
        const rect = nodeElement.getBoundingClientRect();
        this.dragOffset = {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top
        };
    }
    
    onNodeClick(e, nodeId) {
        e.stopPropagation();
        this.selectNode(nodeId);
    }
    
    onNodeContextMenu(e, nodeId) {
        e.preventDefault();
        this.selectNode(nodeId);
        this.showContextMenu(e.clientX, e.clientY, 'node', nodeId);
    }
    
    onHandleMouseDown(e, nodeId, handleElement) {
        e.stopPropagation();
        
        const handleType = handleElement.classList.contains('input') ? 'input' : 'output';
        const handleName = handleElement.getAttribute('data-handle');
        
        if (handleType === 'output') {
            this.startConnection(nodeId, handleName, e);
        }
    }
    
    startConnection(sourceNodeId, sourceHandle, e) {
        this.isConnecting = true;
        this.connectionStart = {
            nodeId: sourceNodeId,
            handle: sourceHandle,
            position: this.getHandlePosition(sourceNodeId, sourceHandle, 'output')
        };
        
        this.createTempConnection();
    }
    
    createTempConnection() {
        let tempLine = this.connectionsLayer.querySelector('.temp-connection');
        if (!tempLine) {
            tempLine = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            tempLine.setAttribute('class', 'temp-connection');
            tempLine.setAttribute('stroke', '#999');
            tempLine.setAttribute('stroke-width', '2');
            tempLine.setAttribute('stroke-dasharray', '5,5');
            tempLine.setAttribute('fill', 'none');
            this.connectionsLayer.appendChild(tempLine);
        }
    }
    
    updateTempConnection(e) {
        const tempLine = this.connectionsLayer.querySelector('.temp-connection');
        if (!tempLine || !this.connectionStart) return;
        
        const rect = document.getElementById('workflow-canvas').getBoundingClientRect();
        const start = this.connectionStart.position;
        const end = {
            x: (e.clientX - rect.left - this.canvasOffset.x) / this.zoomLevel,
            y: (e.clientY - rect.top - this.canvasOffset.y) / this.zoomLevel
        };
        
        const path = this.createConnectionPath(start, end);
        tempLine.setAttribute('d', path);
    }
    
    finishConnection(e) {
        this.isConnecting = false;
        
        // Remove temporary connection
        const tempLine = this.connectionsLayer.querySelector('.temp-connection');
        if (tempLine) {
            tempLine.remove();
        }
        
        // Find target handle
        const target = e.target;
        if (target && target.classList.contains('node-handle') && target.classList.contains('input')) {
            const targetNodeId = target.closest('.workflow-node').getAttribute('data-node-id');
            const targetHandle = target.getAttribute('data-handle');
            
            if (this.connectionStart && targetNodeId !== this.connectionStart.nodeId) {
                this.addConnection(this.connectionStart.nodeId, this.connectionStart.handle, targetNodeId, targetHandle);
            }
        }
        
        this.connectionStart = null;
    }
    
    addConnection(sourceNodeId, sourceHandle, targetNodeId, targetHandle) {
        const connectionId = `connection_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        const connection = {
            id: connectionId,
            source: sourceNodeId,
            sourceHandle: sourceHandle,
            target: targetNodeId,
            targetHandle: targetHandle
        };
        
        this.connections.set(connectionId, connection);
        this.renderConnection(connection);
        this.markDirty();
        
        return connectionId;
    }
    
    renderConnection(connection) {
        const sourceNode = this.nodes.get(connection.source);
        const targetNode = this.nodes.get(connection.target);
        
        if (!sourceNode || !targetNode) return;
        
        const sourcePos = this.getHandlePosition(connection.source, connection.sourceHandle, 'output');
        const targetPos = this.getHandlePosition(connection.target, connection.targetHandle, 'input');
        
        let connectionElement = this.connectionsLayer.querySelector(`[data-connection-id="${connection.id}"]`);
        
        if (!connectionElement) {
            connectionElement = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            connectionElement.setAttribute('data-connection-id', connection.id);
            connectionElement.setAttribute('class', 'connection-path');
            connectionElement.setAttribute('marker-end', 'url(#arrowhead)');
            connectionElement.setAttribute('stroke', '#3b82f6');
            connectionElement.setAttribute('stroke-width', '2');
            connectionElement.setAttribute('fill', 'none');
            connectionElement.style.cursor = 'pointer';
            this.connectionsLayer.appendChild(connectionElement);
            
            connectionElement.addEventListener('click', (e) => this.onConnectionClick(e, connection.id));
        }
        
        const isSelected = this.selectedConnection === connection.id;
        connectionElement.setAttribute('stroke', isSelected ? '#10b981' : '#3b82f6');
        connectionElement.setAttribute('stroke-width', isSelected ? '3' : '2');
        
        const path = this.createConnectionPath(sourcePos, targetPos);
        connectionElement.setAttribute('d', path);
    }
    
    getHandlePosition(nodeId, handleName, type) {
        const nodeElement = this.nodesLayer.querySelector(`[data-node-id="${nodeId}"]`);
        if (!nodeElement) return { x: 0, y: 0 };
        
        const handle = nodeElement.querySelector(`.node-handle.${type}[data-handle="${handleName}"]`);
        if (!handle) return { x: 0, y: 0 };
        
        const nodeRect = nodeElement.getBoundingClientRect();
        const handleRect = handle.getBoundingClientRect();
        const canvasRect = document.getElementById('workflow-canvas').getBoundingClientRect();
        
        return {
            x: (handleRect.left + handleRect.width / 2 - canvasRect.left - this.canvasOffset.x) / this.zoomLevel,
            y: (handleRect.top + handleRect.height / 2 - canvasRect.top - this.canvasOffset.y) / this.zoomLevel
        };
    }
    
    createConnectionPath(start, end) {
        const dx = end.x - start.x;
        const dy = end.y - start.y;
        const controlOffset = Math.max(50, Math.abs(dx) * 0.5);
        
        return `M ${start.x} ${start.y} C ${start.x + controlOffset} ${start.y}, ${end.x - controlOffset} ${end.y}, ${end.x} ${end.y}`;
    }
    
    onConnectionClick(e, connectionId) {
        e.stopPropagation();
        this.selectConnection(connectionId);
    }
    
    selectNode(nodeId) {
        this.deselectAll();
        this.selectedNode = nodeId;
        
        const nodeElement = this.nodesLayer.querySelector(`[data-node-id="${nodeId}"]`);
        if (nodeElement) {
            nodeElement.classList.add('selected');
        }
        
        this.showNodeProperties(nodeId);
    }
    
    selectConnection(connectionId) {
        this.deselectAll();
        this.selectedConnection = connectionId;
        this.renderConnection(this.connections.get(connectionId));
        this.showConnectionProperties(connectionId);
    }
    
    deselectAll() {
        // Deselect nodes
        this.nodesLayer.querySelectorAll('.workflow-node.selected').forEach(node => {
            node.classList.remove('selected');
        });
        
        // Deselect connections
        this.connections.forEach(connection => {
            this.renderConnection(connection);
        });
        
        this.selectedNode = null;
        this.selectedConnection = null;
        this.hideProperties();
    }
    
    showNodeProperties(nodeId) {
        const node = this.nodes.get(nodeId);
        const nodeType = this.nodeTypes.get(node.type);
        
        if (!node || !nodeType) return;
        
        document.getElementById('no-selection').style.display = 'none';
        document.getElementById('node-properties').style.display = 'block';
        document.getElementById('connection-properties').style.display = 'none';
        document.getElementById('panel-title').textContent = node.name;
        
        const propertiesContainer = document.getElementById('node-properties');
        propertiesContainer.innerHTML = this.generatePropertiesForm(node, nodeType);
        
        // Add event listeners to form fields
        propertiesContainer.querySelectorAll('input, select, textarea').forEach(field => {
            field.addEventListener('change', () => this.updateNodeConfig(nodeId, field));
            field.addEventListener('input', () => this.updateNodeConfig(nodeId, field));
        });
    }
    
    showConnectionProperties(connectionId) {
        const connection = this.connections.get(connectionId);
        if (!connection) return;
        
        document.getElementById('no-selection').style.display = 'none';
        document.getElementById('node-properties').style.display = 'none';
        document.getElementById('connection-properties').style.display = 'block';
        document.getElementById('panel-title').textContent = 'Connection Properties';
        
        const propertiesContainer = document.getElementById('connection-properties');
        propertiesContainer.innerHTML = `
            <div class="form-section">
                <h4>Connection Details</h4>
                <div class="form-group">
                    <label>Source Node</label>
                    <input type="text" value="${this.nodes.get(connection.source)?.name || connection.source}" readonly>
                </div>
                <div class="form-group">
                    <label>Source Handle</label>
                    <input type="text" value="${connection.sourceHandle}" readonly>
                </div>
                <div class="form-group">
                    <label>Target Node</label>
                    <input type="text" value="${this.nodes.get(connection.target)?.name || connection.target}" readonly>
                </div>
                <div class="form-group">
                    <label>Target Handle</label>
                    <input type="text" value="${connection.targetHandle}" readonly>
                </div>
                <div class="form-group">
                    <button class="btn btn-danger btn-sm" onclick="workflowEditor.deleteConnection('${connectionId}')">
                        <i class="fas fa-trash"></i> Delete Connection
                    </button>
                </div>
            </div>
        `;
    }
    
    generatePropertiesForm(node, nodeType) {
        let html = `
            <div class="form-section">
                <h4>General</h4>
                <div class="form-group">
                    <label for="node-name">Node Name</label>
                    <input type="text" id="node-name" data-field="name" value="${node.name}" class="form-control">
                </div>
                <div class="form-group">
                    <label for="node-description">Description</label>
                    <textarea id="node-description" data-field="description" class="form-control" rows="2" placeholder="Optional description">${node.description || ''}</textarea>
                </div>
            </div>
        `;
        
        if (nodeType.config_schema && nodeType.config_schema.fields) {
            html += `<div class="form-section"><h4>Configuration</h4>`;
            
            nodeType.config_schema.fields.forEach(field => {
                const value = node.config[field.name] || field.default || '';
                html += this.generateFormField(field, value);
            });
            
            html += `</div>`;
        }
        
        // Advanced section
        html += `
            <div class="form-section">
                <h4>Advanced</h4>
                <div class="form-group">
                    <label>
                        <input type="checkbox" data-field="continue_on_error" ${node.continue_on_error ? 'checked' : ''}>
                        Continue on Error
                    </label>
                    <small class="form-help">Continue workflow execution even if this node fails</small>
                </div>
                <div class="form-group">
                    <label for="node-timeout">Timeout (seconds)</label>
                    <input type="number" id="node-timeout" data-field="timeout" value="${node.timeout || 30}" class="form-control" min="1" max="3600">
                </div>
                <div class="form-group">
                    <button class="btn btn-danger btn-sm" onclick="workflowEditor.deleteNode('${node.id}')">
                        <i class="fas fa-trash"></i> Delete Node
                    </button>
                </div>
            </div>
        `;
        
        return html;
    }
    
    generateFormField(field, value) {
        const fieldId = `field-${field.name}`;
        const required = field.required ? 'required' : '';
        const placeholder = field.placeholder || '';
        
        let html = `<div class="form-group">`;
        html += `<label for="${fieldId}">${field.label || this.formatFieldName(field.name)}</label>`;
        
        switch (field.type) {
            case 'text':
                html += `<input type="text" id="${fieldId}" data-field="${field.name}" value="${value}" placeholder="${placeholder}" class="form-control" ${required}>`;
                break;
            case 'number':
                const min = field.min !== undefined ? `min="${field.min}"` : '';
                const max = field.max !== undefined ? `max="${field.max}"` : '';
                const step = field.step !== undefined ? `step="${field.step}"` : '';
                html += `<input type="number" id="${fieldId}" data-field="${field.name}" value="${value}" placeholder="${placeholder}" class="form-control" ${min} ${max} ${step} ${required}>`;
                break;
            case 'textarea':
                const rows = field.rows || 3;
                html += `<textarea id="${fieldId}" data-field="${field.name}" placeholder="${placeholder}" class="form-control" rows="${rows}" ${required}>${value}</textarea>`;
                break;
            case 'select':
                html += `<select id="${fieldId}" data-field="${field.name}" class="form-control" ${required}>`;
                if (!field.required) {
                    html += `<option value="">-- Select --</option>`;
                }
                field.options.forEach(option => {
                    const selected = value === option ? 'selected' : '';
                    html += `<option value="${option}" ${selected}>${option}</option>`;
                });
                html += `</select>`;
                break;
            case 'checkbox':
                const checked = value === true || value === 'true' ? 'checked' : '';
                html += `<label class="checkbox-label">
                    <input type="checkbox" id="${fieldId}" data-field="${field.name}" ${checked}>
                    ${field.label || this.formatFieldName(field.name)}
                </label>`;
                break;
            default:
                html += `<input type="text" id="${fieldId}" data-field="${field.name}" value="${value}" placeholder="${placeholder}" class="form-control" ${required}>`;
        }
        
        if (field.help) {
            html += `<small class="form-help">${field.help}</small>`;
        }
        
        html += `</div>`;
        return html;
    }
    
    formatFieldName(name) {
        return name.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
    }
    
    updateNodeConfig(nodeId, field) {
        const node = this.nodes.get(nodeId);
        if (!node) return;
        
        const fieldName = field.dataset.field;
        let value = field.value;
        
        if (field.type === 'checkbox') {
            value = field.checked;
        } else if (field.type === 'number') {
            value = value ? Number(value) : null;
        }
        
        if (fieldName === 'name') {
            node.name = value;
            // Update node title in DOM
            const nodeElement = this.nodesLayer.querySelector(`[data-node-id="${nodeId}"] .node-title`);
            if (nodeElement) {
                nodeElement.textContent = value;
            }
        } else if (fieldName === 'description') {
            node.description = value;
        } else if (fieldName === 'continue_on_error') {
            node.continue_on_error = value;
        } else if (fieldName === 'timeout') {
            node.timeout = value;
        } else {
            // Configuration field
            if (!node.config) {
                node.config = {};
            }
            node.config[fieldName] = value;
            
            // Update node description
            const nodeType = this.nodeTypes.get(node.type);
            const bodyElement = this.nodesLayer.querySelector(`[data-node-id="${nodeId}"] .node-body`);
            if (bodyElement) {
                bodyElement.textContent = this.getNodeDescription(node, nodeType);
            }
        }
        
        this.markDirty();
    }
    
    hideProperties() {
        document.getElementById('no-selection').style.display = 'flex';
        document.getElementById('node-properties').style.display = 'none';
        document.getElementById('connection-properties').style.display = 'none';
        document.getElementById('panel-title').textContent = 'Properties';
    }
    
    // Canvas interaction methods
    onCanvasMouseDown(e) {
        if (e.target === e.currentTarget || e.target.classList.contains('canvas-grid')) {
            this.deselectAll();
            this.isPanning = true;
            this.lastMousePos = { x: e.clientX, y: e.clientY };
            e.currentTarget.style.cursor = 'grabbing';
        }
    }
    
    onCanvasMouseMove(e) {
        if (this.isPanning) {
            const deltaX = e.clientX - this.lastMousePos.x;
            const deltaY = e.clientY - this.lastMousePos.y;
            
            this.canvasOffset.x += deltaX;
            this.canvasOffset.y += deltaY;
            
            this.updateCanvasTransform();
            this.lastMousePos = { x: e.clientX, y: e.clientY };
        }
        
        if (this.isDragging && this.selectedNode) {
            const deltaX = (e.clientX - this.lastMousePos.x) / this.zoomLevel;
            const deltaY = (e.clientY - this.lastMousePos.y) / this.zoomLevel;
            
            const node = this.nodes.get(this.selectedNode);
            if (node) {
                node.position.x += deltaX;
                node.position.y += deltaY;
                
                // Snap to grid
                node.position.x = Math.round(node.position.x / this.gridSize) * this.gridSize;
                node.position.y = Math.round(node.position.y / this.gridSize) * this.gridSize;
                
                this.renderNode(node);
                this.renderConnections();
            }
            
            this.lastMousePos = { x: e.clientX, y: e.clientY };
        }
        
        if (this.isConnecting) {
            this.updateTempConnection(e);
        }
    }
    
    onCanvasMouseUp(e) {
        if (this.isPanning) {
            this.isPanning = false;
            e.currentTarget.style.cursor = 'grab';
        }
        
        if (this.isDragging) {
            this.isDragging = false;
            this.markDirty();
        }
        
        if (this.isConnecting) {
            this.finishConnection(e);
        }
    }
    
    onCanvasWheel(e) {
        e.preventDefault();
        
        const rect = document.getElementById('workflow-canvas').getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;
        
        const scaleFactor = e.deltaY > 0 ? 0.9 : 1.1;
        const newZoom = Math.max(0.1, Math.min(3, this.zoomLevel * scaleFactor));
        
        // Zoom towards mouse position
        const scaleChange = newZoom / this.zoomLevel;
        this.canvasOffset.x = mouseX - (mouseX - this.canvasOffset.x) * scaleChange;
        this.canvasOffset.y = mouseY - (mouseY - this.canvasOffset.y) * scaleChange;
        this.zoomLevel = newZoom;
        
        this.updateCanvasTransform();
        this.updateGrid();
        this.updateZoomDisplay();
    }
    
    onCanvasContextMenu(e) {
        e.preventDefault();
        this.showContextMenu(e.clientX, e.clientY, 'canvas');
    }
    
    updateCanvasTransform() {
        const transform = `translate(${this.canvasOffset.x}px, ${this.canvasOffset.y}px) scale(${this.zoomLevel})`;
        this.nodesLayer.style.transform = transform;
        this.connectionsLayer.style.transform = transform;
    }
    
    updateGrid() {
        const gridSize = this.gridSize * this.zoomLevel;
        this.gridLayer.style.backgroundImage = `radial-gradient(circle, #ddd 1px, transparent 1px)`;
        this.gridLayer.style.backgroundSize = `${gridSize}px ${gridSize}px`;
        this.gridLayer.style.backgroundPosition = `${this.canvasOffset.x % gridSize}px ${this.canvasOffset.y % gridSize}px`;
    }
    
    renderConnections() {
        this.connections.forEach(connection => {
            this.renderConnection(connection);
        });
    }
    
    // Zoom methods
    zoomIn() {
        this.zoomLevel = Math.min(this.zoomLevel * 1.2, 3);
        this.updateCanvasTransform();
        this.updateGrid();
        this.updateZoomDisplay();
    }
    
    zoomOut() {
        this.zoomLevel = Math.max(this.zoomLevel / 1.2, 0.1);
        this.updateCanvasTransform();
        this.updateGrid();
        this.updateZoomDisplay();
    }
    
    updateZoomDisplay() {
        const zoomDisplay = document.getElementById('zoom-level');
        if (zoomDisplay) {
            zoomDisplay.textContent = `${Math.round(this.zoomLevel * 100)}%`;
        }
    }
    
    fitToScreen() {
        if (this.nodes.size === 0) return;
        
        let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
        
        this.nodes.forEach(node => {
            minX = Math.min(minX, node.position.x);
            minY = Math.min(minY, node.position.y);
            maxX = Math.max(maxX, node.position.x + 200);
            maxY = Math.max(maxY, node.position.y + 100);
        });
        
        const workflowWidth = maxX - minX;
        const workflowHeight = maxY - minY;
        
        const canvas = document.getElementById('workflow-canvas');
        const rect = canvas.getBoundingClientRect();
        const scaleX = (rect.width - 100) / workflowWidth;
        const scaleY = (rect.height - 100) / workflowHeight;
        
        this.zoomLevel = Math.min(scaleX, scaleY, 1);
        
        const centerX = (minX + maxX) / 2;
        const centerY = (minY + maxY) / 2;
        
        this.canvasOffset.x = rect.width / 2 - centerX * this.zoomLevel;
        this.canvasOffset.y = rect.height / 2 - centerY * this.zoomLevel;
        
        this.updateCanvasTransform();
        this.updateGrid();
        this.updateZoomDisplay();
    }
    
    centerCanvas() {
        if (this.nodes.size === 0) return;
        
        let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
        
        this.nodes.forEach(node => {
            minX = Math.min(minX, node.position.x);
            minY = Math.min(minY, node.position.y);
            maxX = Math.max(maxX, node.position.x + 200);
            maxY = Math.max(maxY, node.position.y + 100);
        });
        
        const centerX = (minX + maxX) / 2;
        const centerY = (minY + maxY) / 2;
        
        const canvas = document.getElementById('workflow-canvas');
        const rect = canvas.getBoundingClientRect();
        this.canvasOffset.x = rect.width / 2 - centerX * this.zoomLevel;
        this.canvasOffset.y = rect.height / 2 - centerY * this.zoomLevel;
        
        this.updateCanvasTransform();
    }
    
    clearCanvas() {
        if (confirm('Are you sure you want to clear the entire canvas? This action cannot be undone.')) {
            this.nodes.clear();
            this.connections.clear();
            this.nodesLayer.innerHTML = '';
            this.connectionsLayer.innerHTML = `
                <defs>
                    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                        <polygon points="0 0, 10 3.5, 0 7" fill="#3b82f6" />
                    </marker>
                </defs>
            `;
            this.deselectAll();
            this.markDirty();
        }
    }
    
    deleteNode(nodeId) {
        // Remove connections
        const connectionsToRemove = [];
        this.connections.forEach((connection, id) => {
            if (connection.source === nodeId || connection.target === nodeId) {
                connectionsToRemove.push(id);
            }
        });
        
        connectionsToRemove.forEach(id => this.deleteConnection(id));
        
        // Remove node
        this.nodes.delete(nodeId);
        const nodeElement = this.nodesLayer.querySelector(`[data-node-id="${nodeId}"]`);
        if (nodeElement) {
            nodeElement.remove();
        }
        
        this.deselectAll();
        this.markDirty();
    }
    
    deleteConnection(connectionId) {
        this.connections.delete(connectionId);
        const connectionElement = this.connectionsLayer.querySelector(`[data-connection-id="${connectionId}"]`);
        if (connectionElement) {
            connectionElement.remove();
        }
        
        if (this.selectedConnection === connectionId) {
            this.deselectAll();
        }
        
        this.markDirty();
    }
    
    // Context menu
    showContextMenu(x, y, type, targetId = null) {
        const contextMenu = document.getElementById('context-menu');
        if (!contextMenu) return;
        
        let menuItems = '';
        
        if (type === 'node') {
            menuItems = `
                <div class="context-item" onclick="workflowEditor.copyNode('${targetId}')">
                    <i class="fas fa-copy"></i> Copy
                </div>
                <div class="context-item" onclick="workflowEditor.duplicateNode('${targetId}')">
                    <i class="fas fa-clone"></i> Duplicate
                </div>
                <div class="context-divider"></div>
                <div class="context-item" onclick="workflowEditor.deleteNode('${targetId}')">
                    <i class="fas fa-trash"></i> Delete
                </div>
            `;
        } else if (type === 'connection') {
            menuItems = `
                <div class="context-item" onclick="workflowEditor.deleteConnection('${targetId}')">
                    <i class="fas fa-trash"></i> Delete Connection
                </div>
            `;
        } else {
            menuItems = `
                <div class="context-item" onclick="workflowEditor.pasteNode()">
                    <i class="fas fa-paste"></i> Paste
                </div>
                <div class="context-item" onclick="workflowEditor.centerCanvas()">
                    <i class="fas fa-crosshairs"></i> Center View
                </div>
                <div class="context-item" onclick="workflowEditor.fitToScreen()">
                    <i class="fas fa-expand-arrows-alt"></i> Fit to Screen
                </div>
            `;
        }
        
        contextMenu.innerHTML = menuItems;
        contextMenu.style.left = `${x}px`;
        contextMenu.style.top = `${y}px`;
        contextMenu.style.display = 'block';
    }
    
    hideContextMenu() {
        const contextMenu = document.getElementById('context-menu');
        if (contextMenu) {
            contextMenu.style.display = 'none';
        }
    }
    
    // Clipboard operations
    copyNode(nodeId) {
        const node = this.nodes.get(nodeId);
        if (node) {
            this.clipboard = JSON.parse(JSON.stringify(node));
            this.showNotification('Node copied to clipboard', 'success');
        }
    }
    
    duplicateNode(nodeId) {
        const node = this.nodes.get(nodeId);
        if (!node) return;
        
        const newNode = JSON.parse(JSON.stringify(node));
        newNode.id = `node_${++this.nodeCounter}`;
        newNode.position.x += 50;
        newNode.position.y += 50;
        newNode.name += ' (Copy)';
        
        this.nodes.set(newNode.id, newNode);
        this.renderNode(newNode);
        this.selectNode(newNode.id);
        this.markDirty();
    }
    
    pasteNode() {
        if (!this.clipboard) {
            this.showNotification('Nothing to paste', 'warning');
            return;
        }
        
        const newNode = JSON.parse(JSON.stringify(this.clipboard));
        newNode.id = `node_${++this.nodeCounter}`;
        newNode.position.x += 50;
        newNode.position.y += 50;
        newNode.name += ' (Pasted)';
        
        this.nodes.set(newNode.id, newNode);
        this.renderNode(newNode);
        this.selectNode(newNode.id);
        this.markDirty();
    }
    
    // Workflow operations
    async saveWorkflow() {
        const workflowName = document.getElementById('workflow-name')?.value || 'Untitled Workflow';
        const workflowData = {
            name: workflowName,
            definition: this.getWorkflowData()
        };
        
        try {
            this.showLoading('Saving workflow...');
            
            const url = this.workflowId ? `${this.apiBaseUrl}${this.workflowId}/` : this.apiBaseUrl;
            const method = this.workflowId ? 'PUT' : 'POST';
            
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrfToken
                },
                body: JSON.stringify(workflowData)
            });
            
            if (response.ok) {
                const result = await response.json();
                if (!this.workflowId) {
                    this.workflowId = result.id;
                    window.history.replaceState({}, '', `/workflow/${result.id}/edit/`);
                }
                this.markClean();
                this.showNotification('Workflow saved successfully', 'success');
                this.updateWorkflowStatus(result.status);
            } else {
                throw new Error('Failed to save workflow');
            }
        } catch (error) {
            console.error('Save error:', error);
            this.showNotification('Failed to save workflow', 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    async testWorkflow() {
        if (!this.workflowId) {
            this.showNotification('Please save the workflow first', 'warning');
            return;
        }
        
        try {
            this.showLoading('Testing workflow...');
            
            const response = await fetch(`${this.apiBaseUrl}${this.workflowId}/execute/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrfToken
                },
                body: JSON.stringify({ sync: false, test_mode: true })
            });
            
            if (response.ok) {
                const result = await response.json();
                this.showNotification('Workflow test started', 'success');
                this.switchTab('logs');
                this.pollExecutionStatus(result.execution_id);
            } else {
                throw new Error('Failed to start workflow test');
            }
        } catch (error) {
            console.error('Test error:', error);
            this.showNotification('Failed to test workflow', 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    async deployWorkflow() {
        if (!this.workflowId) {
            this.showNotification('Please save the workflow first', 'warning');
            return;
        }
        
        try {
            this.showLoading('Deploying workflow...');
            
            const response = await fetch(`${this.apiBaseUrl}${this.workflowId}/activate/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.csrfToken
                }
            });
            
            if (response.ok) {
                this.showNotification('Workflow deployed successfully', 'success');
                this.updateWorkflowStatus('active');
            } else {
                throw new Error('Failed to deploy workflow');
            }
        } catch (error) {
            console.error('Deploy error:', error);
            this.showNotification('Failed to deploy workflow', 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    getWorkflowData() {
        const nodes = [];
        const connections = [];
        
        this.nodes.forEach(node => {
            nodes.push({
                id: node.id,
                type: node.type,
                name: node.name,
                position: node.position,
                config: node.config || {},
                description: node.description || '',
                continue_on_error: node.continue_on_error || false,
                timeout: node.timeout || 30
            });
        });
        
        this.connections.forEach(connection => {
            connections.push({
                id: connection.id,
                source: connection.source,
                sourceHandle: connection.sourceHandle,
                target: connection.target,
                targetHandle: connection.targetHandle
            });
        });
        
        return { nodes, connections };
    }
    
    loadWorkflow() {
        if (this.workflowData && this.workflowData.nodes) {
            this.workflowData.nodes.forEach(nodeData => {
                const node = {
                    id: nodeData.id,
                    type: nodeData.type,
                    name: nodeData.name,
                    position: nodeData.position,
                    config: nodeData.config || {},
                    description: nodeData.description || '',
                    continue_on_error: nodeData.continue_on_error || false,
                    timeout: nodeData.timeout || 30,
                    inputs: this.getNodeInputs(this.nodeTypes.get(nodeData.type)),
                    outputs: this.getNodeOutputs(this.nodeTypes.get(nodeData.type))
                };
                
                this.nodes.set(node.id, node);
                this.renderNode(node);
                
                if (parseInt(node.id.split('_')[1]) > this.nodeCounter) {
                    this.nodeCounter = parseInt(node.id.split('_')[1]);
                }
            });
            
            // Render connections after nodes
            setTimeout(() => {
                if (this.workflowData.connections) {
                    this.workflowData.connections.forEach(connectionData => {
                        const connection = {
                            id: connectionData.id,
                            source: connectionData.source,
                            sourceHandle: connectionData.sourceHandle || 'output',
                            target: connectionData.target,
                            targetHandle: connectionData.targetHandle || 'input'
                        };
                        
                        this.connections.set(connection.id, connection);
                        this.renderConnection(connection);
                    });
                }
            }, 100);
        }
    }
    
    // Import/Export
    exportWorkflow() {
        const workflowData = {
            name: document.getElementById('workflow-name')?.value || 'Untitled Workflow',
            definition: this.getWorkflowData(),
            exported_at: new Date().toISOString(),
            version: '1.0'
        };
        
        const dataStr = JSON.stringify(workflowData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(dataBlob);
        link.download = `${workflowData.name.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.json`;
        link.click();
        
        this.showNotification('Workflow exported', 'success');
    }
    
    importWorkflow() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.json';
        
        input.onchange = (e) => {
            const file = e.target.files[0];
            if (!file) return;
            
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const workflowData = JSON.parse(e.target.result);
                    
                    if (confirm('This will replace the current workflow. Continue?')) {
                        this.clearCanvas();
                        this.workflowData = workflowData.definition || workflowData;
                        this.loadWorkflow();
                        
                        // Update workflow name
                        const nameInput = document.getElementById('workflow-name');
                        if (nameInput && workflowData.name) {
                            nameInput.value = workflowData.name;
                        }
                        
                        this.markDirty();
                        this.showNotification('Workflow imported', 'success');
                    }
                } catch (error) {
                    console.error('Import error:', error);
                    this.showNotification('Failed to import workflow', 'error');
                }
            };
            
            reader.readAsText(file);
        };
        
        input.click();
    }
    
    duplicateWorkflow() {
        if (!this.workflowId) {
            this.showNotification('Please save the workflow first', 'warning');
            return;
        }
        
        this.workflowId = null;
        
        const nameInput = document.getElementById('workflow-name');
        if (nameInput) {
            nameInput.value = `${nameInput.value} (Copy)`;
        }
        
        window.history.replaceState({}, '', '/workflow/create/');
        this.markDirty();
        this.showNotification('Workflow duplicated. Save to create a new workflow.', 'info');
    }
    
    // Execution monitoring
    async pollExecutionStatus(executionId) {
        const maxPolls = 60;
        let pollCount = 0;
        
        const poll = async () => {
            try {
                const response = await fetch(`/workflow/api/executions/${executionId}/`);
                if (response.ok) {
                    const execution = await response.json();
                    
                    if (execution.status === 'running' || execution.status === 'queued') {
                        if (pollCount < maxPolls) {
                            pollCount++;
                            setTimeout(poll, 5000);
                        }
                    } else {
                        this.loadExecutionLogs(executionId);
                    }
                }
            } catch (error) {
                console.error('Polling error:', error);
            }
        };
        
        poll();
    }
    
    async loadExecutionLogs(executionId) {
        try {
            const response = await fetch(`/workflow/api/executions/${executionId}/logs/`);
            if (response.ok) {
                const data = await response.json();
                this.displayExecutionLogs(data.logs);
            }
        } catch (error) {
            console.error('Failed to load execution logs:', error);
        }
    }
    
    displayExecutionLogs(logs) {
        const logsContainer = document.getElementById('execution-logs');
        if (!logsContainer) return;
        
        if (!logs || logs.length === 0) {
            logsContainer.innerHTML = '<div class="log-placeholder">No logs available</div>';
            return;
        }
        
        let logsHtml = '';
        logs.forEach(log => {
            const timestamp = new Date(log.timestamp).toLocaleTimeString();
            const levelClass = `log-${log.level.toLowerCase()}`;
            
            logsHtml += `
                <div class="log-entry ${levelClass}">
                    <span class="log-timestamp">[${timestamp}]</span>
                    <span class="log-level">${log.level}</span>
                    <span class="log-node">${log.node_name}:</span>
                    <span class="log-message">${log.message}</span>
                    ${log.duration_ms ? `<span class="log-duration">(${log.duration_ms}ms)</span>` : ''}
                </div>
            `;
        });
        
        logsContainer.innerHTML = logsHtml;
        logsContainer.scrollTop = logsContainer.scrollHeight;
    }
    
    // Tab management
    switchTab(tabName) {
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabName);
        });
        
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.toggle('active', content.id === `${tabName}-tab`);
        });
    }
    
    // State management
    markDirty() {
        this.isDirty = true;
        this.updateSaveButton();
    }
    
    markClean() {
        this.isDirty = false;
        this.updateSaveButton();
    }
    
    updateSaveButton() {
        const saveBtn = document.getElementById('save-btn');
        if (saveBtn) {
            saveBtn.classList.toggle('btn-warning', this.isDirty);
            saveBtn.innerHTML = this.isDirty ? '<i class="fas fa-save"></i> Save*' : '<i class="fas fa-save"></i> Save';
        }
    }
    
    updateWorkflowName() {
        this.markDirty();
    }
    
    updateWorkflowStatus(status) {
        const statusElement = document.querySelector('.workflow-status');
        if (statusElement) {
            statusElement.className = `workflow-status status-${status}`;
            statusElement.textContent = status.charAt(0).toUpperCase() + status.slice(1);
        }
    }
    
    // Navigation
    goBack() {
        if (this.isDirty) {
            if (confirm('You have unsaved changes. Are you sure you want to leave?')) {
                this.navigateBack();
            }
        } else {
            this.navigateBack();
        }
    }
    
    navigateBack() {
        if (this.workflowId) {
            window.location.href = `/workflow/${this.workflowId}/`;
        } else {
            window.location.href = '/workflow/';
        }
    }
    
    // Keyboard shortcuts
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch (e.key) {
                    case 's':
                        e.preventDefault();
                        this.saveWorkflow();
                        break;
                    case 'c':
                        if (this.selectedNode) {
                            e.preventDefault();
                            this.copyNode(this.selectedNode);
                        }
                        break;
                    case 'v':
                        if (this.clipboard) {
                            e.preventDefault();
                            this.pasteNode();
                        }
                        break;
                    case 'a':
                        e.preventDefault();
                        this.selectAll();
                        break;
                    case 'Enter':
                        if (e.shiftKey) {
                            e.preventDefault();
                            this.testWorkflow();
                        }
                        break;
                }
            } else if (e.key === 'Delete' || e.key === 'Backspace') {
                if (this.selectedNode) {
                    this.deleteNode(this.selectedNode);
                } else if (this.selectedConnection) {
                    this.deleteConnection(this.selectedConnection);
                }
            } else if (e.key === 'Escape') {
                this.deselectAll();
            }
        });
        
        // Prevent page unload with unsaved changes
        window.addEventListener('beforeunload', (e) => {
            if (this.isDirty) {
                e.preventDefault();
                e.returnValue = 'You have unsaved changes. Are you sure you want to leave?';
                return e.returnValue;
            }
        });
    }
    
    selectAll() {
        // For now, just select all nodes
        this.nodes.forEach((node, nodeId) => {
            this.selectNode(nodeId);
        });
    }
    
    filterNodes(searchTerm) {
        const term = searchTerm.toLowerCase();
        document.querySelectorAll('.palette-node').forEach(node => {
            const text = node.textContent.toLowerCase();
            const nodeType = node.dataset.nodeType;
            const type = this.nodeTypes.get(nodeType);
            const description = type?.description?.toLowerCase() || '';
            
            const matches = text.includes(term) || description.includes(term);
            node.style.display = matches ? 'flex' : 'none';
        });
    }
    
    // UI helpers
    showLoading(message = 'Loading...') {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            const spinner = overlay.querySelector('.loading-spinner p');
            if (spinner) spinner.textContent = message;
            overlay.style.display = 'flex';
        }
    }
    
    hideLoading() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.style.display = 'none';
        }
    }
    
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas ${this.getNotificationIcon(type)}"></i>
            <span>${message}</span>
        `;
        
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 6px;
            color: white;
            font-weight: 500;
            z-index: 10000;
            display: flex;
            align-items: center;
            gap: 8px;
            animation: slideIn 0.3s ease;
            max-width: 400px;
        `;
        
        const colors = {
            success: '#10b981',
            error: '#ef4444',
            warning: '#f59e0b',
            info: '#3b82f6'
        };
        
        notification.style.backgroundColor = colors[type] || colors.info;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
    
    getNotificationIcon(type) {
        const icons = {
            success: 'fa-check-circle',
            error: 'fa-times-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle'
        };
        return icons[type] || icons.info;
    }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .workflow-node {
        position: absolute;
        min-width: 180px;
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        cursor: move;
        z-index: 10;
        transition: all 0.2s;
    }
    
    .workflow-node:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }
    
    .workflow-node.selected {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    .node-header {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 12px;
        border-bottom: 1px solid #e5e7eb;
        background: #f8fafc;
        border-radius: 6px 6px 0 0;
    }
    
    .node-icon {
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 6px;
        color: white;
        font-size: 14px;
    }
    
    .node-title {
        font-weight: 600;
        font-size: 14px;
        flex: 1;
        color: #1f2937;
    }
    
    .node-status {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #6b7280;
    }
    
    .node-body {
        padding: 12px;
        font-size: 12px;
        color: #6b7280;
        min-height: 40px;
    }
    
    .node-handle {
        position: absolute;
        width: 12px;
        height: 12px;
        border: 2px solid white;
        border-radius: 50%;
        background: #6b7280;
        cursor: crosshair;
        z-index: 20;
        transform: translate(-50%, -50%);
    }
    
    .node-handle:hover,
    .node-handle.active {
        background: #3b82f6;
        transform: translate(-50%, -50%) scale(1.2);
    }
    
    .node-handle.input {
        left: 0;
    }
    
    .node-handle.output {
        right: 0;
    }
    
    .palette-node {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px;
        margin: 2px 0;
        border-radius: 6px;
        cursor: grab;
        font-size: 14px;
        transition: all 0.2s;
    }
    
    .palette-node:hover {
        background: #f3f4f6;
        transform: translateX(4px);
    }
    
    .palette-node:active {
        cursor: grabbing;
    }
    
    .palette-node .node-icon {
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 4px;
        color: white;
        font-size: 12px;
    }
    
    .palette-node.dragging {
        opacity: 0.5;
    }
    
    .connection-path {
        stroke: #3b82f6;
        stroke-width: 2;
        fill: none;
        cursor: pointer;
    }
    
    .connection-path:hover {
        stroke: #f59e0b;
        stroke-width: 3;
    }
    
    .temp-connection {
        pointer-events: none;
    }
    
    .context-menu {
        position: fixed;
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        min-width: 120px;
        display: none;
    }
    
    .context-item {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        font-size: 14px;
        cursor: pointer;
        transition: background 0.2s;
    }
    
    .context-item:hover {
        background: #f3f4f6;
    }
    
    .context-divider {
        height: 1px;
        background: #e5e7eb;
        margin: 4px 0;
    }
    
    .form-section {
        margin-bottom: 24px;
        padding-bottom: 16px;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .form-section:last-child {
        border-bottom: none;
        margin-bottom: 0;
    }
    
    .form-section h4 {
        margin: 0 0 16px 0;
        font-size: 16px;
        font-weight: 600;
        color: #1f2937;
    }
    
    .form-group {
        margin-bottom: 16px;
    }
    
    .form-group label {
        display: block;
        font-weight: 500;
        font-size: 14px;
        margin-bottom: 4px;
        color: #374151;
    }
    
    .form-control {
        width: 100%;
        padding: 8px 12px;
        border: 1px solid #d1d5db;
        border-radius: 6px;
        font-size: 14px;
        transition: border-color 0.2s;
    }
    
    .form-control:focus {
        outline: none;
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    .form-help {
        display: block;
        margin-top: 4px;
        font-size: 12px;
        color: #6b7280;
    }
    
    .checkbox-label {
        display: flex !important;
        align-items: center;
        cursor: pointer;
        font-weight: normal !important;
    }
    
    .checkbox-label input[type="checkbox"] {
        width: auto !important;
        margin-right: 8px;
    }
    
    .log-entry {
        font-family: 'Monaco', 'Menlo', monospace;
        font-size: 12px;
        padding: 4px 8px;
        margin: 2px 0;
        border-radius: 3px;
        background: #f8f9fa;
    }
    
    .log-entry.log-error {
        background: #fee2e2;
        color: #dc2626;
    }
    
    .log-entry.log-warning {
        background: #fef3c7;
        color: #d97706;
    }
    
    .log-entry.log-info {
        background: #dbeafe;
        color: #2563eb;
    }
    
    .log-timestamp {
        color: #6b7280;
        margin-right: 8px;
    }
    
    .log-level {
        font-weight: bold;
        margin-right: 8px;
    }
    
    .log-node {
        font-weight: 600;
        margin-right: 8px;
    }
    
    .log-duration {
        color: #6b7280;
        margin-left: 8px;
        font-style: italic;
    }
    
    .log-placeholder {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        color: #6b7280;
        font-style: italic;
    }
`;
document.head.appendChild(style);

// Export for global use
window.WorkflowEditor = WorkflowEditor;