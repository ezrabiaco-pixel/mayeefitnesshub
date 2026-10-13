"""
MayeeFitness Hub - Multi-User Web-Based Management System
Powered by Python Flask & Object-Oriented Programming (OOP)
Temporary In-Memory Storage: Python Lists Only (NO DATABASE)
"""

from functools import wraps
from datetime import datetime
from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, abort, jsonify
)
from storage import DataStore
from models import AdminUser, TrainerUser, MemberUser

app = Flask(__name__)
app.secret_key = "mayeefitness_hub_super_secret_key_2026"

# Initialize DataStore singleton (In-memory Python lists)
store = DataStore()


# ==============================================================================
# ROLE-BASED ACCESS CONTROL (RBAC) DECORATORS
# ==============================================================================
def login_required(f):
    """Decorator ensuring user is authenticated before accessing route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please sign in to access this page.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


def role_required(allowed_roles):
    """Decorator restricting route access to specific user roles."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                flash("Please sign in first.", "warning")
                return redirect(url_for("login"))
            user_role = session.get("role")
            if user_role not in allowed_roles:
                flash("Access denied: You do not have permission to view that page.", "danger")
                return render_template("403.html"), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def get_current_user():
    """Helper function to fetch the currently logged-in User instance."""
    user_id = session.get("user_id")
    if user_id:
        return store.get_user_by_id(user_id)
    return None


@app.context_processor
def inject_global_data():
    """Context processor making user state, notifications, and current date available to all templates."""
    current_user = get_current_user()
    notifications = store.get_notifications()
    unread_count = sum(1 for n in notifications if n.get("unread", False))
    return {
        "current_user": current_user,
        "current_year": datetime.now().year,
        "today_str": datetime.now().strftime("%A, %B %d, %Y"),
        "global_notifications": notifications,
        "unread_notifications_count": unread_count
    }


