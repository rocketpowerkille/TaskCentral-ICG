# Import necessary libraries
from enum import Enum  
from datetime import datetime  
from werkzeug.security import generate_password_hash, check_password_hash  # For secure password handling


# Using an enum ensures consistency in our application and prevents typos or invalid colors
class NoteColor(Enum):
    YELLOW = "yellow"  
    BLUE = "blue"     
    GREEN = "green"   
    PINK = "pink"     
    ORANGE = "orange"  


class TaskStatus(Enum):
    PENDING = "pending"          # Task has been created but not started yet
    IN_PROGRESS = "in_progress"  # Task is currently being worked on
    DONE = "done"                # Task has been completed successfully
    OVERDUE = "overdue"          # Task deadline has passed without completion


class TaskPriority(Enum):
    LOW = "low"           # Can be done whenever time permits
    MEDIUM = "medium"     # Standard priority for regular tasks
    HIGH = "high"         # Important tasks that should be prioritized
    CRITICAL = "critical" # Urgent tasks that need immediate attention

# Task category enum
class TaskCategory(Enum):
    PROJECT = "project"
    BAU = "bau"  # Business As Usual
    MEETING_PREP = "meeting_prep"  # Meeting preparation
    MEETING_ACTION = "meeting_action"  # Action items from meetings
    MEETING_MINUTES = "meeting_minutes"  # Meeting minutes and documentation
    DECISION_LOG = "decision_log"  # For tracking decisions
    INCIDENT = "incident"
    OTHER = "other"
    
# Project status enum
class ProjectStatus(Enum):
    PLANNED = "planned"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    
