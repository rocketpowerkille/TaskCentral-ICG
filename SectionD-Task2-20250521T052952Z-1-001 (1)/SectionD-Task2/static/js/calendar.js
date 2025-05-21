/**
 * TasksCentral - Calendar Functionality
 * This module provides calendar functionality for managing tasks with due dates.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize calendar if present
    initCalendar();
    
    // Initialize task detail popup functionality
    initTaskDetailPopup();
});

/**
 * Initialize the FullCalendar component
 */
function initCalendar() {
    const calendarEl = document.getElementById('calendar');
    
    if (calendarEl) {
        // Get events from the data attribute or an API call
        let events = [];
        
        // Check if the events are provided as a JavaScript variable
        if (typeof calendarEvents !== 'undefined') {
            events = calendarEvents;
        }
        
        // Create calendar instance
        const calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,listWeek'
            },
            events: events,
            eventClick: function(info) {
                showTaskDetail(info.event);
            },
            eventTimeFormat: {
                hour: 'numeric',
                minute: '2-digit',
                meridiem: 'short'
            },
            eventDidMount: function(info) {
                // Add tooltip with task title
                const tooltip = new bootstrap.Tooltip(info.el, {
                    title: info.event.title,
                    placement: 'top',
                    trigger: 'hover',
                    container: 'body'
                });
            },
            dayMaxEvents: true, // When too many events, show the "+more" link
            themeSystem: 'bootstrap5',
            aspectRatio: 1.8,
            height: 'auto'
        });
        
        // Render the calendar
        calendar.render();
        
        // Expose calendar globally if needed for later reference
        window.taskCalendar = calendar;
    }
}

/**
 * Initialize task detail popup functionality
 */
function initTaskDetailPopup() {
    const taskDetailBox = document.getElementById('taskDetailBox');
    
    if (taskDetailBox) {
        // Close when clicking on close button
        const closeButton = taskDetailBox.querySelector('.btn-close');
        if (closeButton) {
            closeButton.addEventListener('click', function() {
                hideTaskDetail();
            });
        }
        
        // Close when clicking outside the popup
        document.addEventListener('click', function(event) {
            if (taskDetailBox.style.display === 'block' && 
                !taskDetailBox.contains(event.target) && 
                !event.target.classList.contains('fc-event') &&
                !event.target.closest('.fc-event')) {
                hideTaskDetail();
            }
        });
        
        // Close when pressing Escape key
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape' && taskDetailBox.style.display === 'block') {
                hideTaskDetail();
            }
        });
        
        // Handle view task button click
        const viewTaskButton = taskDetailBox.querySelector('#taskLink');
        if (viewTaskButton) {
            viewTaskButton.addEventListener('click', function() {
                // Custom functionality can be added here if needed
                // By default, it just follows the href link
            });
        }
    }
}

/**
 * Show task detail popup
 * @param {Object} event - FullCalendar event object
 */
function showTaskDetail(event) {
    const detail = document.getElementById('taskDetailBox');
    if (!detail) return;
    
    // Get position of the event element
    const rect = event.el.getBoundingClientRect();
    
    // Calculate position to show the popup
    let top = rect.bottom + window.scrollY + 10;
    let left = rect.left;
    
    // Adjust if the popup would go off the right edge of the screen
    const popupWidth = 350; // Max width defined in CSS
    if (left + popupWidth > window.innerWidth) {
        left = window.innerWidth - popupWidth - 20;
    }
    
    // Position the popup
    detail.style.top = top + 'px';
    detail.style.left = left + 'px';
    
    // Set content
    document.getElementById('taskTitle').textContent = event.title;
    
    // Set status badge
    const status = event.extendedProps.status;
    const statusElem = document.getElementById('taskStatus');
    statusElem.textContent = formatString(status);
    statusElem.className = 'badge status-' + status + ' status-badge';
    
    // Set priority badge
    const priority = event.extendedProps.priority;
    const priorityElem = document.getElementById('taskPriority');
    priorityElem.textContent = formatString(priority);
    priorityElem.className = 'badge priority-' + priority + ' priority-badge';
    
    // Set category badge
    const category = event.extendedProps.category;
    const categoryElem = document.getElementById('taskCategory');
    categoryElem.textContent = formatString(category);
    
    // Set description (placeholder or actual description if available)
    const descriptionElem = document.getElementById('taskDescription');
    if (event.extendedProps.description) {
        descriptionElem.textContent = event.extendedProps.description;
    } else {
        descriptionElem.textContent = 'Task scheduled for the calendar.';
    }
    
    // Set due date
    const dueDateElem = document.getElementById('taskDueDate');
    let dateString = '';
    if (event.start) {
        dateString = formatDate(event.start);
    }
    dueDateElem.innerHTML = '<i class="fas fa-calendar-day me-1"></i> Due: ' + dateString;
    
    // Set link to view task details
    const taskLinkElem = document.getElementById('taskLink');
    taskLinkElem.href = '/tasks/' + event.id;
    
    // Show the popup
    detail.style.display = 'block';
}

/**
 * Hide task detail popup
 */
function hideTaskDetail() {
    const detail = document.getElementById('taskDetailBox');
    if (detail) {
        detail.style.display = 'none';
    }
}

/**
 * Format date as a readable string
 * @param {Date} date - Date object
 * @returns {string} - Formatted date string
 */
function formatDate(date) {
    if (!date) return 'Not set';
    
    const options = { 
        weekday: 'short', 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    };
    
    return date.toLocaleDateString(undefined, options);
}

