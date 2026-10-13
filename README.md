# 🏋️ MayeeFitness Hub - Multi-User Gym Management System

A web-based gym management application engineered with **Python Flask** and **Object-Oriented Programming (OOP)**, sporting a high-fidelity dark-themed interface with vibrant orange accents (`#ff6b00`).

Designed strictly following the Final Project specification:
- **3 Distinct User Roles**: Admin (Gym Owner / Staff), Trainer (Coach), and Member.
- **Login & Role-Based Access Control (RBAC)**: Secure multi-role authentication with session isolation.
- **Full CRUD Operations**: Create, Read, Update, and Delete for Members, Classes, Equipment, Payments, Workouts, and Goals.
- **Python OOP**: Core principles applied: **Encapsulation**, **Inheritance**, **Polymorphism**, and **Functions**.
- **Temporary In-Memory Storage**: Built purely on **Python Lists only (NO DATABASE)**.
- **Responsive UI**: Faithfully reproduced from design mockups for Admin Dashboard, Member Dashboard, and Login screens.
- **Ready for Online Deployment**: Configured for instant deployment on Render, Railway, or PythonAnywhere.

---

## 📸 Interface Preview & Design Alignment

| Screen | Description | UI Highlights |
|---|---|---|
| **Login Screen** | Multi-Role Authentication Pane | Split-screen hero, 4 KPI stats, Role switcher tabs, 1-Click demo logins |
| **Admin Dashboard** | Gym Owner Management Center | Monthly Revenue card (₱482,500), Revenue chart, Donut chart, Recent Members, Today's Classes, Peak Hours, Equipment Status, Quick Actions |
| **Member Dashboard** | Athlete Personalized Hub | Today's Workout hero with 67% progress ring, Calorie/Visit metrics, Weekly Activity chart, Digital Orange Membership Card with QR, Class booking, Goals |
| **Trainer Dashboard** | Coach & Athlete Performance | Assigned athletes, class schedules, custom routine assigner, and form advice |

---

## 🏛️ Python OOP Architecture

### 1. Inheritance
A polymorphic class hierarchy rooted in the base `User` class:

```
                  ┌──────────────┐
                  │     User     │ (Base Class: id, name, email, password, role)
                  └──────┬───────┘
          _______________|_______________
         │                               │                               │
┌────────────────┐             ┌───────────────────┐           ┌──────────────────┐
│   AdminUser    │             │    TrainerUser    │           │    MemberUser    │
│ (Gym Owner)    │             │  (Fitness Coach)  │           │ (Athlete/Client) │
└────────────────┘             └───────────────────┘           └──────────────────┘
```

- `AdminUser(User)`: Extends `User` with managerial title, full administrative privileges, and financial access.
- `TrainerUser(User)`: Extends `User` with coaching specialty, client assignment list, ratings, and routine builder.
- `MemberUser(User)`: Extends `User` with membership code (`#MF-1290`), plan type, expiration dates, attendance streaks, weight logs, and booked class IDs.

### 2. Polymorphism
Subclasses override base class methods to provide specialized behavior without conditional branching:

- `get_dashboard_url()`:
  - `AdminUser` $\rightarrow$ `"/admin"`
  - `TrainerUser` $\rightarrow$ `"/trainer"`
  - `MemberUser` $\rightarrow$ `"/member"`
- `get_role_display()`:
  - `AdminUser` $\rightarrow$ `"Gym Owner"`
  - `TrainerUser` $\rightarrow$ `"Coach (HIIT & Strength)"`
  - `MemberUser` $\rightarrow$ `"Annual Member"`
- `can_access(feature)`:
  - `AdminUser` $\rightarrow$ returns `True` for all sections.
  - `TrainerUser` $\rightarrow$ returns `True` only for classes, workouts, and trainee rosters.
  - `MemberUser` $\rightarrow$ returns `True` only for workouts, booking, and personal goals.

### 3. Encapsulation
- Sensitive and state attributes (e.g. `_password`, `_email`, `_status`, `_capacity`) are defined as private/protected.
- Accessed and modified exclusively via `@property` getters and setters with validation logic:
  - **Email validation**: Regex pattern check preventing malformed emails.
  - **Password security**: `verify_password()` and `change_password()` requiring length constraints.
  - **Positive constraints**: Capacities, units, weights, and fees are validated before mutating state.

### 4. Functions & Modular Business Logic
- Decorator functions: `@login_required`, `@role_required(['admin'])`.
- Calculation helpers: Percentage fill rates, SVG circular progress math, and attendance incrementers.

---

## 🗄️ Temporary Storage Architecture (Python Lists Only)

