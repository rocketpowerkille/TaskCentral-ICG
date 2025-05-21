/**
 * TasksCentral - Tasks Management
 * 
 * This JavaScript file handles all task-related functionality including:
 * - Task filtering and sorting
 * - Status updates via AJAX
 * - Task deletion with confirmation
 * - Form validation for task creation/editing
 * 
 * Tasks are one of the core features of our application, so this file
 * contains significant functionality for task management.
 */

/**
 * Main initialization function that runs when the page loads
 * This uses the DOMContentLoaded event which fires when the HTML document
 * has been completely parsed, but before all resources finish loading
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize filter form submission - For filtering task lists by various criteria
    // This enhances usability by letting users quickly find relevant tasks
    initFilterForm();
    
    // Initialize task status update handlers - For updating task status without page reload
    // This provides a smoother user experience when changing task statuses
    initQuickStatusUpdate();
    
    // Initialize task deletion confirmation - Prevents accidental task deletion
    // This adds a safety check before permanently removing tasks
    initTaskDeletion();
    
    // Initialize form validation - Ensures data integrity when creating/editing tasks
    // This prevents invalid data from being submitted
    initFormValidation();
});

/**
 * Initialize task filter form
 * 
 * This function sets up the task filtering system to automatically submit
 * when a filter option changes, providing immediate feedback to users.
 * 
 * The filter form allows filtering by:
 * - Status (pending, in progress, done, overdue)
 * - Priority (low, medium, high, critical)
 * - Assigned user
 * - Project
 * - Category
 */
function initFilterForm() {
    // Get the filter form element if it exists on the current page
    const filterForm = document.getElementById('filterForm');
    
    if (filterForm) {
        // Auto-submit form on select change - This creates a responsive filtering experience
        // Find all dropdown selects within the filter form
        const selects = filterForm.querySelectorAll('.form-select');
        
        // Add change event listener to each select element
        selects.forEach(select => {
            select.addEventListener('change', function() {
                // Submit the form automatically when a filter changes
                filterForm.submit();
            });
        });
        
        // Add reset button functionality
        const resetButton = filterForm.querySelector('a.btn-outline-secondary');
        if (resetButton) {
            resetButton.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Reset all form selects
                selects.forEach(select => {
                    select.selectedIndex = 0;
                });
                
                // Submit the form
                filterForm.submit();
            });
        }
    }
}

/**
 * Initialize quick status update functionality
 */
function initQuickStatusUpdate() {
    const statusForms = document.querySelectorAll('.status-form');
    
    statusForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const statusInput = form.querySelector('input[name="status"]');
            const formData = new FormData(form);
            
            // Submit the form using fetch API
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (response.ok) {
                    // On success, reload the page to show updated status
                    window.location.reload();
                } else {
                    // Handle error
                    throw new Error('Failed to update task status');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Failed to update task status', 'danger');
            });
        });
    });
}

/**
 * Initialize task deletion confirmation modal
 */
function initTaskDeletion() {
    const deleteTaskModal = document.getElementById('deleteTaskModal');
    
    if (deleteTaskModal) {
        deleteTaskModal.addEventListener('show.bs.modal', function(event) {
            // Button that triggered the modal
            const button = event.relatedTarget;
            
            // Extract task info from data attributes if needed
            const taskTitle = document.querySelector('h1').textContent;
            
            // Update the modal's content
            const modalTitle = deleteTaskModal.querySelector('.modal-title');
            const modalBody = deleteTaskModal.querySelector('.modal-body p:first-child');
            
            modalTitle.textContent = 'Confirm Delete';
            modalBody.innerHTML = `Are you sure you want to delete the task <strong>${taskTitle}</strong>?`;
        });
    }
}

/**
 * Initialize form validation
 */
function initFormValidation() {
    // Task form
    const taskForm = document.querySelector('form[action*="task"]');
    
    if (taskForm) {
        taskForm.addEventListener('submit', function(e) {
            if (!validateTaskForm(taskForm)) {
                e.preventDefault();
            }
        });
    }
    
    // Project form
    const projectForm = document.querySelector('form[action*="project"]');
    
    if (projectForm) {
        projectForm.addEventListener('submit', function(e) {
            if (!validateProjectForm(projectForm)) {
                e.preventDefault();
            }
        });
    }
}

/**
 * Validate task form
 * @param {HTMLFormElement} form - The form element to validate
 * @returns {boolean} - True if valid, false otherwise
 */
function validateTaskForm(form) {
    let isValid = true;
    
    // Required fields
    const title = form.querySelector('input[name="title"]');
    const description = form.querySelector('textarea[name="description"]');
    
    // Validate title
    if (!title.value.trim()) {
        markInvalid(title, 'Title is required');
        isValid = false;
    } else {
        markValid(title);
    }
    
    // Validate description
    if (!description.value.trim()) {
        markInvalid(description, 'Description is required');
        isValid = false;
    } else {
        markValid(description);
    }
    
    // Validate due date (if provided)
    const dueDate = form.querySelector('input[name="due_date"]');
    if (dueDate && dueDate.value) {
        const selectedDate = new Date(dueDate.value);
        if (isNaN(selectedDate.getTime())) {
            markInvalid(dueDate, 'Invalid date format');
            isValid = false;
        } else {
            markValid(dueDate);
        }
    }
    
    return isValid;
}

/**
 * Validate project form
 * @param {HTMLFormElement} form - The form element to validate
 * @returns {boolean} - True if valid, false otherwise
 */
function validateProjectForm(form) {
    let isValid = true;
    
    // Required fields
    const name = form.querySelector('input[name="name"]');
    const description = form.querySelector('textarea[name="description"]');
    
    // Validate name
    if (!name.value.trim()) {
        markInvalid(name, 'Project name is required');
        isValid = false;
    } else {
        markValid(name);
    }
    
    // Validate description
    if (!description.value.trim()) {
        markInvalid(description, 'Description is required');
        isValid = false;
    } else {
        markValid(description);
    }
    
    // Validate dates (if provided)
    const startDate = form.querySelector('input[name="start_date"]');
    const endDate = form.querySelector('input[name="end_date"]');
    
    if (startDate && startDate.value && endDate && endDate.value) {
        const start = new Date(startDate.value);
        const end = new Date(endDate.value);
        
        if (start > end) {
            markInvalid(endDate, 'End date must be after start date');
            isValid = false;
        } else {
            markValid(startDate);
            markValid(endDate);
        }
    }
    
    return isValid;
}

/**
 * Mark a form field as invalid
 * @param {HTMLElement} field - The form field
 * @param {string} message - Error message
 */
function markInvalid(field, message) {
    field.classList.add('is-invalid');
    
    // Add or update feedback message
    let feedback = field.nextElementSibling;
    if (!feedback || !feedback.classList.contains('invalid-feedback')) {
        feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        field.parentNode.insertBefore(feedback, field.nextSibling);
    }
    
    feedback.textContent = message;
}

/**
 * Mark a form field as valid
 * @param {HTMLElement} field - The form field
 */
function markValid(field) {
    field.classList.remove('is-invalid');
    field.classList.add('is-valid');
    
    // Remove feedback message if exists
    const feedback = field.nextElementSibling;
    if (feedback && feedback.classList.contains('invalid-feedback')) {
        feedback.remove();
    }
}