/**
 * Format a string to title case and replace underscores with spaces
 * @param {string} str - String to format
 * @returns {string} - Formatted string
 */
function formatString(str) {
    if (!str) return '';
    
    // Replace underscores with spaces
    str = str.replace(/_/g, ' ');
    
    // Convert to title case
    return str.split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

/**
 * Fetch additional task details for a given task ID
 * @param {string} taskId - ID of the task
 * @returns {Promise} - Promise that resolves with task details
 */
function fetchTaskDetails(taskId) {
    return fetch(`/api/tasks/${taskId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch task details');
            }
            return response.json();
        })
        .catch(error => {
            console.error('Error fetching task details:', error);
            return null;
        });
}

/**
 * Add a new event to the calendar
 * @param {Object} taskData - Task data object
 */
function addCalendarEvent(taskData) {
    if (window.taskCalendar) {
        const event = {
            id: taskData.id,
            title: taskData.title,
            start: taskData.due_date,
            color: getColorForStatus(taskData.status),
            extendedProps: {
                status: taskData.status,
                priority: taskData.priority,
                category: taskData.category,
                description: taskData.description
            }
        };
        
        window.taskCalendar.addEvent(event);
    }
}

/**
 * Update an existing event on the calendar
 * @param {Object} taskData - Updated task data
 */
function updateCalendarEvent(taskData) {
    if (window.taskCalendar) {
        const existingEvent = window.taskCalendar.getEventById(taskData.id);
        
        if (existingEvent) {
            existingEvent.setProp('title', taskData.title);
            existingEvent.setStart(taskData.due_date);
            existingEvent.setProp('color', getColorForStatus(taskData.status));
            existingEvent.setExtendedProp('status', taskData.status);
            existingEvent.setExtendedProp('priority', taskData.priority);
            existingEvent.setExtendedProp('category', taskData.category);
            existingEvent.setExtendedProp('description', taskData.description);
        }
    }
}

/**
 * Remove an event from the calendar
 * @param {string} taskId - ID of the task to remove
 */
function removeCalendarEvent(taskId) {
    if (window.taskCalendar) {
        const existingEvent = window.taskCalendar.getEventById(taskId);
        
        if (existingEvent) {
            existingEvent.remove();
        }
    }
}

/**
 * Get color for task status
 * @param {string} status - Task status
 * @returns {string} - Color code
 */
function getColorForStatus(status) {
    switch (status) {
        case 'done':
            return '#2ecc71'; // Green
        case 'overdue':
            return '#e74c3c'; // Red
        case 'in_progress':
            return '#3498db'; // Blue
        case 'pending':
            return '#f39c12'; // Orange
        default:
            return '#3498db'; // Default blue
    }
}

/**
 * Refresh the calendar with new data
 * @param {Array} events - Array of event objects
 */
function refreshCalendar(events) {
    if (window.taskCalendar) {
        // Remove all existing events
        window.taskCalendar.getEvents().forEach(event => event.remove());
        
        // Add new events
        events.forEach(event => {
            window.taskCalendar.addEvent(event);
        });
    }
}

/**
 * Toggle between calendar views
 * @param {string} view - View name (e.g., 'dayGridMonth', 'timeGridWeek', 'listWeek')
 */
function switchCalendarView(view) {
    if (window.taskCalendar) {
        window.taskCalendar.changeView(view);
    }
}

/**
 * Navigate to specific date in calendar
 * @param {Date|string} date - Date to navigate to
 */
function gotoCalendarDate(date) {
    if (window.taskCalendar) {
        window.taskCalendar.gotoDate(date);
    }
}

/**
 * Filter calendar events by criteria
 * @param {Function} filterFn - Filter function that takes an event and returns boolean
 */
function filterCalendarEvents(filterFn) {
    if (window.taskCalendar) {
        const events = window.taskCalendar.getEvents();
        
        events.forEach(event => {
            if (filterFn(event)) {
                event.setProp('display', 'auto');
            } else {
                event.setProp('display', 'none');
            }
        });
    }
}

/**
 * Export calendar events to iCalendar format
 * @returns {string} - iCalendar formatted string
 */
function exportToICal() {
    if (!window.taskCalendar) return null;
    
    const events = window.taskCalendar.getEvents();
    let icalContent = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//TasksCentral//Calendar//EN'
    ];
    
    events.forEach(event => {
        const startDate = event.start ? formatICalDate(event.start) : '';
        const endDate = event.end ? formatICalDate(event.end) : startDate;
        
        icalContent.push('BEGIN:VEVENT');
        icalContent.push(`UID:${event.id}@taskscentral`);
        icalContent.push(`DTSTAMP:${formatICalDate(new Date())}`);
        icalContent.push(`DTSTART:${startDate}`);
        icalContent.push(`DTEND:${endDate}`);
        icalContent.push(`SUMMARY:${event.title}`);
        icalContent.push(`DESCRIPTION:Status: ${event.extendedProps.status}, Priority: ${event.extendedProps.priority}, Category: ${event.extendedProps.category}`);
        icalContent.push('END:VEVENT');
    });
    
    icalContent.push('END:VCALENDAR');
    return icalContent.join('\n');
}

/**
 * Format date for iCalendar format
 * @param {Date} date - Date object
 * @returns {string} - Formatted date string
 */
function formatICalDate(date) {
    if (!date) return '';
    
    return date.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
}

/**
 * Download calendar as iCalendar file
 */
function downloadCalendarAsICal() {
    const icalContent = exportToICal();
    if (!icalContent) return;
    
    const blob = new Blob([icalContent], { type: 'text/calendar;charset=utf-8' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'taskscentral_calendar.ics';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
