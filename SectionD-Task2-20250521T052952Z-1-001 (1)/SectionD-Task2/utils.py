from datetime import datetime  
import uuid  
from flask import session, redirect, url_for  
from functools import wraps  
import database  

def generate_id():
    """
    Generate a unique ID using UUID4
    
    Returns:
        str: A string representation of a UUID4, which is random and practically unique
        
    Note:
        - UUID4 generates random IDs with extremely low collision probability
        - We use this for all entity IDs in our system (users, tasks, projects, etc.)
        - Using UUIDs avoids the need for sequential IDs or complex ID generation logic
    """
    return str(uuid.uuid4())  

def login_required(f):
    """
    Decorator to require login for a route
    
    This is a common security pattern in web applications. It creates a 
    decorator that can be applied to route functions to ensure users 
    are logged in before accessing protected content.
    
    Parameters:
        f (function): The view function to decorate
        
    Returns:
        function: The decorated function with login checking logic
        
    Usage example:
        @app.route('/protected')
        @login_required
        def protected_route():
            # This code only runs if user is logged in
    """
    @wraps(f) 
    def decorated_function(*args, **kwargs):
        print("login_required decorator - Session:", session)  
        try:
           
            if 'user_id' not in session:
                print("No user_id in session, redirecting to login")
                return redirect(url_for('login'))  
                
           
            user_id = session.get('user_id')
            print(f"Looking up user with ID: {user_id}")
            
          
            user = database.get_user_by_id(user_id)
            
            if not user:
                print(f"No user found with ID: {user_id}, redirecting to login")
                
                session.clear()
                return redirect(url_for('login'))
        except Exception as e:
            print(f"Exception in login_required decorator: {e}")
            session.clear()
            return redirect(url_for('login'))
            
        print(f"Found user: {user.username}, role: {user.role}")
            
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin role for a route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("admin_required decorator - Session:", session)
        try:
            if 'user_id' not in session:
                print("No user_id in session, redirecting to login")
                return redirect(url_for('login'))
            
            user_id = session['user_id']
            user_role = session.get('user_role')
            print(f"Found user_id: {user_id}, role from session: {user_role}")
            
           
            user = database.get_user_by_id(user_id)
            if not user:
                print(f"No user found with ID: {user_id}")
                
                session.clear()
                return redirect(url_for('login'))
                
            print(f"User from DB: {user.username}, role from DB: {user.role}")
            
            if user.role != 'manager':
                print(f"User {user.username} is not a manager, redirecting to dashboard")
                return redirect(url_for('dashboard'))
        except Exception as e:
            print(f"Exception in admin_required decorator: {e}")
            session.clear()
            return redirect(url_for('login'))
        
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Get the current logged in user"""
    print("get_current_user - Session:", session)
    try:
        if 'user_id' in session:
            user_id = session['user_id']
            print(f"Looking up user with ID: {user_id}")
            user = database.get_user_by_id(user_id)
            if user:
                print(f"Found user: {user.username}, role: {user.role}")
                return user
            else:
                print(f"No user found with ID: {user_id}")
                # Clear the invalid session data
                session.clear()
        else:
            print("No user_id in session")
    except Exception as e:
        print(f"Exception in get_current_user: {e}")
        # Clear the session on error to force a new login
        session.clear()
    return None

def format_datetime(dt):
    """Format a datetime object to string"""
    if not dt:
        return ""
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except:
            return dt
    return dt.strftime('%Y-%m-%d %H:%M')

def format_date(dt):
    """Format a date object to string"""
    if not dt:
        return ""
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except:
            return dt
    return dt.strftime('%Y-%m-%d')

def count_tasks_by_status(tasks):
    """Count tasks by status"""
    counts = {
        'pending': 0,
        'in_progress': 0,
        'done': 0,
        'overdue': 0,
        'total': len(tasks)
    }
    
    for task in tasks:
        if task.status in counts:
            counts[task.status] += 1
    
    return counts

def calculate_completion_rate(tasks):
    """Calculate completion rate of tasks"""
    if not tasks:
        return 0
    
    done_count = sum(1 for task in tasks if task.status == 'done')
    return round((done_count / len(tasks)) * 100, 2)

def calculate_overdue_rate(tasks):
    """Calculate overdue rate of tasks"""
    if not tasks:
        return 0
    
    overdue_count = sum(1 for task in tasks if task.status == 'overdue')
    return round((overdue_count / len(tasks)) * 100, 2)

def get_team_workload():
    """Get workload for all team members"""
    all_users = database.get_all_users()
    workload = []
    
    for user in all_users:
        if user.role == 'member':
            user_tasks = database.get_tasks_by_user(user.id)
            
            # Skip users with no tasks
            if not user_tasks:
                continue
                
            task_counts = count_tasks_by_status(user_tasks)
            completion_rate = calculate_completion_rate(user_tasks)
            
            workload.append({
                'user': user,
                'tasks': user_tasks,
                'task_counts': task_counts,
                'completion_rate': completion_rate,
                'occupancy': min(100, round(len(user_tasks) * 10, 2))  
            })
    
    return workload

def get_project_progress(project_id):
    """Get progress for a project"""
    project = database.get_project(project_id)
    if not project:
        return None
    
    tasks = database.get_tasks_by_project(project_id)
    task_counts = count_tasks_by_status(tasks)
    completion_rate = calculate_completion_rate(tasks)
    
    return {
        'project': project,
        'tasks': tasks,
        'task_counts': task_counts,
        'completion_rate': completion_rate
    }

def get_task_distribution():
    """Get task distribution by category and priority"""
    all_tasks = database.get_all_tasks()
    
    category_counts = {}
    priority_counts = {}
    
    for task in all_tasks:
        # Count by category
        if task.category not in category_counts:
            category_counts[task.category] = 0
        category_counts[task.category] += 1
        
        # Count by priority
        if task.priority not in priority_counts:
            priority_counts[task.priority] = 0
        priority_counts[task.priority] += 1
    
    return {
        'category': category_counts,
        'priority': priority_counts
    }

def update_task_status():
    """Update task statuses based on due dates"""
    all_tasks = database.get_all_tasks()
    now = datetime.now()
    now_date = now.date()
    
    for task in all_tasks:
        # Skip tasks without due dates or already completed
        if not task.due_date or task.status == 'done':
            continue
            
        # Normalize the task due date
        task_due_date = task.due_date
        if isinstance(task_due_date, datetime):
            task_due_date = task_due_date.date()
        elif isinstance(task_due_date, str):
            try:
                task_due_date = datetime.strptime(task_due_date, '%Y-%m-%d').date()
            except ValueError:
                continue
            
        # Update status based on due date
        if task_due_date < now_date:
            if task.status in ['pending', 'in_progress']:
                database.update_task(task.id, status='overdue')
        elif task.status == 'overdue':
            # If the task was overdue but the due date was changed to the future
            database.update_task(task.id, status='pending')
