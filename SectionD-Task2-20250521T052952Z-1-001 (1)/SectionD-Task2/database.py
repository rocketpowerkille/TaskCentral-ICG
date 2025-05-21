import uuid  # For generating unique IDs
from datetime import datetime, timedelta  # For date/time operations and calculations
# Import all our data models - these define the structure of our application's objects
from models import (
    User, Task, Project, Comment, Meeting, Decision, Milestone, Note,
    TaskStatus, TaskPriority, TaskCategory, ProjectStatus, MilestoneStatus, NoteColor,
    CommentType
)

users = {}
tasks = {}
projects = {}
comments = {}
meetings = {}
decisions = {}
milestones = {}
sessions = {}
notes = {}

def init_db():
    """Initialize the database with some sample data
    
    This function populates our in-memory database with initial data so we have
    something to work with when the application starts. In a real application,
    we would load data from an actual database instead.
    """
    # Create default admin user - Every system needs at least one admin account
    # This ensures we always have a way to access the system with full privileges
    create_user("admin", "admin@example.com", "admin123", "manager", "Admin User")
    
    # demo team members - These are sample users for testing and demonstration
    # In a real application, users would register themselves or be added by an admin
    create_user("vishu", "vishu.khare@company.com", "password123", "member", "Vishu Khare")
    create_user("member2", "member2@company.com", "password123", "member", "Member 2")
    create_user("member3", "member3@company.com", "password123", "member", "Member 3")
    create_user("member4", "member4@company.com", "password123", "member", "Member 4")
    
    # some projects with team members
   
    current_date = datetime.now().date()
    
    project1_id = create_project(
        "Wadhwani AI Project", 
        "Advancing AI driven EdTech solutions for improved student engagement",
        current_date, 
        current_date + timedelta(days=30), 
        "admin",
        ProjectStatus.ACTIVE.value,
        ["vishu", "member2"]
    )
    
    project2_id = create_project(
        "Adani Group Hospital Project", 
        "Feasibility study for new hospital in Dharavi", 
        current_date - timedelta(days=30), 
        current_date + timedelta(days=90), 
        "admin",
        ProjectStatus.ACTIVE.value,
        ["member2", "member3"]
    )
    
    project3_id = create_project(
        "Project Phoenix", 
        "Develop and roll out security awareness training", 
        current_date, 
        current_date + timedelta(days=45), 
        "admin",
        ProjectStatus.PLANNED.value,
        ["vishu", "member4"]
    )
    
    # Create completed project for demo
    project4_id = create_project(
        "Project Blackmirror", 
        "Developing a new futureistc memory aid", 
        current_date - timedelta(days=60), 
        current_date - timedelta(days=30), 
        "admin",
        ProjectStatus.COMPLETED.value,
        ["vishu", "member2", "member3"]
    )
    
    # Create some milestones for projects
    milestone1_id = create_milestone(
        "Project Blackmirror - Phase 1",
        "Tie ups with various R&D labs",
        project1_id,
        datetime.now() + timedelta(days=7),
        "admin",
        MilestoneStatus.IN_PROGRESS.value
    )
    
    milestone2_id = create_milestone(
        "Project Blackmirror - Phase 2",
        "Implement recommended Hardware controls",
        project1_id,
        datetime.now() + timedelta(days=20),
        "admin"
    )
    
    milestone3_id = create_milestone(
        "Project Blackmirror - Phase 3",
        "Implement new software controls", 
        project2_id,
        datetime.now() + timedelta(days=5),
        "admin",
        MilestoneStatus.PLANNED.value
    )
    
 
   
    
    # Create milestones for completed project
    milestone6_id = create_milestone(
        "Policy Review Complete",
        "All security policies reviewed and updated",
        project4_id,
        datetime.now() - timedelta(days=35),
        "admin",
        MilestoneStatus.COMPLETED.value
    )
    
   
    
    # Create varied tasks for Wadhwani AI Project (project1_id)
    create_task(
        "AI Model Validation", 
        "Validate machine learning models for student engagement prediction",
        TaskStatus.IN_PROGRESS.value,
        TaskPriority.HIGH.value,
        TaskCategory.PROJECT.value,
        current_date + timedelta(days=5),
        "admin",
        "vishu",
        project1_id
    )

    create_task(
        "Data Pipeline Setup",
        "Set up ETL pipeline for student interaction data",
        TaskStatus.PENDING.value,
        TaskPriority.MEDIUM.value,
        TaskCategory.PROJECT.value,
        current_date + timedelta(days=10),
        "admin",
        "member2",
        project1_id
    )

    create_task(
        "Weekly Algorithm Review",
        "Review and optimize AI model performance metrics",
        TaskStatus.DONE.value,
        TaskPriority.MEDIUM.value,
        TaskCategory.BAU.value,
        current_date - timedelta(days=1),
        "admin",
        "vishu",
        project1_id
    )

    # Create varied tasks for Adani Hospital Project (project2_id)
    create_task(
        "Hospital Requirements Analysis",
        "Document detailed requirements for hospital systems",
        TaskStatus.OVERDUE.value,
        TaskPriority.CRITICAL.value,
        TaskCategory.PROJECT.value,
        current_date - timedelta(days=2),
        "admin",
        "member3",
        project2_id
    )

    create_task(
        "Equipment Inventory Planning",
        "Create inventory plan for medical equipment",
        TaskStatus.IN_PROGRESS.value,
        TaskPriority.HIGH.value,
        TaskCategory.PROJECT.value,
        current_date + timedelta(days=15),
        "admin",
        "member2",
        project2_id
    )

    create_task(
        "Daily Progress Report",
        "Update project status and metrics",
        TaskStatus.PENDING.value,
        TaskPriority.LOW.value,
        TaskCategory.BAU.value,
        current_date + timedelta(days=1),
        "admin",
        "member3",
        project2_id
    )

    # Create varied tasks for Project Phoenix (project3_id)
    create_task(
        "Training Content Development",
        "Create interactive security awareness modules",
        TaskStatus.IN_PROGRESS.value,
        TaskPriority.HIGH.value,
        TaskCategory.PROJECT.value,
        current_date + timedelta(days=7),
        "admin",
        "member4",
        project3_id
    )

    create_task(
        "Phishing Simulation Setup",
        "Configure phishing simulation campaign",
        TaskStatus.PENDING.value,
        TaskPriority.MEDIUM.value,
        TaskCategory.PROJECT.value,
        current_date + timedelta(days=12),
        "admin",
        "member3",
        project3_id
    )

    # Create some standalone tasks (not linked to projects)
    create_task(
        "System Health Check",
        "Perform monthly system health assessment",
        TaskStatus.OVERDUE.value,
        TaskPriority.HIGH.value,
        TaskCategory.INCIDENT.value,
        current_date - timedelta(days=3),
        "admin",
        "member2",
        None
    )

    create_task(
        "Team Meeting Preparation",
        "Prepare agenda and materials for weekly team sync",
        TaskStatus.PENDING.value,
        TaskPriority.LOW.value,
        TaskCategory.MEETING_PREP.value,
        current_date + timedelta(days=2),
        "admin",
        "vishu",
        None
    )

    create_task(
        "Software License Review",
        "Audit software licenses and prepare renewal plan",
        TaskStatus.DONE.value,
        TaskPriority.MEDIUM.value,
        TaskCategory.BAU.value,
        current_date - timedelta(days=1),
        "admin",
        "member4",
        None
    )

    create_task(
        "Infrastructure Upgrade Decision",
        "Document decision for cloud infrastructure upgrade",
        TaskStatus.IN_PROGRESS.value,
        TaskPriority.CRITICAL.value,
        TaskCategory.DECISION_LOG.value,
        current_date + timedelta(days=3),
        "admin",
        "vishu",
        None
    )

    create_task(
        "Update Security Policies", 
        "Review and update data classification policies", 
        TaskStatus.OVERDUE.value, 
        TaskPriority.MEDIUM.value, 
        TaskCategory.BAU.value, 
        datetime.now() - timedelta(days=5), 
        "admin", 
        "vishu", 
        None
    )
    
    # Create some sample notes
    create_note(
        "Incident Response Checklist",
        "1. Identify and assess the incident\n2. Contain the incident\n3. Eradicate the threat\n4. Recover systems\n5. Document lessons learned",
        "admin",
        NoteColor.YELLOW.value,
        True  # Pinned
    )
    
    create_note(
        "Security Meeting Agenda",
        "- Review recent security incidents\n- Discuss progress on vulnerability remediation\n- Plan for upcoming security awareness training\n- Review security policy updates",
        "admin",
        NoteColor.BLUE.value,
        False
    )
    
    create_note(
        "Reminder: Change VPN Certificates",
        "Need to update VPN certificates by end of month. Contact vendor for new certs.",
        "admin",
        NoteColor.ORANGE.value,
        True  # Pinned
    )

