/**
 * Main Workflow Editor - Integrates all components
 */
class WorkflowEditorMain {
  constructor(options = {}) {
    this.options = {
      workflowId: null,
      workflowData: { nodes: [], connections: [] },
      csrfToken: null,
      apiBaseUrl: "/workflow/api/workflows/",
      autoSave: true,
      ...options,
    }

    // Components
    this.canvas = null
    this.palette = null
    this.properties = null

    // State
    this.isDirty = false
    this.isLoading = false
    this.currentWorkflow = null

    this.init()
  }

  init() {
    this.setupComponents()
    this.setupEventListeners()
    this.loadWorkflow()
  }

  setupComponents() {
    // Initialize canvas
    this.canvas = new WorkflowCanvas("workflow-canvas", {
      gridSize: 20,
      snapToGrid: true,
    })

    // Initialize node palette
    this.palette = new NodePalette("node-palette", {
      searchable: true,
      collapsible: true,
    })

    // Initialize properties panel
    this.properties = new PropertiesPanel("properties-panel", {
      autoSave: true,
    })

    // Setup component interactions
    this.setupComponentInteractions()
  }

  setupComponentInteractions() {
    // Canvas events
    this.canvas.on("nodeDropped", (e) => {
      const { nodeType, position } = e.detail
      this.addNodeFromPalette(nodeType, position)
    })

    this.canvas.on("nodeSelected", (e) => {
      const { nodeId } = e.detail
      const node = this.canvas.nodes.get(nodeId)
      if (node) {
        this.properties.showNodeProperties(node)
      }
    })

    this.canvas.on("connectionSelected", (e) => {
      const { connectionId } = e.detail
      const connection = this.canvas.connections.get(connectionId)
      if (connection) {
        this.properties.showConnectionProperties(connection)
      }
    })

    this.canvas.on("selectionCleared", () => {
      this.properties.hide()
    })

    this.canvas.on("nodesMoved", () => {
      this.markDirty()
    })

    this.canvas.on("connectionAdded", () => {
      this.markDirty()
    })

    this.canvas.on("connectionRemoved", () => {
      this.markDirty()
    })

    this.canvas.on("nodeRemoved", () => {
      this.markDirty()
      this.properties.hide()
    })

    // Properties panel events
    this.properties.on("nodePropertyChanged", (e) => {
      const { node } = e.detail
      this.canvas.updateNode(node.id, node)
      this.markDirty()
    })

    this.properties.on("connectionPropertyChanged", () => {
      this.markDirty()
    })
  }