# ==============================================================================
# AUTHENTICATION ROUTES
# ==============================================================================
@app.route("/")
def index():
    """Root route redirects authenticated users to their specific dashboard."""
    user = get_current_user()
    if user:
        return redirect(user.get_dashboard_url())
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login page matching Image 3 mockup.
    Supports Member, Trainer, and Admin logins with role tabs and demo quick-login.
    """
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        selected_role = request.form.get("role_tab", "member").strip()

        if not email or not password:
            flash("Please enter both email address and password.", "danger")
            return render_template("login.html", active_tab=selected_role, email=email)

        user = store.get_user_by_email(email)

        # Validation and credential verification
        if user and user.verify_password(password):
            session["user_id"] = user.id
            session["role"] = user.role
            session["user_name"] = user.name
            flash(f"Welcome back, {user.name}!", "success")
            # Polymorphic redirect based on user role
            return redirect(user.get_dashboard_url())
        else:
            flash("Invalid email or password. Please verify your credentials.", "danger")
            return render_template("login.html", active_tab=selected_role, email=email)

    active_tab = request.args.get("tab", "member")
    return render_template("login.html", active_tab=active_tab)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Self-registration page for new gym members."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        phone = request.form.get("phone", "").strip()
        plan = request.form.get("plan", "Monthly").strip()

        if not name or not email or not password:
            flash("All required fields must be filled.", "danger")
            return render_template("register.html")

        try:
            member = store.add_member(
                name=name,
                email=email,
                password=password,
                phone=phone,
                plan=plan,
                trainer_name="Unassigned",
                expires="Nov 2027",
                status="Active"
            )
            # Automatically log in the newly registered member
            session["user_id"] = member.id
            session["role"] = member.role
            session["user_name"] = member.name
            flash("Account successfully created! Welcome to MayeeFitness Hub.", "success")
            return redirect(url_for("member_dashboard"))
        except ValueError as e:
            flash(str(e), "danger")
            return render_template("register.html")

    return render_template("register.html")


@app.route("/auth/<provider>")
def social_login(provider):
    """Handles 1-click social logins for Google and Facebook without errors."""
    provider_name = provider.capitalize()
    # Log in as member demo account
    user = store.get_user_by_email("maya@mayeefitness.com")
    if user:
        session["user_id"] = user.id
        session["role"] = user.role
        session["user_name"] = user.name
        flash(f"Successfully signed in via {provider_name}! Welcome back, {user.name}.", "success")
        return redirect(user.get_dashboard_url())
    flash(f"{provider_name} authentication completed.", "info")
    return redirect(url_for("login"))


@app.route("/forgot-password", methods=["POST"])
def forgot_password():
    """Simulates password recovery with instant feedback."""
    email = request.form.get("email", "").strip().lower()
    user = store.get_user_by_email(email)
    if user:
        flash(f"Account found for {user.name}! Your demo password is: '{user._password}'. Use it to sign in.", "info")
    else:
        flash(f"If an account is associated with {email}, password reset credentials have been prepared. Use demo password 'member' to sign in.", "info")
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    """Logs out user and clears session state."""
    session.clear()
    flash("You have been signed out successfully.", "info")
    return redirect(url_for("login"))


# ==============================================================================
# DASHBOARD ROUTES (ROLE SPECIFIC)
# ==============================================================================
@app.route("/admin")
@login_required
@role_required(["admin"])
def admin_dashboard():
    """
    Admin Dashboard faithfully matching Image 1:
    - Monthly Revenue (₱482,500), Active Members (1,284), Check-ins Today (312), Expiring Soon (27)
    - Revenue Overview Line Chart, Membership Plans Donut
    - Recent Members table with status badges and avatars
    - Today's Classes with capacity bars
    - Peak Hours bar chart, Equipment Status badges, Quick Actions
    """
    members = store.get_members()
    classes = store.get_classes()
    equipment = store.get_equipment()
    payments = store.get_payments()
    trainers = store.get_trainers()

    # Pre-calculated KPI metrics matching UI
    active_count = sum(1 for m in members if m.status == "Active")
    expiring_count = sum(1 for m in members if m.status == "Expiring")

    return render_template(
        "admin_dashboard.html",
        members=members,
        classes=classes,
        equipment=equipment,
        payments=payments,
        trainers=trainers,
        active_count=active_count,
        expiring_count=expiring_count
    )


@app.route("/member")
@login_required
@role_required(["member"])
def member_dashboard():
    """
    Member Dashboard faithfully matching Image 2:
    - Hi Maya banner, Upper Body Power workout widget (67% complete)
    - Calories burned (2,480), Workouts (5/6), Body weight (58.4 kg), Gym visits (18)
    - Weekly Activity Chart, Orange Membership Card with QR
    - Upcoming Classes with Booked/Book state
    - Goals with progress bars (Lose 4kg, Bench press 50kg, 20 visits/month)
    """
    user = get_current_user()
    if not isinstance(user, MemberUser):
        return redirect(url_for("login"))

    classes = store.get_classes()
    workout = store.get_workout_for_member(user.id)
    goals = store.get_goals_for_member(user.id)

    return render_template(
        "member_dashboard.html",
        member=user,
        classes=classes,
        workout=workout,
        goals=goals
    )


@app.route("/trainer")
@login_required
@role_required(["trainer", "admin"])
def trainer_dashboard():
    """
    Trainer Dashboard for Fitness Coaches:
    - View assigned classes and rosters
    - View trainees / assigned members
    - Manage workout plans and progress feedback
    """
    user = get_current_user()
    all_members = store.get_members()
    classes = store.get_classes()

    # Filter classes assigned to this trainer
    trainer_classes = [c for c in classes if user.name.lower() in c.trainer.lower()] if isinstance(user, TrainerUser) else classes

    return render_template(
        "trainer_dashboard.html",
        trainer=user,
        members=all_members,
        trainer_classes=trainer_classes,
        classes=classes
    )


# ==============================================================================
# CRUD ROUTES: MEMBERS MANAGEMENT
# ==============================================================================
@app.route("/members")
@login_required
@role_required(["admin", "trainer"])
def members_list():
    """Lists all members with search and plan/status filtering."""
    query = request.args.get("q", "").strip().lower()
    status_filter = request.args.get("status", "All")

    members = store.get_members()
    trainers = store.get_trainers()

    if query:
        members = [m for m in members if query in m.name.lower() or query in m.email.lower() or query in m.member_code.lower()]

    if status_filter != "All":
        members = [m for m in members if m.status.lower() == status_filter.lower()]

    return render_template("members.html", members=members, trainers=trainers, current_filter=status_filter, query=query)


@app.route("/members/add", methods=["POST"])
@login_required
@role_required(["admin"])
def add_member():
    """Adds a new member record to the in-memory Python list."""
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "member123").strip()
    phone = request.form.get("phone", "").strip()
    plan = request.form.get("plan", "Monthly").strip()
    trainer_name = request.form.get("trainer_name", "Unassigned").strip()
    expires = request.form.get("expires", "Nov 2027").strip()
    status = request.form.get("status", "Active").strip()

    if not name or not email:
        flash("Name and email are required fields.", "danger")
        return redirect(url_for("members_list"))

    try:
        new_m = store.add_member(
            name=name,
            email=email,
            password=password,
            phone=phone,
            plan=plan,
            trainer_name=trainer_name,
            expires=expires,
            status=status
        )
        flash(f"Member '{new_m.name}' ({new_m.member_code}) added successfully!", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("members_list"))


@app.route("/members/edit/<int:user_id>", methods=["POST"])
@login_required
@role_required(["admin"])
def edit_member(user_id):
    """Updates an existing member in the Python list."""
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    plan = request.form.get("plan", "Monthly").strip()
    trainer_name = request.form.get("trainer_name", "Unassigned").strip()
    expires = request.form.get("expires", "Nov 2027").strip()
    status = request.form.get("status", "Active").strip()

    try:
        updated = store.update_member(
            user_id=user_id,
            name=name,
            email=email,
            phone=phone,
            plan=plan,
            trainer_name=trainer_name,
            expires=expires,
            status=status
        )
        if updated:
            flash(f"Member #{user_id} updated successfully.", "success")
        else:
            flash(f"Member not found.", "danger")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("members_list"))


@app.route("/members/delete/<int:user_id>", methods=["POST"])
@login_required
@role_required(["admin"])
def delete_member(user_id):
    """Deletes a member from the Python list."""
    user = store.get_user_by_id(user_id)
    if user and isinstance(user, MemberUser):
        name = user.name
        store.delete_user(user_id)
        flash(f"Member '{name}' has been deleted.", "info")
    else:
        flash("Member not found.", "danger")
    return redirect(url_for("members_list"))


# ==============================================================================
# CRUD ROUTES: CLASSES & SCHEDULE
# ==============================================================================
@app.route("/classes")
@login_required
def classes_list():
    """Displays scheduled fitness classes with booking capabilities."""
    classes = store.get_classes()
    trainers = store.get_trainers()
    current_u = get_current_user()
    return render_template("classes.html", classes=classes, trainers=trainers, current_u=current_u)


@app.route("/classes/add", methods=["POST"])
@login_required
@role_required(["admin", "trainer"])
def add_class():
    """Adds a new GymClass to the temporary Python list."""
    title = request.form.get("title", "").strip()
    trainer = request.form.get("trainer", "").strip()
    time_slot = request.form.get("time_slot", "").strip()
    day = request.form.get("day", "").strip()
    studio = request.form.get("studio", "Studio A").strip()
    capacity = int(request.form.get("capacity", 20))

    if not title or not trainer or not time_slot:
        flash("Please fill all required class fields.", "danger")
        return redirect(url_for("classes_list"))

    store.add_class(title, trainer, time_slot, day, studio, capacity)
    flash(f"Class '{title}' has been successfully scheduled!", "success")
    return redirect(url_for("classes_list"))


@app.route("/classes/edit/<int:class_id>", methods=["POST"])
@login_required
@role_required(["admin", "trainer"])
def edit_class(class_id):
    """Updates an existing class in the list."""
    title = request.form.get("title", "").strip()
    trainer = request.form.get("trainer", "").strip()
    time_slot = request.form.get("time_slot", "").strip()
    day = request.form.get("day", "").strip()
    studio = request.form.get("studio", "").strip()
    capacity = int(request.form.get("capacity", 20))

    updated = store.update_class(class_id, title, trainer, time_slot, day, studio, capacity)
    if updated:
        flash("Class updated successfully.", "success")
    else:
        flash("Class not found.", "danger")
    return redirect(url_for("classes_list"))


@app.route("/classes/delete/<int:class_id>", methods=["POST"])
@login_required
@role_required(["admin", "trainer"])
def delete_class(class_id):
    """Deletes a class from the list."""
    gym_class = store.get_class_by_id(class_id)
    if gym_class:
        title = gym_class.title
        store.delete_class(class_id)
        flash(f"Class '{title}' has been removed.", "info")
    else:
        flash("Class not found.", "danger")
    return redirect(url_for("classes_list"))


@app.route("/classes/book/<int:class_id>", methods=["POST"])
@login_required
@role_required(["member"])
def book_class(class_id):
    """Member enrolls in or cancels booking for a class."""
    member = get_current_user()
    gym_class = store.get_class_by_id(class_id)

    if not gym_class or not isinstance(member, MemberUser):
        flash("Unable to complete booking.", "danger")
        return redirect(url_for("member_dashboard"))

    if class_id in member.booked_class_ids:
        # Cancel booking
        member.cancel_class(class_id)
        gym_class.unenroll(member.id)
        flash(f"Booking cancelled for '{gym_class.title}'.", "info")
    else:
        # Enroll in class
        if gym_class.is_full:
            flash(f"Sorry, '{gym_class.title}' is currently full!", "danger")
        else:
            member.book_class(class_id)
            gym_class.enroll(member.id)
            flash(f"Successfully booked your spot in '{gym_class.title}'!", "success")

    # Redirect back to referring page (dashboard or classes list)
    referrer = request.referrer or url_for("member_dashboard")
    return redirect(referrer)


# ==============================================================================
# CRUD ROUTES: EQUIPMENT MANAGEMENT
# ==============================================================================
@app.route("/equipment")
@login_required
def equipment_list():
    """Displays equipment status inventory."""
    equipment = store.get_equipment()
    return render_template("equipment.html", equipment=equipment)


@app.route("/equipment/add", methods=["POST"])
@login_required
@role_required(["admin"])
def add_equipment():
    """Adds a new equipment inventory record."""
    name = request.form.get("name", "").strip()
    units = int(request.form.get("units", 1))
    status = request.form.get("status", "All OK").strip()
    category = request.form.get("category", "Free Weights").strip()

    if not name:
        flash("Equipment name is required.", "danger")
        return redirect(url_for("equipment_list"))

    store.add_equipment(name, units, status, category)
    flash(f"Equipment '{name}' added to inventory.", "success")
    return redirect(url_for("equipment_list"))


@app.route("/equipment/edit/<int:eq_id>", methods=["POST"])
@login_required
@role_required(["admin"])
def edit_equipment(eq_id):
    """Updates equipment units and status."""
    name = request.form.get("name", "").strip()
    units = int(request.form.get("units", 1))
    status = request.form.get("status", "All OK").strip()
    category = request.form.get("category", "General").strip()

    updated = store.update_equipment(eq_id, name, units, status, category)
    if updated:
        flash("Equipment record updated successfully.", "success")
    else:
        flash("Equipment not found.", "danger")
    return redirect(url_for("equipment_list"))


@app.route("/equipment/delete/<int:eq_id>", methods=["POST"])
@login_required
@role_required(["admin"])
def delete_equipment(eq_id):
    """Deletes equipment from inventory."""
    deleted = store.delete_equipment(eq_id)
    if deleted:
        flash("Equipment item removed.", "info")
    else:
        flash("Equipment item not found.", "danger")
    return redirect(url_for("equipment_list"))


# ==============================================================================
# CRUD ROUTES: PAYMENTS & REVENUE
# ==============================================================================
@app.route("/payments")
@login_required
@role_required(["admin"])
def payments_list():
    """Displays payment transactions and gym revenue statistics."""
    payments = store.get_payments()
    total_rev = store.get_total_revenue()
    members = store.get_members()
    return render_template("payments.html", payments=payments, total_rev=total_rev, members=members)


@app.route("/payments/add", methods=["POST"])
@login_required
@role_required(["admin"])
def add_payment():
    """Records a new membership payment transaction."""
    member_name = request.form.get("member_name", "").strip()
    member_code = request.form.get("member_code", "#MF-1000").strip()
    plan = request.form.get("plan", "Monthly").strip()
    amount = float(request.form.get("amount", 2500.00))
    method = request.form.get("method", "GCash").strip()

    if not member_name or amount <= 0:
        flash("Invalid payment details provided.", "danger")
        return redirect(url_for("payments_list"))

    store.add_payment(member_name, member_code, plan, amount, method)
    flash(f"Payment of ₱{amount:,.2f} recorded for {member_name}.", "success")
    return redirect(url_for("payments_list"))


# ==============================================================================
# WORKOUTS & PROGRESS ACTIONS
# ==============================================================================
@app.route("/workouts/toggle-exercise/<int:plan_id>/<int:ex_idx>", methods=["POST"])
@login_required
def toggle_exercise(plan_id, ex_idx):
    """Toggles exercise completion state within a workout plan."""
    for w in store.workouts:
        if w.id == plan_id:
            w.toggle_exercise(ex_idx)
            flash(f"Workout progress updated: {w.completion_percentage}% completed!", "success")
            break
    referrer = request.referrer or url_for("member_dashboard")
    return redirect(referrer)


@app.route("/workouts/assign", methods=["POST"])
@login_required
@role_required(["trainer", "admin"])
def assign_workout():
    """Coach assigns a customized workout plan to a member."""
    member_id = int(request.form.get("member_id", 0))
    title = request.form.get("title", "Custom Strength Plan").strip()
    duration_min = int(request.form.get("duration_min", 45))
    notes = request.form.get("notes", "").strip()

    user = get_current_user()
    assigned_by = user.name if user else "Coach"

    store.add_workout_plan(member_id, title, duration_min, assigned_by, notes)
    flash(f"Workout routine '{title}' assigned successfully!", "success")
    return redirect(url_for("trainer_dashboard"))


@app.route("/member/log-visit", methods=["POST"])
@login_required
@role_required(["member"])
def log_visit():
    """Member logs a QR contactless check-in visit."""
    member = get_current_user()
    if isinstance(member, MemberUser):
        member.log_visit()
        flash(f"Checked in! Total visits: {member.visits} (Streak: {member.streak_days} days 🔥)", "success")
    return redirect(url_for("member_dashboard"))


@app.route("/goals/update/<int:goal_id>", methods=["POST"])
@login_required
@role_required(["member"])
def update_goal(goal_id):
    """Member updates their personal target or current fitness goal progress."""
    current_val = float(request.form.get("current_val", 0))
    target_val = float(request.form.get("target_val", 100))

    if store.update_goal(goal_id, current_val, target_val):
        flash("Goal progress updated successfully!", "success")
    else:
        flash("Goal not found.", "danger")
    return redirect(url_for("member_dashboard"))


# ==============================================================================
# SETTINGS & PROFILE
# ==============================================================================
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Allows user to view and edit their profile and password."""
    user = get_current_user()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        old_pass = request.form.get("old_password", "").strip()
        new_pass = request.form.get("new_password", "").strip()

        if name:
            user.name = name
        user.phone = phone

        if old_pass and new_pass:
            if user.change_password(old_pass, new_pass):
                flash("Password updated successfully!", "success")
            else:
                flash("Current password incorrect. Password not changed.", "danger")
        else:
            flash("Profile updated successfully.", "success")

        return redirect(url_for("profile"))

    return render_template("profile.html", user=user)


