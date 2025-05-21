/**
 * TasksCentral - Main JavaScript
 * 
 * This is the primary JavaScript file that handles general UI interactions
 * across the entire application. It initializes components and sets up event
 * listeners when the DOM is fully loaded.
 */

/**
 * DOMContentLoaded event listener
 * 
 * This ensures our JavaScript only runs after the HTML document has been fully loaded
 * and parsed, but doesn't wait for stylesheets, images, and subframes to finish loading.
 * This is a best practice to avoid JavaScript errors from trying to access elements
 * that don't exist yet.
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips - These are the small popups that appear when hovering over elements
    initTooltips();
    
    // Initialize all task status badges - Apply appropriate colors based on status
    // This makes it easy to visually identify task statuses (red for overdue, green for complete, etc.)
    updateStatusBadgeColors();
    
    // Add event listener to task status dropdowns - For changing task status via UI
    // This allows users to update task status without refreshing the page (AJAX)
    setupStatusDropdowns();
    
    // Initialize all tab navigation if present - For tabbed interfaces
    // Many pages use tabs to organize content (details, comments, attachments, etc.)
    initTabNavigation();
});

/**
 * Initialize Bootstrap tooltips
 * 
 * This function finds all elements with the data-bs-toggle="tooltip" attribute
 * and initializes them as Bootstrap tooltip components. Tooltips provide helpful
 * text when hovering over buttons or icons.
 * 
 * Bootstrap 5 requires manual initialization of tooltips for performance reasons.
 */
function initTooltips() {
    // Find all tooltip elements in the document
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    
    // Initialize each tooltip using Bootstrap's Tooltip constructor
    // The map function transforms each element into an initialized tooltip
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Update colors for status badges
 */
function updateStatusBadgeColors() {
    // Update colors for status badges
    document.querySelectorAll('.status-badge').forEach(badge => {
        const status = badge.textContent.toLowerCase().trim();
        if (status.includes('pending')) {
            badge.classList.add('status-pending');
        } else if (status.includes('in progress')) {
            badge.classList.add('status-in_progress');
        } else if (status.includes('done')) {
            badge.classList.add('status-done');
        } else if (status.includes('overdue')) {
            badge.classList.add('status-overdue');
        }
    });
    
    // Update colors for priority badges
    document.querySelectorAll('.priority-badge').forEach(badge => {
        const priority = badge.textContent.toLowerCase().trim();
        if (priority.includes('low')) {
            badge.classList.add('priority-low');
        } else if (priority.includes('medium')) {
            badge.classList.add('priority-medium');
        } else if (priority.includes('high')) {
            badge.classList.add('priority-high');
        } else if (priority.includes('critical')) {
            badge.classList.add('priority-critical');
        }
    });
}

/**
 * Setup status dropdown change handlers
 */
function setupStatusDropdowns() {
    // For status-form quick status changes
    document.querySelectorAll('.status-form').forEach(form => {
        const statusInput = form.querySelector('input[name="status"]');
        const submitButton = form.querySelector('button[type="submit"]');
        
        if (submitButton && statusInput) {
            submitButton.addEventListener('click', function() {
                const newStatus = statusInput.value;
                const statusBadge = document.querySelector('.status-badge');
                
                // Check if status badge exists before reading from it
                if (statusBadge) {
                    const currentStatus = statusBadge.textContent.toLowerCase().trim();
                    
                    // Only submit if status is different
                    if (newStatus !== currentStatus.replace(' ', '_')) {
                        form.submit();
                    }
                } else {
                    // No status badge found, just submit the form
                    form.submit();
                }
            });
        }
    });
}

/**
 * Initialize tab navigation
 */
function initTabNavigation() {
    const triggerTabList = [].slice.call(document.querySelectorAll('button[data-bs-toggle="tab"]'));
    triggerTabList.forEach(function (triggerEl) {
        const tabTrigger = new bootstrap.Tab(triggerEl);
        
        triggerEl.addEventListener('click', function (event) {
            event.preventDefault();
            tabTrigger.show();
        });
    });
}

/**
 * Format date to YYYY-MM-DD format
 * @param {Date} date - Date object to format
 * @returns {string} - Formatted date string
 */
function formatDate(date) {
    if (!date) return '';
    
    if (!(date instanceof Date)) {
        date = new Date(date);
    }
    
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    
    return `${year}-${month}-${day}`;
}

/**
 * Show a toast notification
 * @param {string} message - Message to display
 * @param {string} type - Type of notification (success, warning, error, info)
 */
function showNotification(message, type = 'info') {
    // Check if notification container exists, if not create it
    let container = document.getElementById('notification-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'notification-container';
        container.className = 'position-fixed bottom-0 end-0 p-3';
        container.style.zIndex = '1050';
        document.body.appendChild(container);
    }
    
    // Create toast element
    const toastId = 'toast-' + Date.now();
    const toast = document.createElement('div');
    toast.id = toastId;
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    // Create toast content
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    // Add toast to container
    container.appendChild(toast);
    
    // Initialize and show toast
    const bsToast = new bootstrap.Toast(toast, {
        autohide: true,
        delay: 5000
    });
    bsToast.show();
    
    // Remove toast element after it's hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}