Strictly adhering to the constraint: **"Use Python Lists only; NO DATABASE"**.

The `DataStore` singleton class in `storage.py` maintains in-memory Python lists:
```python
self.users: List[User] = []           # AdminUser, TrainerUser, MemberUser instances
self.classes: List[GymClass] = []       # Scheduled fitness classes
self.equipment: List[EquipmentItem] = [] # Gym gear & maintenance status
self.payments: List[PaymentRecord] = []  # Financial transactions
self.workouts: List[WorkoutPlan] = []    # Assigned workout routines
self.goals: List[FitnessGoal] = []       # Personal fitness targets
```

The system pre-seeds these lists on startup with realistic data matching the design mockups.

---

## 👥 Default User Accounts & Credentials

For fast testing and grading, use these pre-seeded accounts (or use the **1-Click Demo Login chips** on `/login`):

| Role | Name | Email | Password | Access / Responsibilities |
|---|---|---|---|---|
| **Admin** | Mayee Santos | `admin@mayeefitness.com` | `admin` | Full gym access, member CRUD, revenue, equipment, class creation |
| **Trainer** | Coach Dan | `dan@mayeefitness.com` | `coach` | Trainee rosters, workout routines assigner, class attendance |
| **Member** | Maya Santos | `maya@mayeefitness.com` | `member` | Workout tracker, class booking, QR check-in, personal goals |

---

## 🚀 Local Setup & Installation

### Prerequisites
- Python 3.9+ installed on your system.

### Step 1: Open Terminal in the project directory
```powershell
cd C:\Users\Mono\Documents\mayeefitnesshub
```

### Step 2: Install dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Run the web application
```powershell
python app.py
```

### Step 4: Open in your browser
Navigate to:
```
http://127.0.0.1:5000
```

---

## 🌐 Online Deployment Guide (Free Hosting)

To fulfill the requirement: **"The completed system must be hosted online and accessible through a browser"**:

### Option A: Free Deployment on Render.com (Recommended)
1. Initialize a Git repository and commit your files:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of MayeeFitness Hub"
   ```
2. Push your project to a new **GitHub repository** (e.g. `https://github.com/your-username/mayeefitnesshub`).
3. Sign in to [Render.com](https://render.com) using your GitHub account.
4. Click **New +** $\rightarrow$ **Web Service**.
5. Connect your GitHub repository `mayeefitnesshub`.
6. Configure the service:
   - **Name**: `mayeefitnesshub`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app` (or `python app.py`)
7. Click **Create Web Service**. Within 2 minutes, you will get a free live URL (e.g. `https://mayeefitnesshub.onrender.com`)!

### Option B: Free Deployment on PythonAnywhere
1. Sign up for a free account at [PythonAnywhere.com](https://www.pythonanywhere.com).
2. Open a Bash console and clone your GitHub repository:
   ```bash
   git clone https://github.com/your-username/mayeefitnesshub.git
   ```
3. Install Flask:
   ```bash
   pip install flask
   ```
4. In the **Web** tab, configure the WSGI configuration file to point to `app.py`.
5. Reload your web app to get your live URL: `https://yourusername.pythonanywhere.com`.

---

## 🎯 Project Presentation Outline (For Project Defense)

When presenting your final project submission:

1. **Introduction & Motivation**
   - Project: *MayeeFitness Hub - Modern Multi-User Gym Management Platform*.
   - Problem solved: Streamlines interactions between gym owners, fitness trainers, and members within a unified, modern interface.
2. **System Architecture & Constraints**
   - Pure Python Flask backend + vanilla HTML5/CSS3/JS.
   - 100% database-free temporary storage utilizing OOP in-memory Python lists.
3. **Core OOP Demonstrations**
   - **Inheritance**: `User` parent class extended by `AdminUser`, `TrainerUser`, and `MemberUser`.
   - **Polymorphism**: Dynamic method resolution for dashboard routing, permissions, and roles.
   - **Encapsulation**: Private fields (`_password`, `_status`, `_email`) guarded by validated properties.
4. **Live System Walkthrough**
   - Demonstrate 1-click login as **Admin** $\rightarrow$ Review revenue KPIs, add a new member, update equipment status.
   - Switch to **Trainer** $\rightarrow$ View assigned trainees, assign a custom workout.
   - Switch to **Member** (Maya Santos) $\rightarrow$ Complete workout exercises, book a class, simulate QR check-in.
5. **Conclusion & Future Work**
   - Highlight the clean separation of concerns and how the architecture is ready for database integration (e.g. SQLAlchemy) if required in future releases.
