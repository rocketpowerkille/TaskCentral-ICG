# TeamTaskTracker - Project Management System

## Project Overview

TeamTaskTracker is a comprehensive web-based project and task management system designed for teams working on consulting and project management engagements. Built with Flask and a modern web stack, the application provides tools for tracking tasks, projects, milestones, meetings, decisions, and team collaboration.

## Core Functionality

### User Management
- **Role-Based Access Control**: Supports different user roles (manager and member) with appropriate permissions
- **Authentication System**: Secure login and registration with password hashing
- **User Profiles**: Individual user profiles with performance metrics and workload tracking

### Task Management
- **Task Creation & Assignment**: Create tasks with title, description, due dates, and assign to team members
- **Status Tracking**: Track tasks through various statuses (pending, in-progress, done, overdue)
- **Priority Levels**: Assign priority levels (low, medium, high, critical) to tasks
- **Categorization**: Organize tasks by customizable categories
- **Filtering & Sorting**: Advanced filtering options for task lists by status, priority, assignee, etc.
- **Automatic Status Updates**: Tasks automatically marked as overdue when past due date

### Project Management
- **Project Creation**: Create projects with detailed descriptions, goals, and team assignments
- **Project Status Tracking**: Monitor project progress through various status levels
- **Team Assignment**: Assign multiple team members to projects
- **Progress Visualization**: Visual representation of project completion rates
- **Project Dashboard**: Overview of project health, task distribution, and timeline

### Meeting Management
- **Meeting Scheduling**: Create and schedule team meetings with agendas
- **Attendee Management**: Assign and track meeting participants
- **Meeting Notes**: Record meeting discussions and outcomes
- **Meeting History**: Maintain a record of all project meetings

### Decision Tracking
- **Decision Documentation**: Record important decisions made during the project lifecycle
- **Decision Categories**: Categorize decisions for easy reference
- **Approval Workflow**: Track decision approval status

### Milestone Tracking
- **Milestone Creation**: Set project milestones with deadlines
- **Status Updates**: Track milestone completion status
- **Dependency Management**: Link milestones to related tasks and projects

### Notes & Documentation
- **Note Taking**: Create color-coded notes for various purposes
- **Attachments**: Support for documentation and file references
- **Searchable Content**: Easily find notes and documentation

### Reporting & Analytics
- **Task Distribution**: Visualize task distribution by category and priority
- **Team Workload**: Monitor team member workload and capacity
- **Completion Rates**: Track task and project completion rates
- **Overdue Analysis**: Identify bottlenecks through overdue task analysis
- **Performance Metrics**: Individual and team performance tracking

### Calendar & Timeline
- **Visual Calendar**: Calendar view of tasks, meetings, and milestones
- **Timeline Visualization**: Project timeline with key events and deadlines
- **Due Date Tracking**: Visual indicators for upcoming deadlines

## Technical Architecture

- **Backend**: Python Flask framework
- **Database**: In-memory database (for MVP), with MongoDB integration capability
- **Frontend**: HTML5, CSS3, JavaScript with Bootstrap 5
- **Security**: CSRF protection, password hashing, session management
- **Responsive Design**: Mobile-friendly interface that works on all device sizes

## Key Features

1. **Intuitive Dashboard**: Central hub showing task summaries, recent activities, and upcoming deadlines
2. **Real-time Updates**: Dynamic status updates without page reloads
3. **Data Visualization**: Charts and graphs for better project insights
4. **Collaborative Tools**: Team-oriented features for better collaboration
5. **Audit Trail**: Tracking changes and updates to tasks and projects
6. **Notification System**: Alerts for task assignments, updates, and approaching deadlines

## Getting Started
### Video Walkthrough
- https://drive.google.com/file/d/1NInGB4CBCq1beEB0jR4EOYDytJTR4Mzs/view?usp=sharing
  
### Prerequisites
- Python 3.11 or higher
- Required Python packages listed in requirements.txt

### Installation
1. Clone the repository
2. Install dependencies using `pip install -r requirements.txt .`
3. Run the application using `python main.py`
4. Access the application at http://localhost:5000

### Default Login
- Admin: username: `admin`, password: `admin123`
- Test User: username: `vishu`, password: `password123`

## Future Enhancements

- Email notifications
- File attachment system
- Advanced reporting and analytics
- API for third-party integrations
- Full database integration with PostgreSQL/MongoDB