def create_user(username, email, password, role="member", name=None):
    """Create a new user and return user_id"""
    user_id = str(uuid.uuid4())
    user = User(user_id, username, email, password, role, name)
    users[user_id] = user
    return user_id

def get_user_by_id(user_id):
    """Get user by ID"""
    return users.get(user_id)

def get_user_by_username(username):
    """Get user by username"""
    for user in users.values():
        if user.username == username:
            return user
    return None

def get_user_by_email(email):
    """Get user by email"""
    for user in users.values():
        if user.email == email:
            return user
    return None

def get_all_users():
    """Get all users"""
    return list(users.values())

def create_task(title, description, status, priority, category, due_date, created_by, assigned_to=None, project_id=None, meeting_id=None, related_decision=None):
    """Create a new task and return task_id"""
    task_id = str(uuid.uuid4())
    task = Task(
        task_id, title, description, status, priority, category, 
        due_date, created_by, assigned_to, project_id,
        meeting_id, related_decision
    )
    tasks[task_id] = task
    
    # Add to user's tasks if assigned
    if assigned_to and assigned_to in users:
        users[assigned_to].tasks.append(task_id)
    
    # Add to project's tasks if part of a project
    if project_id and project_id in projects:
        projects[project_id].tasks.append(task_id)
    
    # Add to meeting's tasks if associated with a meeting
    if meeting_id and meeting_id in meetings:
        meetings[meeting_id].tasks.append(task_id)
    
    # Add to decision's tasks if resulting from a decision
    if related_decision and related_decision in decisions:
        decisions[related_decision].tasks.append(task_id)
        
    return task_id

