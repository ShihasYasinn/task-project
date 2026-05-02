import datetime
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta

def generate_project_tasks(project):
    """
    Generates tasks for a project based on its service's tasks.
    If the project is recurring, it generates tasks for each occurrence.
    """
    from tasks.models import Task
    
    service = project.service
    if not service:
        return

    # Get existing tasks to avoid duplicates or overwriting manual edits
    existing_tasks = {t.task_code: t for t in project.tasks.all()}

    # Get tasks from the service
    service_tasks = service.service_tasks.all()

    # Determine occurrences
    occurrences = []
    if not project.is_recurring:
        occurrences.append((project.start_date, project.end_date))
    else:
        current_start = project.start_date
        
        while current_start < project.recurrence_end_date:
            # Move to next occurrence start
            if project.period == 'daily':
                next_start = current_start + timedelta(days=project.repeat_every)
            elif project.period == 'weekly':
                next_start = current_start + timedelta(weeks=project.repeat_every)
            elif project.period == 'monthly':
                next_start = current_start + relativedelta(months=project.repeat_every)
            else:
                break
                
            # The end date of this instance is the start date of the next instance
            current_end = next_start
            
            # Cap the instance end date at the project's recurrence end date
            if current_end > project.recurrence_end_date:
                current_end = project.recurrence_end_date
                
            occurrences.append((current_start, current_end))
            current_start = next_start
            
            if len(occurrences) > 500:
                break

    # Get prefixes for task code
    service_prefix = (service.service_code[:3] if service.service_code else service.name[:3]).upper()
    project_prefix = (project.project_code.split('-')[1][:3] if '-' in project.project_code else project.project_code[:3]).upper()
    base_prefix = f"{service_prefix}{project_prefix}"

    tasks_to_create = []
    task_count = 1
    
    for occ_start, occ_end in occurrences:
        if service_tasks.exists():
            for service_task in service_tasks:
                task_code = f"{base_prefix}{task_count:03d}"
                
                # Only create if it doesn't exist
                if task_code not in existing_tasks:
                    new_task = Task(
                        project=project,
                        task_code=task_code,
                        title=service_task.title,
                        priority=service_task.priority,
                        assigned_days=service_task.assigned_days,
                        days_before_project_end=service_task.days_before_project_end,
                        start_date=occ_start,
                        end_date=occ_end,
                        assignee=project.assignee,
                        description=service_task.description,
                        status='open'
                    )
                    tasks_to_create.append(new_task)
                
                task_count += 1
        else:
            # Create a default task if no service tasks exist
            task_code = f"{base_prefix}{task_count:03d}"
            if task_code not in existing_tasks:
                new_task = Task(
                    project=project,
                    task_code=task_code,
                    title=f"Project Task: {project.friendly_name if project.friendly_name else service.name}",
                    priority='medium',
                    start_date=occ_start,
                    end_date=occ_end,
                    assignee=project.assignee,
                    description="Automatically generated task.",
                    status='open'
                )
                tasks_to_create.append(new_task)
            task_count += 1
            
    # Bulk create tasks
    if tasks_to_create:
        Task.objects.bulk_create(tasks_to_create)