  setupEventListeners() {
    // Toolbar buttons
    document.getElementById("save-btn")?.addEventListener("click", () => this.saveWorkflow())
    document.getElementById("test-btn")?.addEventListener("click", () => this.testWorkflow())
    document.getElementById("deploy-btn")?.addEventListener("click", () => this.deployWorkflow())

    // Zoom controls
    document.getElementById("zoom-in")?.addEventListener("click", () => this.zoomIn())
    document.getElementById("zoom-out")?.addEventListener("click", () => this.zoomOut())
    document.getElementById("zoom-fit")?.addEventListener("click", () => this.fitToScreen())

    // Canvas controls
    document.getElementById("center-canvas")?.addEventListener("click", () => this.centerCanvas())
    document.getElementById("clear-canvas")?.addEventListener("click", () => this.clearCanvas())

    // Menu actions
    document.getElementById("export-btn")?.addEventListener("click", () => this.exportWorkflow())
    document.getElementById("import-btn")?.addEventListener("click", () => this.importWorkflow())
    document.getElementById("duplicate-btn")?.addEventListener("click", () => this.duplicateWorkflow())

    // Workflow name editing
    const nameInput = document.getElementById("workflow-name")
    if (nameInput) {
      nameInput.addEventListener("blur", () => this.updateWorkflowName())
      nameInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
          nameInput.blur()
        }
      })
    }

    // Back button
    document.getElementById("back-btn")?.addEventListener("click", () => {
      if (this.isDirty) {
        if (confirm("You have unsaved changes. Are you sure you want to leave?")) {
          this.goBack()
        }
      } else {
        this.goBack()
      }
    })

    // Auto-save
    if (this.options.autoSave) {
      setInterval(() => {
        if (this.isDirty && !this.isLoading) {
          this.saveWorkflow(true) // Silent save
        }
      }, 30000) // Auto-save every 30 seconds
    }

    // Keyboard shortcuts
    document.addEventListener("keydown", (e) => {
      if (e.ctrlKey || e.metaKey) {
        switch (e.key) {
          case "s":
            e.preventDefault()
            this.saveWorkflow()
            break
          case "Enter":
            if (e.shiftKey) {
              e.preventDefault()
              this.testWorkflow()
            }
            break
        }
      }
    })

    // Prevent page unload with unsaved changes
    window.addEventListener("beforeunload", (e) => {
      if (this.isDirty) {
        e.preventDefault()
        e.returnValue = "You have unsaved changes. Are you sure you want to leave?"
        return e.returnValue
      }
    })
  }

  addNodeFromPalette(nodeTypeName, position) {
    const nodeType = this.palette.getNodeType(nodeTypeName)
    if (!nodeType) {
      console.error("Unknown node type:", nodeTypeName)
      return
    }

    const nodeData = {
      type: nodeType.name,
      name: nodeType.display_name,
      config: this.getDefaultConfig(nodeType),
      inputs: this.getNodeInputs(nodeType),
      outputs: this.getNodeOutputs(nodeType),
    }

    const nodeId = this.canvas.addNode(nodeData, position)
    this.canvas.selectNode(nodeId)
    this.markDirty()

    return nodeId
  }

  getDefaultConfig(nodeType) {
    const config = {}
    if (nodeType.config_schema && nodeType.config_schema.fields) {
      nodeType.config_schema.fields.forEach((field) => {
        if (field.default !== undefined) {
          config[field.name] = field.default
        }
      })
    }
    return config
  }

  getNodeInputs(nodeType) {
    // Most nodes have a single input, except triggers
    if (nodeType.category === "trigger") {
      return []
    }
    return ["input"]
  }

  getNodeOutputs(nodeType) {
    // Condition nodes have multiple outputs
    if (nodeType.name === "condition") {
      return ["true", "false"]
    } else if (nodeType.name === "switch") {
      return ["output"] // Dynamic outputs based on cases
    }
    return ["output"]
  }

  async saveWorkflow(silent = false) {
    if (this.isLoading) return

    try {
      this.isLoading = true
      if (!silent) this.showLoading("Saving workflow...")

      const workflowData = this.getWorkflowData()
      const url = this.options.workflowId
        ? `${this.options.apiBaseUrl}${this.options.workflowId}/`
        : this.options.apiBaseUrl

      const method = this.options.workflowId ? "PUT" : "POST"

      const response = await fetch(url, {
        method: method,
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": this.options.csrfToken,
        },
        body: JSON.stringify(workflowData),
      })

      if (response.ok) {
        const result = await response.json()

        if (!this.options.workflowId) {
          this.options.workflowId = result.id
          // Update URL without page reload
          window.history.replaceState({}, "", `/workflow/${result.id}/edit/`)
        }

        this.currentWorkflow = result
        this.markClean()

        if (!silent) {
          this.showNotification("Workflow saved successfully", "success")
        }

        this.updateWorkflowStatus(result.status)
      } else {
        throw new Error("Failed to save workflow")
      }
    } catch (error) {
      console.error("Save error:", error)
      if (!silent) {
        this.showNotification("Failed to save workflow", "error")
      }
    } finally {
      this.isLoading = false
      if (!silent) this.hideLoading()
    }
  }

  async testWorkflow() {
    if (!this.options.workflowId) {
      this.showNotification("Please save the workflow first", "warning")
      return
    }

    try {
      this.showLoading("Testing workflow...")

      const response = await fetch(`${this.options.apiBaseUrl}${this.options.workflowId}/execute/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": this.options.csrfToken,
        },
        body: JSON.stringify({ sync: false, test_mode: true }),
      })

      if (response.ok) {
        const result = await response.json()
        this.showNotification("Workflow test started", "success")

        // Show logs tab
        this.switchTab("logs")

        // Poll for execution results
        this.pollExecutionStatus(result.execution_id)
      } else {
        throw new Error("Failed to start workflow test")
      }
    } catch (error) {
      console.error("Test error:", error)
      this.showNotification("Failed to test workflow", "error")
    } finally {
      this.hideLoading()
    }
  }

  async deployWorkflow() {
    if (!this.options.workflowId) {
      this.showNotification("Please save the workflow first", "warning")
      return
    }

    try {
      this.showLoading("Deploying workflow...")

      const response = await fetch(`${this.options.apiBaseUrl}${this.options.workflowId}/activate/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": this.options.csrfToken,
        },
      })

      if (response.ok) {
        this.showNotification("Workflow deployed successfully", "success")
        this.updateWorkflowStatus("active")
      } else {
        throw new Error("Failed to deploy workflow")
      }
    } catch (error) {
      console.error("Deploy error:", error)
      this.showNotification("Failed to deploy workflow", "error")
    } finally {
      this.hideLoading()
    }
  }

  async pollExecutionStatus(executionId) {
    const maxPolls = 60 // 5 minutes max
    let pollCount = 0

    const poll = async () => {
      try {
        const response = await fetch(`/workflow/api/executions/${executionId}/`)
        if (response.ok) {
          const execution = await response.json()

          if (execution.status === "running" || execution.status === "queued") {
            if (pollCount < maxPolls) {
              pollCount++
              setTimeout(poll, 5000) // Poll every 5 seconds
            }
          } else {
            // Execution finished, load logs
            this.loadExecutionLogs(executionId)
          }
        }
      } catch (error) {
        console.error("Polling error:", error)
      }
    }

    poll()
  }

  async loadExecutionLogs(executionId) {
    try {
      const response = await fetch(`/workflow/api/executions/${executionId}/logs/`)
      if (response.ok) {
        const data = await response.json()
        this.displayExecutionLogs(data.logs)
      }
    } catch (error) {
      console.error("Failed to load execution logs:", error)
    }
  }

  displayExecutionLogs(logs) {
    const logsContainer = document.getElementById("execution-logs")
    if (!logsContainer) return

    if (!logs || logs.length === 0) {
      logsContainer.innerHTML = '<div class="log-placeholder">No logs available</div>'
      return
    }

    let logsHtml = ""
    logs.forEach((log) => {
      const timestamp = new Date(log.timestamp).toLocaleTimeString()
      const levelClass = `log-${log.level.toLowerCase()}`

      logsHtml += `
                <div class="log-entry ${levelClass}">
                    <span class="log-timestamp">[${timestamp}]</span>
                    <span class="log-level">${log.level}</span>
                    <span class="log-node">${log.node_name}:</span>
                    <span class="log-message">${log.message}</span>
                    ${log.duration_ms ? `<span class="log-duration">(${log.duration_ms}ms)</span>` : ""}
                </div>
            `
    })

    logsContainer.innerHTML = logsHtml
    logsContainer.scrollTop = logsContainer.scrollHeight
  }

  getWorkflowData() {
    const canvasData = this.canvas.getWorkflowData()
    const nameInput = document.getElementById("workflow-name")

    return {
      name: nameInput ? nameInput.value : "Untitled Workflow",
      definition: canvasData,
      // Add other workflow properties as needed
    }
  }

  loadWorkflow() {
    if (this.options.workflowData && this.options.workflowData.nodes) {
      this.canvas.loadWorkflowData(this.options.workflowData)
    }
  }

  updateWorkflowName() {
    const nameInput = document.getElementById("workflow-name")
    if (nameInput && nameInput.value.trim()) {
      this.markDirty()
    }
  }

  updateWorkflowStatus(status) {
    const statusElement = document.querySelector(".workflow-status")
    if (statusElement) {
      statusElement.className = `workflow-status status-${status}`
      statusElement.textContent = status.charAt(0).toUpperCase() + status.slice(1)
    }
  }

  // Canvas controls
  zoomIn() {
    // Implement zoom in
    this.canvas.transform.scale = Math.min(this.canvas.transform.scale * 1.2, 3)
    this.canvas.updateTransform()
    this.updateZoomDisplay()
  }

  zoomOut() {
    // Implement zoom out
    this.canvas.transform.scale = Math.max(this.canvas.transform.scale / 1.2, 0.1)
    this.canvas.updateTransform()
    this.updateZoomDisplay()
  }

  fitToScreen() {
    this.canvas.fitToView()
    this.updateZoomDisplay()
  }

  centerCanvas() {
    this.canvas.centerView()
  }

  clearCanvas() {
    if (confirm("Are you sure you want to clear the entire canvas? This action cannot be undone.")) {
      this.canvas.clear()
      this.properties.hide()
      this.markDirty()
    }
  }

  updateZoomDisplay() {
    const zoomDisplay = document.getElementById("zoom-level")
    if (zoomDisplay) {
      zoomDisplay.textContent = `${Math.round(this.canvas.transform.scale * 100)}%`
    }
  }

  // Import/Export
  exportWorkflow() {
    const workflowData = this.getWorkflowData()
    const dataStr = JSON.stringify(workflowData, null, 2)
    const dataBlob = new Blob([dataStr], { type: "application/json" })

    const link = document.createElement("a")
    link.href = URL.createObjectURL(dataBlob)
    link.download = `${workflowData.name || "workflow"}.json`
    link.click()

    this.showNotification("Workflow exported", "success")
  }

  importWorkflow() {
    const input = document.createElement("input")
    input.type = "file"
    input.accept = ".json"

    input.onchange = (e) => {
      const file = e.target.files[0]
      if (!file) return

      const reader = new FileReader()
      reader.onload = (e) => {
        try {
          const workflowData = JSON.parse(e.target.result)

          if (confirm("This will replace the current workflow. Continue?")) {
            this.canvas.loadWorkflowData(workflowData.definition || workflowData)

            // Update workflow name
            const nameInput = document.getElementById("workflow-name")
            if (nameInput && workflowData.name) {
              nameInput.value = workflowData.name
            }

            this.markDirty()
            this.showNotification("Workflow imported", "success")
          }
        } catch (error) {
          console.error("Import error:", error)
          this.showNotification("Failed to import workflow", "error")
        }
      }

      reader.readAsText(file)
    }

    input.click()
  }

  duplicateWorkflow() {
    if (!this.options.workflowId) {
      this.showNotification("Please save the workflow first", "warning")
      return
    }

    // Reset workflow ID to create a new workflow
    this.options.workflowId = null

    // Update name
    const nameInput = document.getElementById("workflow-name")
    if (nameInput) {
      nameInput.value = `${nameInput.value} (Copy)`
    }

    // Update URL
    window.history.replaceState({}, "", "/workflow/create/")

    this.markDirty()
    this.showNotification("Workflow duplicated. Save to create a new workflow.", "info")
  }

  // Tab management
  switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll(".tab-btn").forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.tab === tabName)
    })

    // Update tab content
    document.querySelectorAll(".tab-content").forEach((content) => {
      content.classList.toggle("active", content.id === `${tabName}-tab`)
    })
  }

  // State management
  markDirty() {
    this.isDirty = true
    this.updateSaveButton()
  }

  markClean() {
    this.isDirty = false
    this.updateSaveButton()
  }

  updateSaveButton() {
    const saveBtn = document.getElementById("save-btn")
    if (saveBtn) {
      saveBtn.classList.toggle("btn-warning", this.isDirty)
      saveBtn.innerHTML = this.isDirty
        ? '<i class="fas fa-save"></i> Save*'
        : '<i class="fas fa-save"></i> Save'
    }
  }

  // Navigation
  goBack() {
    if (this.options.workflowId) {
      window.location.href = `/workflow/${this.options.workflowId}/`
    } else {
      window.location.href = "/workflow/"
    }
  }

  // UI helpers
  showLoading(message = "Loading...") {
    const overlay = document.getElementById("loading-overlay")
    if (overlay) {
      const spinner = overlay.querySelector(".loading-spinner p")
      if (spinner) spinner.textContent = message
      overlay.style.display = "flex"
    }
  }

  hideLoading() {
    const overlay = document.getElementById("loading-overlay")
    if (overlay) {
      overlay.style.display = "none"
    }
  }

  showNotification(message, type = "info") {
    // Create notification element
    const notification = document.createElement("div")
    notification.className = `notification notification-${type}`
    notification.innerHTML = `
            <i class="fas ${this.getNotificationIcon(type)}"></i>
            <span>${message}</span>
        `

    // Style notification
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
        `

    const colors = {
      success: "#10b981",
      error: "#ef4444",
      warning: "#f59e0b",
      info: "#3b82f6",
    }

    notification.style.backgroundColor = colors[type] || colors.info
    document.body.appendChild(notification)

    // Auto remove
    setTimeout(() => {
      notification.style.animation = "slideOut 0.3s ease"
      setTimeout(() => notification.remove(), 300)
    }, 3000)
  }

  getNotificationIcon(type) {
    const icons = {
      success: "fa-check-circle",
      error: "fa-times-circle",
      warning: "fa-exclamation-triangle",
      info: "fa-info-circle",
    }
    return icons[type] || icons.info
  }
}

// Add CSS animations
const style = document.createElement("style")
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
    
    .json-editor.error {
        border-color: #ef4444;
        background-color: #fef2f2;
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
`
document.head.appendChild(style)

// Export for global use
window.WorkflowEditorMain = WorkflowEditorMain