def get_task(task_id):
    """Get task by ID"""
    return tasks.get(task_id)

def get_all_tasks():
    """Get all tasks"""
    return list(tasks.values())

def get_tasks_by_user(user_id):
    """Get all tasks assigned to a user"""
    user_tasks = []
    for task in tasks.values():
        if task.assigned_to == user_id:
            user_tasks.append(task)
    return user_tasks

def get_tasks_by_project(project_id):
    """Get all tasks for a project"""
    project_tasks = []
    for task in tasks.values():
        if task.project_id == project_id:
            project_tasks.append(task)
    return project_tasks

def update_task(task_id, **kwargs):
    """Update a task"""
    if task_id in tasks:
        task = tasks[task_id]
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        task.updated_at = datetime.now()
        return True
    return False

def delete_task(task_id):
    """Delete a task"""
    if task_id in tasks:
        task = tasks[task_id]
        
        # Remove from user's tasks
        if task.assigned_to and task.assigned_to in users:
            if task_id in users[task.assigned_to].tasks:
                users[task.assigned_to].tasks.remove(task_id)
        
        # Remove from project's tasks
        if task.project_id and task.project_id in projects:
            if task_id in projects[task.project_id].tasks:
                projects[task.project_id].tasks.remove(task_id)
        
        # Delete task
        del tasks[task_id]
        return True
    return False

def create_project(name, description, start_date, end_date, created_by, 
                status=ProjectStatus.PLANNED.value, team_members=None):
    """Create a new project and return project_id"""
    project_id = str(uuid.uuid4())
    project = Project(project_id, name, description, start_date, end_date, created_by, status, team_members)
    projects[project_id] = project
    
    # Add project to each team member's project list
    if team_members:
        for member_id in team_members:
            if member_id in users:
                if project_id not in users[member_id].projects:
                    users[member_id].projects.append(project_id)
    
    return project_id

def get_project(project_id):
    """Get project by ID"""
    return projects.get(project_id)