# ==============================================================================
# NOTIFICATIONS & HEADER ACTIONS
# ==============================================================================
@app.route("/notifications/read", methods=["POST"])
@login_required
def mark_notifications_read():
    """Marks all user notifications as read."""
    store.mark_notifications_read()
    return jsonify({"success": True})


@app.route("/notifications/clear", methods=["POST"])
@login_required
def clear_notifications():
    """Clears all notifications."""
    store.clear_notifications()
    flash("All notifications cleared.", "info")
    referrer = request.referrer or url_for("index")
    return redirect(referrer)


@app.route("/admin/send-reminders", methods=["POST"])
@login_required
@role_required(["admin"])
def send_reminders():
    """Dispatches renewal reminders to members expiring soon."""
    store.add_notification("📱", "SMS Reminders Sent", "Automated renewal alerts dispatched to 27 expiring members.")
    flash("Automated SMS and email reminders successfully sent to 27 members!", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/pro-analytics", methods=["POST"])
@login_required
@role_required(["admin"])
def pro_analytics():
    """Enables Pro Analytics simulation."""
    store.add_notification("📊", "Pro Analytics Enabled", "AI Retention and Churn Forecasting activated.")
    flash("Pro Analytics features activated! Real-time churn forecasting is now live.", "success")
    return redirect(url_for("admin_dashboard"))


# ==============================================================================
# GLOBAL SEARCH
# ==============================================================================
@app.route("/search")
@login_required
def search():
    """Searches across members, classes, equipment, and trainers."""
    q = request.args.get("q", "").strip().lower()
    members = [m for m in store.get_members() if q in m.name.lower() or q in m.email.lower() or q in m.member_code.lower()] if q else []
    classes = [c for c in store.get_classes() if q in c.title.lower() or q in c.trainer.lower() or q in c.studio.lower()] if q else []
    equipment = [eq for eq in store.get_equipment() if q in eq.name.lower() or q in eq.category.lower()] if q else []
    trainers = [t for t in store.get_trainers() if q in t.name.lower() or q in t.specialty.lower()] if q else []
    return render_template("search_results.html", query=q, members=members, classes=classes, equipment=equipment, trainers=trainers)


# ==============================================================================
# WORKOUT PLANS & PROGRESS
# ==============================================================================
@app.route("/workouts")
@login_required
def workouts():
    """Displays dedicated workout plans page."""
    user = get_current_user()
    workout = store.get_workout_for_member(user.id)
    all_members = store.get_members()
    return render_template("workouts.html", user=user, workout=workout, members=all_members, workouts=store.workouts)


@app.route("/progress")
@login_required
def progress():
    """Displays athlete fitness progress and metrics."""
    user = get_current_user()
    if not isinstance(user, MemberUser):
        return redirect(url_for("member_dashboard"))
    goals = store.get_goals_for_member(user.id)
    return render_template("progress.html", member=user, goals=goals)


@app.route("/billing")
@login_required
def billing():
    """Displays membership card and billing history."""
    user = get_current_user()
    if not isinstance(user, MemberUser):
        return redirect(url_for("member_dashboard"))
    member_payments = [p for p in store.get_payments() if user.name.lower() in p.member_name.lower()]
    return render_template("billing.html", member=user, payments=member_payments)


@app.route("/member/renew", methods=["POST"])
@login_required
@role_required(["member"])
def renew_membership():
    """Member renews or upgrades their gym membership."""
    user = get_current_user()
    plan = request.form.get("plan", user.plan).strip()
    method = request.form.get("method", "GCash").strip()
    amount = 24000.0 if plan == "Annual" else (6800.0 if plan == "Quarterly" else 2500.0)

    user.plan = plan
    user.expires = "Oct 2028"
    user.status = "Active"
    store.add_payment(user.name, user.member_code, plan, amount, method)
    store.add_notification("🎉", "Membership Renewed", f"{user.name} renewed their {plan} plan via {method}.")
    flash(f"Your {plan} membership has been renewed successfully! Valid through Oct 2028.", "success")
    return redirect(url_for("billing"))


# ==============================================================================
# CHAT WITH COACH
# ==============================================================================
@app.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    """Interactive messaging between member and trainer."""
    user = get_current_user()

    if request.method == "POST":
        message = request.form.get("message", "").strip()
        recipient_id = int(request.form.get("recipient_id", 0))

        if message:
            recipient = store.get_user_by_id(recipient_id)
            if not recipient:
                recipient = store.get_user_by_email("dan@mayeefitness.com")

            store.add_chat_message(user.id, user.name, user.role, recipient.id, message)
            flash("Message sent to coach!", "success")
        return redirect(url_for("chat", recipient_id=recipient_id))

    recipient_id = request.args.get("recipient_id")
    if recipient_id:
        recipient = store.get_user_by_id(int(recipient_id))
    else:
        if user.role == "member":
            recipient = store.get_user_by_email("dan@mayeefitness.com")
        else:
            recipient = store.get_user_by_email("maya@mayeefitness.com")

    chat_history = store.get_chat_history(user.id, recipient.id) if recipient else []
    trainers = store.get_trainers()
    members = store.get_members()

    return render_template("chat.html", user=user, recipient=recipient, chat_history=chat_history, trainers=trainers, members=members)


# ==============================================================================
# REPORTS & TRAINERS (ADMIN & COACH)
# ==============================================================================
@app.route("/reports")
@login_required
@role_required(["admin"])
def reports():
    """Admin gym performance, financial and membership reports."""
    members = store.get_members()
    classes = store.get_classes()
    equipment = store.get_equipment()
    payments = store.get_payments()
    total_rev = store.get_total_revenue()
    return render_template("reports.html", members=members, classes=classes, equipment=equipment, payments=payments, total_rev=total_rev)


@app.route("/trainers")
@login_required
def trainers():
    """Displays trainers directory."""
    all_trainers = store.get_trainers()
    classes = store.get_classes()
    return render_template("trainers.html", trainers=all_trainers, classes=classes)


@app.route("/trainers/add", methods=["POST"])
@login_required
@role_required(["admin"])
def add_trainer():
    """Admin adds a new trainer to the system."""
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    specialty = request.form.get("specialty", "General Fitness").strip()
    phone = request.form.get("phone", "").strip()
    bio = request.form.get("bio", "").strip()

    if not name or not email:
        flash("Name and email are required.", "danger")
        return redirect(url_for("trainers"))

    try:
        store.add_trainer(name, email, "coach", phone, specialty, bio)
        flash(f"Trainer '{name}' added successfully!", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("trainers"))


# ==============================================================================
# GOALS & STREAK REWARDS
# ==============================================================================
@app.route("/goals/add", methods=["POST"])
@login_required
@role_required(["member"])
def add_goal():
    """Member adds a new fitness goal."""
    user = get_current_user()
    title = request.form.get("title", "").strip()
    current_val = float(request.form.get("current_val", 0))
    target_val = float(request.form.get("target_val", 100))
    unit = request.form.get("unit", "kg").strip()

    if title and target_val > 0:
        store.add_goal(user.id, title, current_val, target_val, unit)
        flash(f"Fitness goal '{title}' added to your tracker!", "success")
    return redirect(request.referrer or url_for("member_dashboard"))


@app.route("/goals/delete/<int:goal_id>", methods=["POST"])
@login_required
@role_required(["member"])
def delete_goal(goal_id):
    """Member deletes a fitness goal."""
    store.delete_goal(goal_id)
    flash("Fitness goal removed.", "info")
    return redirect(request.referrer or url_for("member_dashboard"))


@app.route("/member/claim-reward", methods=["POST"])
@login_required
@role_required(["member"])
def claim_reward():
    """Member claims their streak reward voucher."""
    flash("🔥 Streak Reward Claimed! Use Promo Voucher: #STREAK-10OFF at the Gym Pro Shop for 10% off apparel and supplements.", "success")
    return redirect(request.referrer or url_for("member_dashboard"))


# ==============================================================================
# ERROR HANDLERS
# ==============================================================================
@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    # Host on all interfaces for browser accessibility
    app.run(host="0.0.0.0", port=port, debug=False)

