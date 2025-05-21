from flask import render_template, redirect, url_for, flash, request, session, jsonify
import datetime
import uuid
from app import app
from forms import (
    LoginForm, RegisterForm, TaskForm, ProjectForm, CommentForm, 
    MeetingForm, DecisionForm, MilestoneForm, NoteForm
)
import database
from models import ProjectStatus, MilestoneStatus, CommentType
from utils import (
    login_required, admin_required, get_current_user, 
    get_team_workload, get_project_progress, get_task_distribution,
    update_task_status, format_date
)

# Update task statuses before each request
@app.before_request
def before_request():
    update_task_status()

# Authentication routes - These handle user login and registration
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle user login functionality
    
    GET: Display login form
    POST: Process login attempt
    
    This route demonstrates Flask's handling of different HTTP methods
    within the same route function - it's a common pattern in web apps.
    """
    print("Current session:", session)  
    
   
    if 'user_id' in session:
        print("User already logged in, redirecting to dashboard")
        return redirect(url_for('dashboard'))
        
    
    form = LoginForm()
    
    
    if form.validate_on_submit():
        # Extract the username and password from the form
        username = form.username.data
        password = form.password.data
        
        print(f"Login attempt for username: {username}")  
        # Query the database for the user with this username
        user = database.get_user_by_username(username)
        
        
        if user and user.check_password(password):
            
            session.permanent = True
            
            # Store user information in the session
            # This is how we keep track of who is logged in
            session['user_id'] = user.id
            session['user_role'] = user.role  # For permission-based features
            
            print(f"Login successful for {username}, user_id: {user.id}, role: {user.role}")
            print("Updated session:", session)
            
            # Flash a success message to the user - will display on the next page
            flash('Login successful!', 'success')
            
            # Redirect to the dashboard page after successful login
            return redirect(url_for('dashboard'))
        else:
            # If login fails, log it and notify the user
            print(f"Login failed for {username}")
            flash('Invalid username or password!', 'danger')
    
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    print("Logout - Current session before clear:", session)
    session.clear()
    print("Logout - Session after clear:", session)
    flash('You have been logged out!', 'success')
    return redirect(url_for('login'))

@app.route("/register", methods=["GET", "POST"])
def register():
    print("Register - Current session:", session)
    
    if 'user_id' in session:
        print("User already logged in, redirecting to dashboard")
        return redirect(url_for('dashboard'))
        
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        name = form.name.data
        password = form.password.data
        
        print(f"Registration attempt for username: {username}, email: {email}")
        
        # Check if username or email already exists
        if database.get_user_by_username(username):
            print(f"Username {username} already exists")
            flash('Username already exists!', 'danger')
            return render_template('register.html', form=form)
            
        if database.get_user_by_email(email):
            print(f"Email {email} already exists")
            flash('Email already exists!', 'danger')
            return render_template('register.html', form=form)
            
        # Create user
        user_id = database.create_user(username, email, password, "member", name)
        print(f"User created with ID: {user_id}")
        
        # Auto-login the user after registration
        session.permanent = True
        session['user_id'] = user_id
        session['user_role'] = "member"
        print(f"User logged in with ID: {user_id}, Session: {session}")
        
        flash('Registration successful! You are now logged in.', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('register.html', form=form)

# Dashboard route
@app.route("/")
@login_required
def dashboard():
    print("Session:", session)
    user = get_current_user()
    print("User:", user)
    
    if not user:
        flash('User not found. Please login again.', 'danger')
        return redirect(url_for('login'))
    
    # Update task statuses before getting any tasks
    update_task_status()
    
    # Get user tasks
    user_tasks = database.get_tasks_by_user(user.id)
    
    # Get statistics
    pending_tasks = [task for task in user_tasks if task.status == 'pending']
    in_progress_tasks = [task for task in user_tasks if task.status == 'in_progress']
    completed_tasks = [task for task in user_tasks if task.status == 'done']
    overdue_tasks = [task for task in user_tasks if task.status == 'overdue']
    
    # Get all projects
    all_projects = database.get_all_projects()
    
    # For managers, show team workload
    team_workload = None
    if user.role == 'manager':
        team_workload = get_team_workload()
        
    # Get task distribution
    task_distribution = get_task_distribution()
    
    # Get all tasks for project progress
    all_tasks = database.get_all_tasks()
    
    # Create a dictionary of tasks by ID for easy lookup
    tasks_dict = {task.id: task for task in all_tasks}
    
    # Get recent meetings
    if user.role == 'manager':
        recent_meetings = database.get_all_meetings()
    else:
        recent_meetings = database.get_meetings_by_user(user.id)
    # Sort meetings by date (most recent first) and limit to 5
    recent_meetings = sorted(recent_meetings, key=lambda m: m.date if m.date else datetime.datetime.now(), reverse=True)[:5]
    
    # Get recent decisions
    all_decisions = database.get_all_decisions()
    if user.role != 'manager':
        # Filter decisions to only those made by the user or from meetings they attended
        user_meetings = database.get_meetings_by_user(user.id)
        user_meeting_ids = [meeting.id for meeting in user_meetings]
        all_decisions = [d for d in all_decisions if d.made_by == user.id or d.meeting_id in user_meeting_ids]
    
    recent_decisions = sorted(all_decisions, key=lambda d: d.date if d.date else datetime.datetime.now(), reverse=True)[:5]
    
    # Get upcoming milestones (next 30 days)
    upcoming_milestones = database.get_upcoming_milestones(30)
    # Sort milestones by due date (earliest first)
    upcoming_milestones = sorted(upcoming_milestones, key=lambda m: m.due_date if m.due_date else datetime.datetime.now())[:5]
    
    # Get user's pinned notes
    user_notes = database.get_notes_by_user(user.id)
    pinned_notes = [note for note in user_notes if note.pinned]

    context = {
        'user': user,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'all_projects': all_projects,
        'team_workload': team_workload,
        'task_distribution': task_distribution,
        'tasks': tasks_dict,
        'recent_meetings': recent_meetings,
        'recent_decisions': recent_decisions,
        'upcoming_milestones': upcoming_milestones,
        'pinned_notes': pinned_notes
    }
    
    return render_template('dashboard.html', **context)

# Task routes
@app.route("/tasks")
@login_required  
def tasks():
    """
    Display and filter all tasks
    
    This route demonstrates several key concepts:
    1. User role-based access control
    2. Query parameter handling for filtering
    3. List comprehension for filtering data
    4. Authorization-based data access
    """
    
    user = get_current_user()
    
  
    if not user:
        flash('User not found. Please login again.', 'danger')
        return redirect(url_for('login'))
    
   
    status = request.args.get('status')  
    category = request.args.get('category')  
    priority = request.args.get('priority')  
    project_id = request.args.get('project_id')  
    assigned_user_id = request.args.get('user_id')  
    
    
    # Get tasks based on user role
    if user.role == 'manager':
        all_tasks = database.get_all_tasks()  # Managers can see all tasks
    else:
        all_tasks = database.get_tasks_by_user(user.id)  # Regular users only see their tasks
    
   
    filtered_tasks = all_tasks
    
   
    if status:
      
        filtered_tasks = [task for task in filtered_tasks if task.status == status]
        
    # Filter by category if provided
    if category:
        filtered_tasks = [task for task in filtered_tasks if task.category == category]
        
    # Filter by priority if provided
    if priority:
        filtered_tasks = [task for task in filtered_tasks if task.priority == priority]
        
    if project_id:
        filtered_tasks = [task for task in filtered_tasks if task.project_id == project_id]
        
    if assigned_user_id:
        filtered_tasks = [task for task in filtered_tasks if task.assigned_to == assigned_user_id]
    
    # Get all projects for filter dropdown
    all_projects = database.get_all_projects()
    
    # Get all users for filter dropdown (managers only)
    all_users = []
    if user.role == 'manager':
        all_users = database.get_all_users()
    
    context = {
        'user': user,
        'tasks': filtered_tasks,
        'projects': all_projects,
        'users': all_users,
        'status': status,
        'category': category,
        'priority': priority,
        'project_id': project_id,
        'assigned_user_id': assigned_user_id
    }
    
    return render_template('tasks.html', **context)

@app.route("/tasks/create", methods=["GET", "POST"])
@login_required
def create_task():
    user = get_current_user()
    
    if not user:
        flash('User not found. Please login again.', 'danger')
        return redirect(url_for('login'))
    
    # Prepare form with dynamic choices
    form = TaskForm()
    
    # Get all users for assignment dropdown
    all_users = database.get_all_users()
    form.assigned_to.choices = [('', 'Unassigned')] + [(u.id, u.name) for u in all_users if u.role == 'member']
    
    # Get all projects for project dropdown
    all_projects = database.get_all_projects()
    form.project_id.choices = [('', 'None')] + [(p.id, p.name) for p in all_projects]
    
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        status = form.status.data
        priority = form.priority.data
        category = form.category.data
        due_date = form.due_date.data
        assigned_to = form.assigned_to.data or None
        project_id = form.project_id.data or None
        
        # Create task
        task_id = database.create_task(
            title, description, status, priority, category,
            due_date, user.id, assigned_to, project_id
        )
        
        flash('Task created successfully!', 'success')
        return redirect(url_for('tasks'))
    
    return render_template('task_detail.html', form=form, task=None, user=user)

@app.route("/tasks/<task_id>")
@login_required
def view_task(task_id):
    user = get_current_user()
    task = database.get_task(task_id)
    
    if not task:
        flash('Task not found!', 'danger')
        return redirect(url_for('tasks'))
    
    # Get task creator
    creator = database.get_user_by_id(task.created_by)
    
    # Get assigned user
    assigned_user = None
    if task.assigned_to:
        assigned_user = database.get_user_by_id(task.assigned_to)
    
    # Get project
    project = None
    if task.project_id:
        project = database.get_project(task.project_id)
    
    # Get comments
    task_comments = database.get_comments_by_task(task_id)
    
    # Prepare comment form
    comment_form = CommentForm()
    
    # Get all users for comment display
    all_users = database.get_all_users()
    
    context = {
        'user': user,
        'task': task,
        'creator': creator,
        'assigned_user': assigned_user,
        'project': project,
        'comments': task_comments,
        'comment_form': comment_form,
        'users': all_users
    }
    
    return render_template('task_detail.html', **context, view_only=True)

@app.route("/tasks/<task_id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    user = get_current_user()
    task = database.get_task(task_id)
    
    if not task:
        flash('Task not found!', 'danger')
        return redirect(url_for('tasks'))
    
    # Check if user has permission to edit
    if user.role != 'manager' and task.created_by != user.id and task.assigned_to != user.id:
        flash('You do not have permission to edit this task!', 'danger')
        return redirect(url_for('view_task', task_id=task_id))
    
    # Prepare form with dynamic choices
    form = TaskForm(obj=task)
    
    # Get all users for assignment dropdown
    all_users = database.get_all_users()
    form.assigned_to.choices = [('', 'Unassigned')] + [(u.id, u.name) for u in all_users if u.role == 'member']
    
    # Get all projects for project dropdown
    all_projects = database.get_all_projects()
    form.project_id.choices = [('', 'None')] + [(p.id, p.name) for p in all_projects]
    
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        status = form.status.data
        priority = form.priority.data
        category = form.category.data
        due_date = form.due_date.data
        assigned_to = form.assigned_to.data or None
        project_id = form.project_id.data or None
        
        # Update task
        database.update_task(
            task_id,
            title=title,
            description=description,
            status=status,
            priority=priority,
            category=category,
            due_date=due_date,
            assigned_to=assigned_to,
            project_id=project_id
        )
        
        flash('Task updated successfully!', 'success')
        return redirect(url_for('view_task', task_id=task_id))
    
    # Pre-populate form
    if request.method == 'GET':
        form.title.data = task.title
        form.description.data = task.description
        form.status.data = task.status
        form.priority.data = task.priority
        form.category.data = task.category
        form.due_date.data = task.due_date
        form.assigned_to.data = task.assigned_to
        form.project_id.data = task.project_id
    
    return render_template('task_detail.html', form=form, task=task, user=user)

@app.route("/tasks/<task_id>/delete", methods=["POST"])
@login_required
def delete_task(task_id):
    user = get_current_user()
    task = database.get_task(task_id)
    
    if not task:
        flash('Task not found!', 'danger')
        return redirect(url_for('tasks'))
    
    # Check if user has permission to delete
    if user.role != 'manager' and task.created_by != user.id:
        flash('You do not have permission to delete this task!', 'danger')
        return redirect(url_for('view_task', task_id=task_id))
    
    # Delete task
    database.delete_task(task_id)
    
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('tasks'))

@app.route("/tasks/comment", methods=["POST"])
@login_required
def add_comment():
    user = get_current_user()
    form = CommentForm()
    
    if form.validate_on_submit():
        content = form.content.data
        entity_type = form.entity_type.data
        entity_id = form.entity_id.data
        
        # Check entity exists based on type
        entity_exists = False
        redirect_url = url_for('dashboard')
        
        if entity_type == CommentType.TASK.value:
            entity = database.get_task(entity_id)
            if entity:
                entity_exists = True
                redirect_url = url_for('view_task', task_id=entity_id)
        elif entity_type == CommentType.PROJECT.value:
            entity = database.get_project(entity_id)
            if entity:
                entity_exists = True
                redirect_url = url_for('view_project', project_id=entity_id)
        elif entity_type == CommentType.MILESTONE.value:
            entity = database.get_milestone(entity_id)
            if entity:
                entity_exists = True
                redirect_url = url_for('view_milestone', milestone_id=entity_id)
        elif entity_type == CommentType.MEETING.value:
            entity = database.get_meeting(entity_id)
            if entity:
                entity_exists = True
                redirect_url = url_for('view_meeting', meeting_id=entity_id)
        elif entity_type == CommentType.DECISION.value:
            entity = database.get_decision(entity_id)
            if entity:
                entity_exists = True
                redirect_url = url_for('view_decision', decision_id=entity_id)
        
        if not entity_exists:
            flash('Entity not found!', 'danger')
            return redirect(url_for('dashboard'))
        
        # Create comment
        database.create_comment(user.id, content, entity_type, entity_id)
        
        flash('Comment added successfully!', 'success')
        return redirect(redirect_url)
    
    flash('Error adding comment!', 'danger')
    return redirect(url_for('dashboard'))

# Project routes
@app.route("/projects")
@login_required
def projects():
    user = get_current_user()
    
    # Get all projects
    all_projects = database.get_all_projects()
    
    # Calculate progress for each project
    project_progress = {}
    for project in all_projects:
        progress = get_project_progress(project.id)
        project_progress[project.id] = progress
    
    context = {
        'user': user,
        'projects': all_projects,
        'project_progress': project_progress,
        'get_user_by_id': database.get_user_by_id
    }
    
    return render_template('projects.html', **context)

@app.route("/projects/create", methods=["GET", "POST"])
@login_required
def create_project():
    user = get_current_user()
    
    # Only managers can create projects
    if user.role != 'manager':
        flash('Only managers can create projects!', 'danger')
        return redirect(url_for('projects'))
    
    form = ProjectForm()
    
    # Get all users for team members multiselect
    all_users = database.get_all_users()
    form.team_members.choices = [(u.id, u.name) for u in all_users if u.role == 'member']
    
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        status = form.status.data
        team_members = form.team_members.data
        
        # Create project
        project_id = database.create_project(
            name, 
            description, 
            start_date, 
            end_date, 
            user.id,
            status,
            team_members
        )
        
        flash('Project created successfully!', 'success')
        return redirect(url_for('projects'))
    
    # Add current date for timeline calculation
    from datetime import datetime
    now = datetime.now()
    
    return render_template('project_detail.html', form=form, project=None, user=user, now=now)

@app.route("/projects/<project_id>")
@login_required
def view_project(project_id):
    user = get_current_user()
    project = database.get_project(project_id)
    
    if not project:
        flash('Project not found!', 'danger')
        return redirect(url_for('projects'))
    
    # Get project progress
    progress = get_project_progress(project_id)
    
    # Get tasks for this project
    project_tasks = database.get_tasks_by_project(project_id)
    
    # Get comments for this project
    project_comments = database.get_comments_by_project(project_id)
    
    # Prepare comment form
    comment_form = CommentForm()
    
    # Get all users for comment display
    all_users = database.get_all_users()
    
    # Add current date for timeline calculation
    from datetime import datetime
    now = datetime.now()
    
    context = {
        'user': user,
        'project': project,
        'progress': progress,
        'tasks': project_tasks,
        'comments': project_comments,
        'comment_form': comment_form,
        'users': all_users,
        'get_user_by_id': database.get_user_by_id,
        'now': now
    }
    
    return render_template('project_detail.html', **context, view_only=True)

@app.route("/projects/<project_id>/edit", methods=["GET", "POST"])
@login_required
def edit_project(project_id):
    user = get_current_user()
    project = database.get_project(project_id)
    
    if not project:
        flash('Project not found!', 'danger')
        return redirect(url_for('projects'))
    
    # Only managers can edit projects
    if user.role != 'manager':
        flash('Only managers can edit projects!', 'danger')
        return redirect(url_for('view_project', project_id=project_id))
    
    form = ProjectForm(obj=project)
    
    # Get all users for team members multiselect
    all_users = database.get_all_users()
    form.team_members.choices = [(u.id, u.name) for u in all_users if u.role == 'member']
    
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        status = form.status.data
        team_members = form.team_members.data
        
        # Update project
        database.update_project(
            project_id,
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            status=status,
            team_members=team_members
        )
        
        flash('Project updated successfully!', 'success')
        return redirect(url_for('view_project', project_id=project_id))
    
    # Pre-populate form
    if request.method == 'GET':
        form.name.data = project.name
        form.description.data = project.description
        form.start_date.data = project.start_date
        form.end_date.data = project.end_date
        form.status.data = project.status
        form.team_members.data = project.team_members
    
    # Add current date for timeline calculation
    from datetime import datetime
    now = datetime.now()
    
    return render_template('project_detail.html', form=form, project=project, user=user, now=now)

@app.route("/projects/<project_id>/delete", methods=["POST"])
@login_required
def delete_project(project_id):
    user = get_current_user()
    project = database.get_project(project_id)
    
    if not project:
        flash('Project not found!', 'danger')
        return redirect(url_for('projects'))
    
    # Only managers can delete projects
    if user.role != 'manager':
        flash('Only managers can delete projects!', 'danger')
        return redirect(url_for('view_project', project_id=project_id))
    
    # Delete project
    database.delete_project(project_id)
    
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('projects'))

# Team routes
@app.route("/team")
@login_required
def team():
    user = get_current_user()
    
    # Get all team members
    all_users = database.get_all_users()
    team_members = [u for u in all_users if u.role == 'member']
    
    # Get workload for each team member
    workload = get_team_workload()
    
    context = {
        'user': user,
        'team_members': team_members,
        'workload': workload
    }
    
    return render_template('team.html', **context)

@app.route("/team/member/<user_id>")
@login_required
def team_member(user_id):
    current_user = get_current_user()
    team_member = database.get_user_by_id(user_id)
    
    if not team_member:
        flash('Team member not found!', 'danger')
        return redirect(url_for('team'))
    
    # Get tasks for this team member
    member_tasks = database.get_tasks_by_user(user_id)
    
    # Calculate statistics
    task_counts = {
        'pending': sum(1 for task in member_tasks if task.status == 'pending'),
        'in_progress': sum(1 for task in member_tasks if task.status == 'in_progress'),
        'done': sum(1 for task in member_tasks if task.status == 'done'),
        'overdue': sum(1 for task in member_tasks if task.status == 'overdue'),
        'total': len(member_tasks)
    }
    
    # Calculate completion rate
    completion_rate = 0
    if task_counts['total'] > 0:
        completion_rate = (task_counts['done'] / task_counts['total']) * 100
    
    context = {
        'user': current_user,
        'team_member': team_member,
        'tasks': member_tasks,
        'task_counts': task_counts,
        'completion_rate': completion_rate
    }
    
    return render_template('team_member.html', **context)

# Calendar route
@app.route("/calendar")
@login_required
def calendar():
    user = get_current_user()
    
    # Get all tasks with due dates
    if user.role == 'manager':
        all_tasks = database.get_all_tasks()
    else:
        all_tasks = database.get_tasks_by_user(user.id)
    
    tasks_with_dates = [task for task in all_tasks if task.due_date]
    
    # Convert tasks to calendar events
    events = []
    for task in tasks_with_dates:
        # Determine color based on status
        color = '#3498db'  # Default blue
        if task.status == 'done':
            color = '#2ecc71'  # Green
        elif task.status == 'overdue':
            color = '#e74c3c'  # Red
        elif task.priority == 'high' or task.priority == 'critical':
            color = '#f39c12'  # Orange
        
        events.append({
            'id': task.id,
            'title': task.title,
            'start': format_date(task.due_date),
            'color': color,
            'extendedProps': {
                'status': task.status,
                'priority': task.priority,
                'category': task.category
            }
        })
    
    context = {
        'user': user,
        'events': events
    }
    
    return render_template('calendar.html', **context)

# Reports route
@app.route("/reports")
@login_required
def reports():
    user = get_current_user()
    
    # Only managers can view reports
    if user.role != 'manager':
        flash('Only managers can view reports!', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get task distribution data
    task_distribution = get_task_distribution()
    
    # Get team workload data
    team_workload = get_team_workload()
    
    # Get project progress data
    all_projects = database.get_all_projects()
    project_progress = {}
    for project in all_projects:
        progress = get_project_progress(project.id)
        project_progress[project.id] = progress
    
    context = {
        'user': user,
        'task_distribution': task_distribution,
        'team_workload': team_workload,
        'projects': all_projects,
        'project_progress': project_progress
    }
    
    return render_template('reports.html', **context)

# Milestone routes
@app.route("/milestones")
@login_required
def milestones():
    user = get_current_user()
    
    # Get filter parameters
    project_id = request.args.get('project_id')
    status = request.args.get('status')
    timeframe = request.args.get('timeframe', 'all')
    
    # Get all milestones
    all_milestones = database.get_all_milestones()
    
    # Apply filters
    filtered_milestones = all_milestones
    
    if project_id:
        filtered_milestones = [m for m in filtered_milestones if m.project_id == project_id]
        
    if status:
        filtered_milestones = [m for m in filtered_milestones if m.status == status]
        
    if timeframe:
        today = datetime.datetime.now().date()
        if timeframe == 'week':
            # Next 7 days
            end_date = today + datetime.timedelta(days=7)
            filtered_milestones = [m for m in filtered_milestones if m.due_date and m.due_date >= today and m.due_date <= end_date]
        elif timeframe == 'month':
            # Next 30 days
            end_date = today + datetime.timedelta(days=30)
            filtered_milestones = [m for m in filtered_milestones if m.due_date and m.due_date >= today and m.due_date <= end_date]
    
    # Get all projects for filter dropdown
    all_projects = database.get_all_projects()
    
    context = {
        'user': user,
        'milestones': filtered_milestones,
        'projects': all_projects,
        'project_id': project_id,
        'status': status,
        'timeframe': timeframe
    }
    
    return render_template('milestones.html', **context)

@app.route("/milestones/create", methods=["GET", "POST"])
@login_required
def create_milestone():
    user = get_current_user()
    
    # Only managers can create milestones
    if user.role != 'manager':
        flash('Only managers can create milestones!', 'danger')
        return redirect(url_for('milestones'))
    
    form = MilestoneForm()
    
    # Get all projects for the project dropdown
    all_projects = database.get_all_projects()
    form.project_id.choices = [(p.id, p.name) for p in all_projects]
    
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        project_id = form.project_id.data
        due_date = form.due_date.data
        status = form.status.data
        
        # Create milestone
        milestone_id = database.create_milestone(
            title,
            description,
            project_id,
            due_date,
            user.id,
            status
        )
        
        flash('Milestone created successfully!', 'success')
        return redirect(url_for('milestones'))
    
    return render_template('milestone_detail.html', form=form, milestone=None, user=user)

@app.route("/milestones/<milestone_id>")
@login_required
def view_milestone(milestone_id):
    user = get_current_user()
    milestone = database.get_milestone(milestone_id)
    
    if not milestone:
        flash('Milestone not found!', 'danger')
        return redirect(url_for('milestones'))
    
    # Get project
    project = None
    if milestone.project_id:
        project = database.get_project(milestone.project_id)
    
    # Get comments for this milestone
    milestone_comments = database.get_comments_by_milestone(milestone_id)
    
    # Prepare comment form
    comment_form = CommentForm()
    
    # Get all users for comment display
    all_users = database.get_all_users()
    
    context = {
        'user': user,
        'milestone': milestone,
        'project': project,
        'comments': milestone_comments,
        'comment_form': comment_form,
        'users': all_users
    }
    
    return render_template('milestone_detail.html', **context, view_only=True)

@app.route("/milestones/<milestone_id>/edit", methods=["GET", "POST"])
@login_required
def edit_milestone(milestone_id):
    user = get_current_user()
    milestone = database.get_milestone(milestone_id)
    
    if not milestone:
        flash('Milestone not found!', 'danger')
        return redirect(url_for('milestones'))
    
    # Only managers can edit milestones
    if user.role != 'manager':
        flash('Only managers can edit milestones!', 'danger')
        return redirect(url_for('view_milestone', milestone_id=milestone_id))
    
    form = MilestoneForm(obj=milestone)
    
    # Get all projects for the project dropdown
    all_projects = database.get_all_projects()
    form.project_id.choices = [(p.id, p.name) for p in all_projects]
    
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        project_id = form.project_id.data
        due_date = form.due_date.data
        status = form.status.data
        
        # Update milestone
        database.update_milestone(
            milestone_id,
            title=title,
            description=description,
            project_id=project_id,
            due_date=due_date,
            status=status
        )
        
        flash('Milestone updated successfully!', 'success')
        return redirect(url_for('view_milestone', milestone_id=milestone_id))
    
    # Pre-populate form
    if request.method == 'GET':
        form.title.data = milestone.title
        form.description.data = milestone.description
        form.project_id.data = milestone.project_id
        form.due_date.data = milestone.due_date
        form.status.data = milestone.status
    
    return render_template('milestone_detail.html', form=form, milestone=milestone, user=user)

@app.route("/milestones/<milestone_id>/delete", methods=["POST"])
@login_required
def delete_milestone(milestone_id):
    user = get_current_user()
    milestone = database.get_milestone(milestone_id)
    
    if not milestone:
        flash('Milestone not found!', 'danger')
        return redirect(url_for('milestones'))
    
    # Only managers can delete milestones
    if user.role != 'manager':
        flash('Only managers can delete milestones!', 'danger')
        return redirect(url_for('view_milestone', milestone_id=milestone_id))
    
    # Delete milestone
    database.delete_milestone(milestone_id)
    
    flash('Milestone deleted successfully!', 'success')
    return redirect(url_for('milestones'))

# API routes for AJAX calls
@app.route("/api/tasks")
@login_required
def api_tasks():
    user = get_current_user()
    
    # Get all tasks
    if user.role == 'manager':
        all_tasks = database.get_all_tasks()
    else:
        all_tasks = database.get_tasks_by_user(user.id)
    
    # Convert to dictionaries
    tasks_data = [task.to_dict() for task in all_tasks]
    
    return jsonify(tasks_data)

@app.route("/api/team/workload")
@login_required
def api_team_workload():
    user = get_current_user()
    
    # Only managers can access this API
    if user.role != 'manager':
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get team workload data
    workload = get_team_workload()
    
    # Format data for chart
    chart_data = {
        'labels': [member['user'].name for member in workload],
        'datasets': [
            {
                'label': 'Pending',
                'data': [member['task_counts']['pending'] for member in workload],
                'backgroundColor': '#f39c12'
            },
            {
                'label': 'In Progress',
                'data': [member['task_counts']['in_progress'] for member in workload],
                'backgroundColor': '#3498db'
            },
            {
                'label': 'Done',
                'data': [member['task_counts']['done'] for member in workload],
                'backgroundColor': '#2ecc71'
            },
            {
                'label': 'Overdue',
                'data': [member['task_counts']['overdue'] for member in workload],
                'backgroundColor': '#e74c3c'
            }
        ]
    }
    
    return jsonify(chart_data)

@app.route("/api/task/distribution")
@login_required
def api_task_distribution():
    # Get task distribution data
    distribution = get_task_distribution()
    
    # Format data for charts
    category_data = {
        'labels': list(distribution['category'].keys()),
        'datasets': [{
            'data': list(distribution['category'].values()),
            'backgroundColor': [
                '#3498db', '#2ecc71', '#9b59b6', '#e74c3c', '#34495e'
            ]
        }]
    }
    
    priority_data = {
        'labels': list(distribution['priority'].keys()),
        'datasets': [{
            'data': list(distribution['priority'].values()),
            'backgroundColor': [
                '#3498db', '#f39c12', '#e74c3c', '#c0392b'
            ]
        }]
    }
    
    return jsonify({
        'category': category_data,
        'priority': priority_data
    })

# Meeting routes
@app.route("/meetings")
@login_required
def meetings():
    user = get_current_user()
    
    if user.role == 'manager':
        # Managers can see all meetings
        all_meetings = database.get_all_meetings()
    else:
        # Regular users only see meetings they're organizing or attending
        all_meetings = database.get_meetings_by_user(user.id)
    
    context = {
        'user': user,
        'meetings': all_meetings,
        'get_user_by_id': database.get_user_by_id
    }
    
    return render_template('meetings.html', **context)

@app.route("/meetings/create", methods=["GET", "POST"])
@login_required
def create_meeting():
    user = get_current_user()
    form = MeetingForm()
    
    # Get all users for attendees
    all_users = database.get_all_users()
    form.attendees.choices = [(u.id, u.name) for u in all_users]
    
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        date = form.date.data
        attendees = form.attendees.data
        minutes = form.minutes.data
        
        # Create meeting
        meeting_id = database.create_meeting(title, description, date, user.id, attendees)
        
        # Add minutes if provided
        if minutes:
            database.update_meeting(meeting_id, minutes=minutes)
        
        flash('Meeting created successfully!', 'success')
        return redirect(url_for('meetings'))
    
    return render_template('meeting_detail.html', form=form, meeting=None, user=user)

@app.route("/meetings/<meeting_id>")
@login_required
def view_meeting(meeting_id):
    user = get_current_user()
    meeting = database.get_meeting(meeting_id)
    
    if not meeting:
        flash('Meeting not found!', 'danger')
        return redirect(url_for('meetings'))
    
    # Get organizer
    organizer = database.get_user_by_id(meeting.organizer)
    
    # Get attendees
    attendees = []
    for attendee_id in meeting.attendees:
        attendee = database.get_user_by_id(attendee_id)
        if attendee:
            attendees.append(attendee)
    
    # Get tasks associated with this meeting
    meeting_tasks = []
    for task_id in meeting.tasks:
        task = database.get_task(task_id)
        if task:
            meeting_tasks.append(task)
    
    # Get decisions made in this meeting
    meeting_decisions = []
    for decision_id in meeting.decisions:
        decision = database.get_decision(decision_id)
        if decision:
            meeting_decisions.append(decision)
    
    # Get comments for this meeting
    meeting_comments = database.get_comments_by_entity(CommentType.MEETING.value, meeting_id)
    
    # Prepare comment form
    comment_form = CommentForm()
    
    # Get all users for comment display
    all_users = database.get_all_users()
    
    context = {
        'user': user,
        'meeting': meeting,
        'organizer': organizer,
        'attendees': attendees,
        'tasks': meeting_tasks,
        'decisions': meeting_decisions,
        'comments': meeting_comments,
        'comment_form': comment_form,
        'users': all_users
    }
    
    return render_template('meeting_detail.html', **context, view_only=True)

@app.route("/meetings/<meeting_id>/edit", methods=["GET", "POST"])
@login_required
def edit_meeting(meeting_id):
    user = get_current_user()
    meeting = database.get_meeting(meeting_id)
    
    if not meeting:
        flash('Meeting not found!', 'danger')
        return redirect(url_for('meetings'))
    
    # Check if user has permission to edit
    if user.role != 'manager' and meeting.organizer != user.id:
        flash('You do not have permission to edit this meeting!', 'danger')
        return redirect(url_for('view_meeting', meeting_id=meeting_id))
    
    form = MeetingForm(obj=meeting)
    
    # Get all users for attendees
    all_users = database.get_all_users()
    form.attendees.choices = [(u.id, u.name) for u in all_users]
    
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        date = form.date.data
        attendees = form.attendees.data
        minutes = form.minutes.data
        
        # Update meeting
        database.update_meeting(
            meeting_id,
            title=title,
            description=description,
            date=date,
            attendees=attendees,
            minutes=minutes
        )
        
        flash('Meeting updated successfully!', 'success')
        return redirect(url_for('view_meeting', meeting_id=meeting_id))
    
    # Pre-populate form
    if request.method == 'GET':
        form.title.data = meeting.title
        form.description.data = meeting.description
        form.date.data = meeting.date
        form.attendees.data = meeting.attendees
        form.minutes.data = meeting.minutes
    
    return render_template('meeting_detail.html', form=form, meeting=meeting, user=user)

@app.route("/meetings/<meeting_id>/delete", methods=["POST"])
@login_required
def delete_meeting(meeting_id):
    user = get_current_user()
    meeting = database.get_meeting(meeting_id)
    
    if not meeting:
        flash('Meeting not found!', 'danger')
        return redirect(url_for('meetings'))
    
    # Check if user has permission to delete
    if user.role != 'manager' and meeting.organizer != user.id:
        flash('You do not have permission to delete this meeting!', 'danger')
        return redirect(url_for('view_meeting', meeting_id=meeting_id))
    
    # Delete meeting
    database.delete_meeting(meeting_id)
    
    flash('Meeting deleted successfully!', 'success')
    return redirect(url_for('meetings'))

# Decision routes
@app.route("/decisions")
@login_required
def decisions():
    user = get_current_user()
    
    # Get all decisions
    all_decisions = database.get_all_decisions()
    
    # Filter decisions based on user role
    if user.role != 'manager':
        # Regular users only see decisions they made or from meetings they attended
        user_meetings = database.get_meetings_by_user(user.id)
        user_meeting_ids = [meeting.id for meeting in user_meetings]
        all_decisions = [d for d in all_decisions if d.made_by == user.id or d.meeting_id in user_meeting_ids]
    
    context = {
        'user': user,
        'decisions': all_decisions,
        'get_user_by_id': database.get_user_by_id,
        'get_meeting': database.get_meeting
    }
    
    return render_template('decisions.html', **context)

@app.route("/decisions/create", methods=["GET", "POST"])
@login_required
def create_decision():
    user = get_current_user()
    form = DecisionForm()
    
    # Get all meetings for meeting dropdown
    all_meetings = database.get_all_meetings()
    form.meeting_id.choices = [('', 'None')] + [(m.id, m.title) for m in all_meetings]
    
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        meeting_id = form.meeting_id.data or None
        date = form.date.data or datetime.datetime.now()
        
        # Create decision
        decision_id = database.create_decision(title, description, meeting_id, user.id, date)
        
        flash('Decision created successfully!', 'success')
        return redirect(url_for('decisions'))
    
    return render_template('decision_detail.html', form=form, decision=None, user=user)

@app.route("/decisions/<decision_id>")
@login_required
def view_decision(decision_id):
    user = get_current_user()
    decision = database.get_decision(decision_id)
    
    if not decision:
        flash('Decision not found!', 'danger')
        return redirect(url_for('decisions'))
    
    # Get decision maker
    made_by = database.get_user_by_id(decision.made_by)
    
    # Get associated meeting
    meeting = None
    if decision.meeting_id:
        meeting = database.get_meeting(decision.meeting_id)
    
    # Get tasks resulting from this decision
    decision_tasks = []
    for task_id in decision.tasks:
        task = database.get_task(task_id)
        if task:
            decision_tasks.append(task)
    
    # Get comments for this decision
    decision_comments = database.get_comments_by_entity(CommentType.DECISION.value, decision_id)
    
    # Prepare comment form
    comment_form = CommentForm()
    
    # Get all users for comment display
    all_users = database.get_all_users()
    
    context = {
        'user': user,
        'decision': decision,
        'made_by': made_by,
        'meeting': meeting,
        'tasks': decision_tasks,
        'comments': decision_comments,
        'comment_form': comment_form,
        'users': all_users
    }
    
    return render_template('decision_detail.html', **context, view_only=True)

@app.route("/decisions/<decision_id>/edit", methods=["GET", "POST"])
@login_required
def edit_decision(decision_id):
    user = get_current_user()
    decision = database.get_decision(decision_id)
    
    if not decision:
        flash('Decision not found!', 'danger')
        return redirect(url_for('decisions'))
    
    # Check if user has permission to edit
    if user.role != 'manager' and decision.made_by != user.id:
        flash('You do not have permission to edit this decision!', 'danger')
        return redirect(url_for('view_decision', decision_id=decision_id))
    
    form = DecisionForm(obj=decision)
    
    # Get all meetings for meeting dropdown
    all_meetings = database.get_all_meetings()
    form.meeting_id.choices = [('', 'None')] + [(m.id, m.title) for m in all_meetings]
    
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        meeting_id = form.meeting_id.data or None
        date = form.date.data
        
        # Update decision
        database.update_decision(
            decision_id,
            title=title,
            description=description,
            meeting_id=meeting_id,
            date=date
        )
        
        flash('Decision updated successfully!', 'success')
        return redirect(url_for('view_decision', decision_id=decision_id))
    
    # Pre-populate form
    if request.method == 'GET':
        form.title.data = decision.title
        form.description.data = decision.description
        form.meeting_id.data = decision.meeting_id
        form.date.data = decision.date
    
    return render_template('decision_detail.html', form=form, decision=decision, user=user)

@app.route("/decisions/<decision_id>/delete", methods=["POST"])
@login_required
def delete_decision(decision_id):
    user = get_current_user()
    decision = database.get_decision(decision_id)
    
    if not decision:
        flash('Decision not found!', 'danger')
        return redirect(url_for('decisions'))
    
    # Check if user has permission to delete
    if user.role != 'manager' and decision.made_by != user.id:
        flash('You do not have permission to delete this decision!', 'danger')
        return redirect(url_for('view_decision', decision_id=decision_id))
    
    # Delete decision
    database.delete_decision(decision_id)
    
    flash('Decision deleted successfully!', 'success')
    return redirect(url_for('decisions'))

# Note routes
@app.route("/notes")
@login_required
def notes():
    user = get_current_user()
    
    if not user:
        flash('User not found. Please login again.', 'danger')
        return redirect(url_for('login'))
    
    # Get all notes for the user
    user_notes = database.get_notes_by_user(user.id)
    
    # Sort notes with pinned first, then by date (newest first)
    user_notes = sorted(user_notes, key=lambda n: (not n.pinned, n.created_at), reverse=True)
    
    # Create new note form
    form = NoteForm()
    
    context = {
        'user': user,
        'notes': user_notes,
        'form': form
    }
    
    return render_template('notes.html', **context)

@app.route("/notes/create", methods=["POST"])
@login_required
def create_note():
    user = get_current_user()
    
    if not user:
        flash('User not found. Please login again.', 'danger')
        return redirect(url_for('login'))
    
    form = NoteForm()
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        color = form.color.data
        pinned = form.pinned.data
        
        # Create note
        database.create_note(title, content, user.id, color, pinned)
        
        flash('Note created successfully!', 'success')
    else:
        flash('Error creating note!', 'danger')
    
    return redirect(url_for('notes'))

@app.route("/notes/update", methods=["POST"])
@login_required
def update_note():
    user = get_current_user()
    
    if not user:
        flash('User not found. Please login again.', 'danger')
        return redirect(url_for('login'))
    
    form = NoteForm()
    
    if form.validate_on_submit():
        note_id = request.form.get('note_id')
        title = form.title.data
        content = form.content.data
        color = form.color.data
        pinned = form.pinned.data
        
        # Get the note
        note = database.get_note(note_id)
        
        # Check if note exists and belongs to the user
        if not note or note.user_id != user.id:
            flash('Note not found or you do not have permission to edit it!', 'danger')
            return redirect(url_for('notes'))
        
        # Update note
        database.update_note(
            note_id,
            title=title,
            content=content,
            color=color,
            pinned=pinned
        )
        
        flash('Note updated successfully!', 'success')
    else:
        flash('Error updating note!', 'danger')
    
    return redirect(url_for('notes'))

@app.route("/notes/delete", methods=["POST"])
@login_required
def delete_note():
    user = get_current_user()
    
    if not user:
        flash('User not found. Please login again.', 'danger')
        return redirect(url_for('login'))
    
    note_id = request.form.get('note_id')
    
    # Get the note
    note = database.get_note(note_id)
    
    # Check if note exists and belongs to the user
    if not note or note.user_id != user.id:
        flash('Note not found or you do not have permission to delete it!', 'danger')
        return redirect(url_for('notes'))
    
    # Delete note
    database.delete_note(note_id)
    
    flash('Note deleted successfully!', 'success')
    return redirect(url_for('notes'))

@app.route("/toggle_note_pin/<note_id>", methods=["POST"])
@login_required
def toggle_note_pin(note_id):
    user = get_current_user()
    
    if not user:
        return jsonify({'success': False, 'message': 'User not authenticated'})
    
    # Get the note
    note = database.get_note(note_id)
    
    # Check if note exists and belongs to the user
    if not note or note.user_id != user.id:
        return jsonify({'success': False, 'message': 'Note not found or permission denied'})
    
    # Toggle pin status
    new_pin_status = not note.pinned
    
    # Update note
    database.update_note(note_id, pinned=new_pin_status)
    
    return jsonify({'success': True, 'pinned': new_pin_status})