def get_all_projects():
    """Get all projects"""
    return list(projects.values())

def update_project(project_id, **kwargs):
    """Update a project"""
    if project_id in projects:
        project = projects[project_id]
        for key, value in kwargs.items():
            if hasattr(project, key):
                setattr(project, key, value)
        project.updated_at = datetime.now()
        return True
    return False

def delete_project(project_id):
    """Delete a project"""
    if project_id in projects:
        project = projects[project_id]
        
        # Remove project from team members' project lists
        for member_id in project.team_members:
            if member_id in users and project_id in users[member_id].projects:
                users[member_id].projects.remove(project_id)
        
        # Update all tasks to remove project reference
        for task in tasks.values():
            if task.project_id == project_id:
                task.project_id = None
        
        # Delete all milestones associated with this project
        milestones_to_delete = []
        for milestone_id, milestone in milestones.items():
            if milestone.project_id == project_id:
                milestones_to_delete.append(milestone_id)
                
        for milestone_id in milestones_to_delete:
            delete_milestone(milestone_id)
            
        # Delete project
        del projects[project_id]
        return True
    return False

def create_comment(user_id, content, entity_type, entity_id):
    """Create a new comment and return comment_id"""
    comment_id = str(uuid.uuid4())
    comment = Comment(comment_id, user_id, content, entity_type, entity_id)
    comments[comment_id] = comment
    
    # Add to entity's comments
    if entity_type == CommentType.TASK.value and entity_id in tasks:
        tasks[entity_id].comments.append(comment_id)
    elif entity_type == CommentType.PROJECT.value and entity_id in projects:
        projects[entity_id].comments.append(comment_id)
    elif entity_type == CommentType.MILESTONE.value and entity_id in milestones:
        milestones[entity_id].comments.append(comment_id)
    
    return comment_id

def get_comments_by_entity(entity_type, entity_id):
    """Get all comments for a specific entity"""
    entity_comments = []
    for comment in comments.values():
        if comment.entity_type == entity_type and comment.entity_id == entity_id:
            entity_comments.append(comment)
    return entity_comments

def get_comments_by_task(task_id):
    """Get all comments for a task (legacy support)"""
    return get_comments_by_entity(CommentType.TASK.value, task_id)

def get_comments_by_project(project_id):
    """Get all comments for a project"""
    return get_comments_by_entity(CommentType.PROJECT.value, project_id)

def get_comments_by_milestone(milestone_id):
    """Get all comments for a milestone"""
    return get_comments_by_entity(CommentType.MILESTONE.value, milestone_id)

def save_session(user_id, session_id):
    """Save user session"""
    sessions[session_id] = {
        "user_id": user_id,
        "created_at": datetime.now()
    }

def get_session(session_id):
    """Get session by ID"""
    return sessions.get(session_id)

def delete_session(session_id):
    """Delete a session"""
    if session_id in sessions:
        del sessions[session_id]
        return True
    return False

def create_meeting(title, description, date, organizer, attendees=None):
    """Create a new meeting and return meeting_id"""
    meeting_id = str(uuid.uuid4())
    meeting = Meeting(meeting_id, title, description, date, organizer, attendees)
    meetings[meeting_id] = meeting
    return meeting_id

def get_meeting(meeting_id):
    """Get meeting by ID"""
    return meetings.get(meeting_id)

def get_all_meetings():
    """Get all meetings"""
    return list(meetings.values())

def get_meetings_by_user(user_id):
    """Get all meetings organized by or attended by a user"""
    user_meetings = []
    for meeting in meetings.values():
        if meeting.organizer == user_id or user_id in meeting.attendees:
            user_meetings.append(meeting)
    return user_meetings

def update_meeting(meeting_id, **kwargs):
    """Update a meeting"""
    if meeting_id in meetings:
        meeting = meetings[meeting_id]
        for key, value in kwargs.items():
            if hasattr(meeting, key):
                setattr(meeting, key, value)
        meeting.updated_at = datetime.now()
        return True
    return False