# Milestone status enum
class MilestoneStatus(Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DELAYED = "delayed"
    CANCELLED = "cancelled"

# User model
# User class - Central to our application's authentication and authorization system
class User:
    def __init__(self, id, username, email, password, role="member", name=None):
        """
        Initialize a new User object
        
        Parameters:
        - id: Unique identifier for the user
        - username: Login name for the user (must be unique)
        - email: User's email address for notifications
        - password: Plain text password that will be hashed for security
        - role: User's permission level ('member' or 'manager')
        - name: User's full/display name (defaults to username if not provided)
        """
        self.id = id  # Unique identifier for database operations
        self.username = username  # Username for login (must be unique)
        self.email = email  # Email address for notifications
        # Store only the hashed password, never the plain text version!
        self.password_hash = generate_password_hash(password)  # Security best practice - hash passwords
        self.role = role  # 'manager' or 'member' - determines permissions in the app
        self.name = name or username  # Full name or display name (falls back to username)
        self.created_at = datetime.now()  # Timestamp when user account was created
        self.tasks = []  # List of assigned tasks - helps track user's responsibilities
        self.projects = []  # List of project IDs the user is part of - for project access control
        self.meetings = []  # List of meeting IDs the user is attending - for calendar/scheduling
        self.task_efficiency = 100  # Task completion efficiency score (percentage) - for performance metrics
        self.workload = 0  # Current workload score based on assigned tasks - helps prevent overallocation

    def check_password(self, password):
        """
        Securely verify if the provided password matches the stored hash
        This method never compares plain text passwords directly
        """
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """
        Convert user object to dictionary for JSON serialization
        Excludes sensitive data like password hash for security
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'name': self.name,
            'created_at': self.created_at.isoformat(),  # Convert datetime to string for JSON
            'task_count': len(self.tasks),  # Derived data - calculate on the fly
            'project_count': len(self.projects),  # Derived data - calculate on the fly
            'meeting_count': len(self.meetings),
            'task_efficiency': self.task_efficiency,
            'workload': self.workload
        }

# Task model
class Task:
    def __init__(self, id, title, description, status, priority, category, 
                 due_date, created_by, assigned_to=None, project_id=None, 
                 meeting_id=None, related_decision=None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.category = category
        self.due_date = due_date
        self.created_by = created_by
        self.assigned_to = assigned_to
        self.project_id = project_id
        self.meeting_id = meeting_id  # ID of associated meeting
        self.related_decision = related_decision  # ID of related decision
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.comments = []

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'category': self.category,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_by': self.created_by,
            'assigned_to': self.assigned_to,
            'project_id': self.project_id,
            'meeting_id': self.meeting_id,
            'related_decision': self.related_decision,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'comment_count': len(self.comments)
        }

# Project model
class Project:
    def __init__(self, id, name, description, start_date, end_date, created_by, 
                 status=ProjectStatus.PLANNED.value, team_members=None):
        self.id = id
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.created_by = created_by
        self.status = status
        self.team_members = team_members or []  # List of user IDs assigned to this project
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.tasks = []  # List of tasks in this project
        self.milestones = []  # List of milestone IDs for this project
        self.comments = []  # List of comment IDs for this project
        self.completion_percentage = 0  # Project completion percentage

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_by': self.created_by,
            'status': self.status,
            'team_members': self.team_members,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'task_count': len(self.tasks),
            'milestone_count': len(self.milestones),
            'completion_percentage': self.completion_percentage
        }

# Meeting model
class Meeting:
    def __init__(self, id, title, description, date, organizer, attendees=None):
        self.id = id
        self.title = title
        self.description = description
        self.date = date
        self.organizer = organizer  # User ID
        self.attendees = attendees or []  # List of user IDs
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.minutes = None  # Can store meeting minutes as text
        self.decisions = []  # List of decision IDs
        self.tasks = []  # List of task IDs associated with this meeting

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date': self.date.isoformat() if self.date else None,
            'organizer': self.organizer,
            'attendees': self.attendees,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'minutes': self.minutes,
            'decisions_count': len(self.decisions),
            'tasks_count': len(self.tasks)
        }

# Decision model
class Decision:
    def __init__(self, id, title, description, meeting_id, made_by, date=None):
        self.id = id
        self.title = title
        self.description = description
        self.meeting_id = meeting_id
        self.made_by = made_by  # User ID
        self.date = date or datetime.now()
        self.created_at = datetime.now()
        self.tasks = []  # List of task IDs resulting from this decision

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'meeting_id': self.meeting_id,
            'made_by': self.made_by,
            'date': self.date.isoformat() if self.date else None,
            'created_at': self.created_at.isoformat(),
            'tasks_count': len(self.tasks)
        }

# Milestone model
class Milestone:
    def __init__(self, id, title, description, project_id, due_date, created_by, 
                 status=MilestoneStatus.PLANNED.value):
        self.id = id
        self.title = title
        self.description = description
        self.project_id = project_id
        self.due_date = due_date
        self.created_by = created_by
        self.status = status
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.tasks = []  # List of task IDs for this milestone
        self.comments = []  # List of comment IDs for this milestone
        self.completion_percentage = 0  # Milestone completion percentage
        
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'project_id': self.project_id,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_by': self.created_by,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'task_count': len(self.tasks),
            'completion_percentage': self.completion_percentage
        }

# Comment model
class CommentType(Enum):
    TASK = "task"
    PROJECT = "project"
    MILESTONE = "milestone"
    MEETING = "meeting"
    DECISION = "decision"

class Comment:
    def __init__(self, id, user_id, content, entity_type, entity_id, created_at=None):
        self.id = id
        self.user_id = user_id
        self.content = content
        self.entity_type = entity_type  # Task, Project, Milestone, etc.
        self.entity_id = entity_id      # ID of the related entity
        self.created_at = created_at or datetime.now()
        self.needs_notification = True  # Flag to indicate if notification needs to be sent

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content': self.content,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'created_at': self.created_at.isoformat()
        }

# Note model (for Post-it style notes)
class Note:
    def __init__(self, id, title, content, user_id, color=NoteColor.YELLOW.value, pinned=False):
        self.id = id
        self.title = title
        self.content = content
        self.user_id = user_id
        self.color = color
        self.pinned = pinned
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'user_id': self.user_id,
            'color': self.color,
            'pinned': self.pinned,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
