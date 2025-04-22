# Gym Management System

A comprehensive Django-based web application for managing gym operations, focusing on the relationship between trainers and trainees with detailed activity tracking and progress monitoring.

## Overview

This Gym Management System allows gyms to manage both trainers and trainees through a secure platform. Trainers can monitor their assigned trainees' activities, provide personalized recommendations, and track trainee progress. Trainees can log their workout activities, track weight changes, and manage calorie intake.

## Features

### For Trainees
- **Account Management**: Create and manage trainee accounts
- **Activity Tracking**: Log workout activities with details (duration, calories burned, notes)
- **Weight Tracking**: Record weight measurements over time
- **Calorie Logging**: Track calories burned and consumed
- **Personalized Goals**: Set and update workout targets
- **Dashboard**: View weekly progress, recent weight logs, and trainer recommendations

### For Trainers
- **Trainee Management**: View all assigned trainees
- **Daily Monitoring**: Track today's activities and weight logs
- **Attendance Tracking**: Monitor trainee gym attendance
- **Workout Summary**: Access comprehensive workout data for all trainees
- **Personalized Recommendations**: Send custom recommendations to trainees
- **Performance Tracking**: Earn points towards goals for motivation

### System-wide
- **Role-based Access**: Different interfaces and capabilities for trainers and trainees
- **Secure Authentication**: User authentication and authorization
- **Data Management**: Comprehensive data models for storing and relating gym information

## Technical Architecture

### Django Apps
- **users**: Core user management with custom user model
- **trainees**: Functionality for trainee users
- **trainers**: Functionality for trainer users

### Models
- **CustomUser**: Extends Django's user model with role field
- **Trainee**: Profile for trainee users
- **Trainer**: Profile for trainer users with specialized fields
- **Activity**: Records workout sessions
- **WeightLog**: Tracks weight measurements
- **CalorieLog**: Monitors calorie intake and expenditure
- **WorkoutTarget**: Sets fitness goals
- **Recommendation**: Stores trainer advice to trainees

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/gym-management.git
cd gym-management
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Access the application at: http://127.0.0.1:8000/

## Usage

### As a Trainee
1. Sign up for a trainee account
2. Log in using your credentials
3. View your dashboard with fitness summaries
4. Log activities, weight, and calorie information
5. Set and update your workout targets
6. View recommendations from your trainer

### As a Trainer
1. Sign up for a trainer account with your qualifications
2. Log in using your credentials
3. View your dashboard with trainee information
4. Monitor trainee activities and progress
5. Send personalized recommendations to trainees
6. Track attendance and performance metrics

### As an Admin
1. Access the Django admin interface
2. Manage all users, activities, and system data
3. Create, update, or delete records as needed

## Development

### Project Structure
```
gymmanagement/
├── users/              # User authentication and base models
├── trainees/           # Trainee-specific functionality
├── trainers/           # Trainer-specific functionality
└── gymmanagement/      # Project settings and configuration
```

### Key Files
- **models.py**: Database models for each app
- **views.py**: View functions for handling requests
- **urls.py**: URL routing for each app
- **forms.py**: Form definitions for data input

## Extending the System

To add new features:
1. Create appropriate models in the relevant app
2. Add views to handle the feature logic
3. Create templates for UI components
4. Update URLs to route to new views
5. Add forms for data input if needed
6. Run migrations if database changes are made

## Acknowledgments

- Django Framework
- Bootstrap for frontend styling