def delete_meeting(meeting_id):
    """Delete a meeting"""
    if meeting_id in meetings:
        # Update all tasks to remove meeting reference
        for task in tasks.values():
            if task.meeting_id == meeting_id:
                task.meeting_id = None
        
        # Update all decisions to remove meeting reference
        for decision in decisions.values():
            if decision.meeting_id == meeting_id:
                # We might want to delete decisions or just orphan them
                # For now, we'll just orphan them by setting meeting_id to None
                decision.meeting_id = None
        
        # Delete meeting
        del meetings[meeting_id]
        return True
    return False

def create_decision(title, description, meeting_id, made_by, date=None):
    """Create a new decision and return decision_id"""
    decision_id = str(uuid.uuid4())
    decision = Decision(decision_id, title, description, meeting_id, made_by, date)
    decisions[decision_id] = decision
    
    # Add to meeting's decisions if associated with a meeting
    if meeting_id and meeting_id in meetings:
        meetings[meeting_id].decisions.append(decision_id)
    
    return decision_id

def get_decision(decision_id):
    """Get decision by ID"""
    return decisions.get(decision_id)

def get_all_decisions():
    """Get all decisions"""
    return list(decisions.values())

def get_decisions_by_meeting(meeting_id):
    """Get all decisions made in a meeting"""
    meeting_decisions = []
    for decision in decisions.values():
        if decision.meeting_id == meeting_id:
            meeting_decisions.append(decision)
    return meeting_decisions

def update_decision(decision_id, **kwargs):
    """Update a decision"""
    if decision_id in decisions:
        decision = decisions[decision_id]
        for key, value in kwargs.items():
            if hasattr(decision, key):
                setattr(decision, key, value)
        return True
    return False

def delete_decision(decision_id):
    """Delete a decision"""
    if decision_id in decisions:
        decision = decisions[decision_id]
        
        # Remove from meeting's decisions
        if decision.meeting_id and decision.meeting_id in meetings:
            if decision_id in meetings[decision.meeting_id].decisions:
                meetings[decision.meeting_id].decisions.remove(decision_id)
        
        # Update all tasks to remove decision reference
        for task in tasks.values():
            if task.related_decision == decision_id:
                task.related_decision = None
        
        # Delete decision
        del decisions[decision_id]
        return True
    return False

def create_milestone(title, description, project_id, due_date, created_by, status=MilestoneStatus.PLANNED.value):
    """Create a new milestone and return milestone_id"""
    milestone_id = str(uuid.uuid4())
    milestone = Milestone(milestone_id, title, description, project_id, due_date, created_by, status)
    milestones[milestone_id] = milestone
    
    # Add to project's milestones if associated with a project
    if project_id and project_id in projects:
        projects[project_id].milestones.append(milestone_id)
    
    return milestone_id

def get_milestone(milestone_id):
    """Get milestone by ID"""
    return milestones.get(milestone_id)

def get_all_milestones():
    """Get all milestones"""
    return list(milestones.values())

def get_milestones_by_project(project_id):
    """Get all milestones for a project"""
    project_milestones = []
    for milestone in milestones.values():
        if milestone.project_id == project_id:
            project_milestones.append(milestone)
    return project_milestones

def get_milestones_by_date_range(start_date, end_date):
    """Get all milestones due within a date range"""
    range_milestones = []
    for milestone in milestones.values():
        if milestone.due_date:
            # Convert milestone.due_date to date if it's a datetime
            milestone_date = milestone.due_date.date() if hasattr(milestone.due_date, 'date') else milestone.due_date
            if start_date <= milestone_date <= end_date:
                range_milestones.append(milestone)
    return range_milestones

def get_upcoming_milestones(days=30):
    """Get milestones due in the next X days"""
    today = datetime.now().date()
    end_date = today + timedelta(days=days)
    return get_milestones_by_date_range(today, end_date)

def update_milestone(milestone_id, **kwargs):
    """Update a milestone"""
    if milestone_id in milestones:
        milestone = milestones[milestone_id]
        for key, value in kwargs.items():
            if hasattr(milestone, key):
                setattr(milestone, key, value)
        milestone.updated_at = datetime.now()
        return True
    return False

