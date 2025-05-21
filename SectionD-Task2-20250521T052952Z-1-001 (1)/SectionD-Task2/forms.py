from flask_wtf import FlaskForm  
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DateField, HiddenField, SelectMultipleField, BooleanField  # Form field types
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional  # Validation rules


from models import (
    TaskStatus, TaskPriority, TaskCategory,
    ProjectStatus, MilestoneStatus, NoteColor
)



class LoginForm(FlaskForm):
    """
    Login form for user authentication
    
    This form is used on the login page and validates user credentials.
    It contains just two fields - username and password.
    
    When submitted, this data is checked against the user database in routes.py.
    """
    username = StringField('Username', validators=[DataRequired()])  # Text field for username input
    password = PasswordField('Password', validators=[DataRequired()])  # Password field that masks input

class RegisterForm(FlaskForm):
    """
    Registration form for new user accounts
    
    This form collects all necessary information to create a new user account.
    It includes validation to ensure data integrity and security:
    - Username must be 3-20 characters
    - Email must be valid format
    - Password must be at least 6 characters
    - Password confirmation must match
    """
    username = StringField('Username', validators=[
        DataRequired(),  # Field cannot be empty
        Length(min=3, max=20)  # Username must be between 3-20 characters
    ])
    email = StringField('Email', validators=[
        DataRequired(),  # Field cannot be empty
        Email()  # Must be a valid email format (user@domain.com)
    ])
    name = StringField('Full Name', validators=[
        DataRequired(),  # Field cannot be empty
        Length(max=100)  # Prevent extremely long names
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),  # Field cannot be empty
        Length(min=6)  # Password must be at least 6 characters for security
    ])
    confirm_password = PasswordField(
        'Confirm Password', 
        validators=[
            DataRequired(),  # Field cannot be empty
            EqualTo('password', message='Passwords must match')  # Must match password field
        ]
    )

class TaskForm(FlaskForm):
    """
    Form for creating and editing tasks
    
    This form contains all fields needed for task management.
    It uses SelectField for dropdowns that have predefined options.
    This ensures data consistency and prevents invalid values.
    
    Note how we use the enum values from our models module to
    populate the choices for dropdown fields.
    """
    title = StringField('Title', validators=[
        DataRequired(), 
        Length(max=100)   
    ])
    description = TextAreaField('Description', validators=[
        DataRequired()   
    ])
    status = SelectField('Status', choices=[
       
     
        (TaskStatus.PENDING.value, 'Pending'), 
        (TaskStatus.IN_PROGRESS.value, 'In Progress'),  
        (TaskStatus.DONE.value, 'Done'),  
        (TaskStatus.OVERDUE.value, 'Overdue')  
    ])
    priority = SelectField('Priority', choices=[
        (TaskPriority.LOW.value, 'Low'),
        (TaskPriority.MEDIUM.value, 'Medium'),
        (TaskPriority.HIGH.value, 'High'),
        (TaskPriority.CRITICAL.value, 'Critical')
    ])
    category = SelectField('Category', choices=[
        (TaskCategory.PROJECT.value, 'Project'),
        (TaskCategory.BAU.value, 'Business As Usual'),
        (TaskCategory.MEETING_PREP.value, 'Meeting Preparation'),
        (TaskCategory.MEETING_ACTION.value, 'Meeting Action Item'),
        (TaskCategory.MEETING_MINUTES.value, 'Meeting Minutes'),
        (TaskCategory.DECISION_LOG.value, 'Decision Log'),
        (TaskCategory.INCIDENT.value, 'Incident'),
        (TaskCategory.OTHER.value, 'Other')
    ])
    due_date = DateField('Due Date', validators=[Optional()])
    assigned_to = SelectField('Assign To', validators=[Optional()])
    project_id = SelectField('Project', validators=[Optional()], choices=[('', 'None')])

class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[Optional()])
    end_date = DateField('End Date', validators=[Optional()])
    status = SelectField('Status', choices=[
        (ProjectStatus.PLANNED.value, 'Planned'),
        (ProjectStatus.ACTIVE.value, 'Active'),
        (ProjectStatus.ON_HOLD.value, 'On Hold'),
        (ProjectStatus.COMPLETED.value, 'Completed'),
        (ProjectStatus.CANCELLED.value, 'Cancelled')
    ])
    team_members = SelectMultipleField('Team Members', validators=[Optional()])

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    entity_type = HiddenField('Entity Type', validators=[DataRequired()])
    entity_id = HiddenField('Entity ID', validators=[DataRequired()])

class MeetingForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    attendees = SelectMultipleField('Attendees', validators=[Optional()])
    minutes = TextAreaField('Meeting Minutes', validators=[Optional()])

class DecisionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    meeting_id = SelectField('Meeting', validators=[Optional()], choices=[('', 'None')])
    date = DateField('Decision Date', validators=[Optional()])
    
class MilestoneForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    project_id = SelectField('Project', validators=[DataRequired()])
    due_date = DateField('Due Date', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        (MilestoneStatus.PLANNED.value, 'Planned'),
        (MilestoneStatus.IN_PROGRESS.value, 'In Progress'),
        (MilestoneStatus.COMPLETED.value, 'Completed'),
        (MilestoneStatus.DELAYED.value, 'Delayed'),
        (MilestoneStatus.CANCELLED.value, 'Cancelled')
    ])
    
class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    color = SelectField('Color', choices=[
        (NoteColor.YELLOW.value, 'Yellow'),
        (NoteColor.BLUE.value, 'Blue'),
        (NoteColor.GREEN.value, 'Green'),
        (NoteColor.PINK.value, 'Pink'),
        (NoteColor.ORANGE.value, 'Orange')
    ])
    pinned = BooleanField('Pin to Dashboard')