def delete_milestone(milestone_id):
    """Delete a milestone"""
    if milestone_id in milestones:
        milestone = milestones[milestone_id]
        
        # Remove from project's milestones
        if milestone.project_id and milestone.project_id in projects:
            if milestone_id in projects[milestone.project_id].milestones:
                projects[milestone.project_id].milestones.remove(milestone_id)
        
        # Update tasks to remove milestone reference (if applicable)
        for task in tasks.values():
            if hasattr(task, 'milestone_id') and task.milestone_id == milestone_id:
                task.milestone_id = None
        
        # Delete milestone
        del milestones[milestone_id]
        return True
    return False

def calculate_project_completion(project_id):
    """Calculate project completion percentage based on completed tasks"""
    if project_id in projects:
        project = projects[project_id]
        total_tasks = len(project.tasks)
        
        if total_tasks == 0:
            return 0
            
        completed_tasks = 0
        for task_id in project.tasks:
            if task_id in tasks and tasks[task_id].status == TaskStatus.DONE.value:
                completed_tasks += 1
                
        completion_percentage = (completed_tasks / total_tasks) * 100
        
        # Update project's completion percentage
        project.completion_percentage = round(completion_percentage)
        
        return completion_percentage
    return 0

def calculate_milestone_completion(milestone_id):
    """Calculate milestone completion percentage based on completed tasks"""
    if milestone_id in milestones:
        milestone = milestones[milestone_id]
        total_tasks = len(milestone.tasks)
        
        if total_tasks == 0:
            return 0
            
        completed_tasks = 0
        for task_id in milestone.tasks:
            if task_id in tasks and tasks[task_id].status == TaskStatus.DONE.value:
                completed_tasks += 1
                
        completion_percentage = (completed_tasks / total_tasks) * 100
        
        # Update milestone's completion percentage
        milestone.completion_percentage = round(completion_percentage)
        
        return completion_percentage
    return 0

def get_projects_by_status(status):
    """Get all projects with a specific status"""
    status_projects = []
    for project in projects.values():
        if project.status == status:
            status_projects.append(project)
    return status_projects

def get_completed_projects():
    """Get all completed projects"""
    return get_projects_by_status(ProjectStatus.COMPLETED.value)

def add_user_to_project(user_id, project_id):
    """Add a user to a project's team members"""
    if user_id in users and project_id in projects:
        # Add user to project team members
        if user_id not in projects[project_id].team_members:
            projects[project_id].team_members.append(user_id)
            
        # Add project to user's projects
        if project_id not in users[user_id].projects:
            users[user_id].projects.append(project_id)
            
        return True
    return False

def remove_user_from_project(user_id, project_id):
    """Remove a user from a project's team members"""
    if user_id in users and project_id in projects:
        # Remove user from project team members
        if user_id in projects[project_id].team_members:
            projects[project_id].team_members.remove(user_id)
            
        # Remove project from user's projects
        if project_id in users[user_id].projects:
            users[user_id].projects.remove(project_id)
            
        return True
    return False

def get_user_projects(user_id):
    """Get all projects a user is part of"""
    if user_id in users:
        user_projects = []
        for project_id in users[user_id].projects:
            if project_id in projects:
                user_projects.append(projects[project_id])
        return user_projects
    return []

# Note functions
def create_note(title, content, user_id, color=NoteColor.YELLOW.value, pinned=False):
    """Create a new note and return note_id"""
    note_id = str(uuid.uuid4())
    note = Note(note_id, title, content, user_id, color, pinned)
    notes[note_id] = note
    return note_id

def get_note(note_id):
    """Get note by ID"""
    return notes.get(note_id)

def get_notes_by_user(user_id):
    """Get all notes created by a user"""
    user_notes = []
    for note in notes.values():
        if note.user_id == user_id:
            user_notes.append(note)
    return user_notes

def update_note(note_id, **kwargs):
    """Update a note"""
    if note_id in notes:
        note = notes[note_id]
        for key, value in kwargs.items():
            if hasattr(note, key):
                setattr(note, key, value)
        note.updated_at = datetime.now()
        return True
    return False

def delete_note(note_id):
    """Delete a note"""
    if note_id in notes:
        del notes[note_id]
        return True
    return False

def get_pinned_notes(user_id):
    """Get all pinned notes for a user"""
    pinned_notes = []
    for note in notes.values():
        if note.user_id == user_id and note.pinned:
            pinned_notes.append(note)
    return pinned_notes
