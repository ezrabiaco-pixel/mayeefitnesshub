"""
MayeeFitness Hub - Temporary In-Memory Storage
Meets Requirement: "Temporary Storage - Use Python Lists only; NO DATABASE."
All persistent state resides in Python lists within the DataStore singleton.
"""

from typing import List, Optional
from datetime import datetime
from models import (
    User, AdminUser, TrainerUser, MemberUser,
    GymClass, EquipmentItem, PaymentRecord,
    WorkoutPlan, FitnessGoal, ChatMessage
)


class DataStore:
    """
    Singleton repository managing temporary in-memory Python lists.
    NO external database engine is used, strictly adhering to assignment rules.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataStore, cls).__new__(cls)
            cls._instance._init_storage()
        return cls._instance

    def _init_storage(self):
        """Initializes empty Python lists and seeds default sample data."""
        # Core storage containers - Python lists only
        self.users: List[User] = []
        self.classes: List[GymClass] = []
        self.equipment: List[EquipmentItem] = []
        self.payments: List[PaymentRecord] = []
        self.workouts: List[WorkoutPlan] = []
        self.goals: List[FitnessGoal] = []
        self.notifications: List[dict] = []
        self.chat_messages: List[ChatMessage] = []

        # Auto-increment ID counters
        self._user_counter = 1
        self._class_counter = 1
        self._equipment_counter = 1
        self._payment_counter = 1
        self._workout_counter = 1
        self._goal_counter = 1
        self._msg_counter = 1

        # Populate with initial mock records
        self._seed_default_data()

    def _seed_default_data(self):
        """Pre-seeds the Python lists to match the exact project UI screenshots."""
        # 1. ADMIN USER
        admin = AdminUser(
            user_id=self._get_next_user_id(),
            name="Mayee Santos",
            email="admin@mayeefitness.com",
            password="admin",
            phone="+63 917 123 4567",
            title="Gym Owner"
        )
        self.users.append(admin)

        # 2. TRAINER USERS
        trainer_dan = TrainerUser(
            user_id=self._get_next_user_id(),
            name="Coach Dan",
            email="dan@mayeefitness.com",
            password="coach",
            phone="+63 918 234 5678",
            specialty="HIIT & Strength",
            bio="Certified CSCS coach with 8 years of strength conditioning experience.",
            rating=4.9
        )
        trainer_liza = TrainerUser(
            user_id=self._get_next_user_id(),
            name="Coach Liza",
            email="liza@mayeefitness.com",
            password="coach",
            phone="+63 919 345 6789",
            specialty="Power Yoga & Mobility",
            bio="Vinyasa certified instructor passionate about posture and functional flexibility.",
            rating=4.9
        )
        trainer_ben = TrainerUser(
            user_id=self._get_next_user_id(),
            name="Coach Ben",
            email="ben@mayeefitness.com",
            password="coach",
            phone="+63 920 456 7890",
            specialty="Strength 101 & Powerlifting",
            bio="Former competitive lifter specializing in form optimization and hyper-growth.",
            rating=4.8
        )
        trainer_rey = TrainerUser(
            user_id=self._get_next_user_id(),
            name="Coach Rey",
            email="rey@mayeefitness.com",
            password="coach",
            phone="+63 921 567 8901",
            specialty="Boxing Fit & Cardio",
            bio="Professional boxing coach with intense conditioning and agility drills.",
            rating=4.9
        )
        self.users.extend([trainer_dan, trainer_liza, trainer_ben, trainer_rey])

        # 3. MEMBER USERS
        # Primary Member: Maya Santos (Featured in Member Dashboard mockup)
        maya = MemberUser(
            user_id=self._get_next_user_id(),
            name="Maya Santos",
            email="maya@mayeefitness.com",
            password="member",
            phone="+63 922 678 9012",
            member_code="#MF-1290",
            plan="Annual",
            trainer_name="Coach Dan",
            expires="Jun 30, 2027",
            status="Active",
            calories=2480,
            workouts_done=5,
            workouts_goal=6,
            weight_kg=58.4,
            visits=18,
            streak_days=12
        )
        # Additional members shown in Admin Dashboard "Recent Members" table
        jerome = MemberUser(
            user_id=self._get_next_user_id(),
            name="Jerome Reyes",
            email="jerome@mayeefitness.com",
            password="member",
            phone="+63 923 789 0123",
            member_code="#MF-1284",
            plan="Annual",
            trainer_name="Coach Dan",
            expires="Oct 2027",
            status="Active",
            calories=3100,
            workouts_done=4,
            workouts_goal=5,
            weight_kg=74.2,
            visits=14,
            streak_days=8
        )
        anna = MemberUser(
            user_id=self._get_next_user_id(),
            name="Anna Cruz",
            email="anna@mayeefitness.com",
            password="member",
            phone="+63 924 890 1234",
            member_code="#MF-1283",
            plan="Monthly",
            trainer_name="Coach Liza",
            expires="Nov 04, 2026",
            status="Active",
            calories=1850,
            workouts_done=3,
            workouts_goal=4,
            weight_kg=52.0,
            visits=11,
            streak_days=5
        )
        marco = MemberUser(
            user_id=self._get_next_user_id(),
            name="Marco Bautista",
            email="marco@mayeefitness.com",
            password="member",
            phone="+63 925 901 2345",
            member_code="#MF-1279",
            plan="Quarterly",
            trainer_name="Coach Dan",
            expires="Oct 12, 2026",
            status="Expiring",
            calories=2200,
            workouts_done=2,
            workouts_goal=4,
            weight_kg=80.5,
            visits=9,
            streak_days=3
        )
        kristine = MemberUser(
            user_id=self._get_next_user_id(),
            name="Kristine Tan",
            email="kristine@mayeefitness.com",
            password="member",
            phone="+63 926 012 3456",
            member_code="#MF-1270",
            plan="Monthly",
            trainer_name="—",
            expires="Sep 28, 2026",
            status="Expired",
            calories=900,
            workouts_done=1,
            workouts_goal=3,
            weight_kg=61.0,
            visits=4,
            streak_days=0
        )
        self.users.extend([maya, jerome, anna, marco, kristine])

        # Link assigned members to trainers
        trainer_dan.assign_member(maya.id)
        trainer_dan.assign_member(jerome.id)
        trainer_dan.assign_member(marco.id)
        trainer_liza.assign_member(anna.id)

        # 4. GYM CLASSES (Shown in Dashboard schedule)
        c1 = GymClass(
            class_id=self._get_next_class_id(),
            title="HIIT Burn",
            trainer="Coach Dan",
            time_slot="6:00 AM",
            day="Wednesday",
            studio="Studio A",
            capacity=20,
            enrolled_count=18
        )
        c2 = GymClass(
            class_id=self._get_next_class_id(),
            title="Power Yoga",
            trainer="Coach Liza",
            time_slot="8:00 AM",
            day="Tuesday",
            studio="Studio B",
            capacity=15,
            enrolled_count=12
        )
        c3 = GymClass(
            class_id=self._get_next_class_id(),
            title="Strength 101",
            trainer="Coach Ben",
            time_slot="5:30 PM",
            day="Monday",
            studio="Main floor",
            capacity=16,
            enrolled_count=9
        )
        c4 = GymClass(
            class_id=self._get_next_class_id(),
            title="Boxing Fit",
            trainer="Coach Rey",
            time_slot="7:00 PM",
            day="Friday",
            studio="Studio A",
            capacity=14,
            enrolled_count=14
        )
        c5 = GymClass(
            class_id=self._get_next_class_id(),
            title="Core & Mobility",
            trainer="Coach Liza",
            time_slot="4:00 PM",
            day="Thursday",
            studio="Studio B",
            capacity=18,
            enrolled_count=11
        )
        self.classes.extend([c1, c2, c3, c4, c5])

        # Maya has booked Power Yoga
        c2.enroll(maya.id)
        maya.book_class(c2.id)

        # 5. EQUIPMENT ITEMS (Shown in Equipment Status widget)
        eq1 = EquipmentItem(self._get_next_equipment_id(), "Treadmills", 14, "All OK", "Cardio")
        eq2 = EquipmentItem(self._get_next_equipment_id(), "Cable machines", 6, "1 service", "Machines")
        eq3 = EquipmentItem(self._get_next_equipment_id(), "Squat racks", 5, "All OK", "Free Weights")
        eq4 = EquipmentItem(self._get_next_equipment_id(), "Dumbbells Set (2-50kg)", 24, "All OK", "Free Weights")
        eq5 = EquipmentItem(self._get_next_equipment_id(), "Bench Press Stations", 8, "All OK", "Free Weights")
        eq6 = EquipmentItem(self._get_next_equipment_id(), "Rowing Machines", 6, "All OK", "Cardio")
        eq7 = EquipmentItem(self._get_next_equipment_id(), "Stair Climbers", 4, "1 service", "Cardio")
        self.equipment.extend([eq1, eq2, eq3, eq4, eq5, eq6, eq7])

        # 6. PAYMENTS (Reflecting monthly revenue ~₱482,500)
        p1 = PaymentRecord(self._get_next_payment_id(), "Jerome Reyes", "#MF-1284", "Annual", 24000.00, "Oct 05, 2026", "GCash")
        p2 = PaymentRecord(self._get_next_payment_id(), "Anna Cruz", "#MF-1283", "Monthly", 2500.00, "Oct 04, 2026", "Credit Card")
        p3 = PaymentRecord(self._get_next_payment_id(), "Maya Santos", "#MF-1290", "Annual", 24000.00, "Jun 30, 2026", "Bank Transfer")
        p4 = PaymentRecord(self._get_next_payment_id(), "Marco Bautista", "#MF-1279", "Quarterly", 6800.00, "Jul 12, 2026", "Cash")
        p5 = PaymentRecord(self._get_next_payment_id(), "Carlos Mendoza", "#MF-1265", "Annual", 24000.00, "Oct 02, 2026", "Credit Card")
        p6 = PaymentRecord(self._get_next_payment_id(), "Patricia Lim", "#MF-1260", "Monthly", 2500.00, "Oct 01, 2026", "GCash")
        self.payments.extend([p1, p2, p3, p4, p5, p6])

        # 7. WORKOUT PLAN FOR MAYA (Shown on Member Dashboard)
        w1 = WorkoutPlan(
            plan_id=self._get_next_workout_id(),
            title="Upper Body Power",
            duration_min=45,
            total_exercises=6,
            completed_exercises=4,
            assigned_by="Coach Dan",
            member_id=maya.id,
            notes="Assigned by Coach Dan. You've completed 4 of 6 — finish strong!"
        )
        self.workouts.append(w1)

        # 8. FITNESS GOALS FOR MAYA (Shown on Member Dashboard)
        g1 = FitnessGoal(self._get_next_goal_id(), maya.id, "Lose 4 kg", 2.4, 4.0, "kg")
        g2 = FitnessGoal(self._get_next_goal_id(), maya.id, "Bench press 50 kg", 41.0, 50.0, "kg")
        g3 = FitnessGoal(self._get_next_goal_id(), maya.id, "20 visits / month", 18.0, 20.0, "visits")
        self.goals.extend([g1, g2, g3])

        # 9. NOTIFICATIONS
        self.notifications = [
            {"id": 1, "icon": "👤", "title": "New Member Registered", "desc": "Jerome Reyes joined with Annual Plan", "time": "10 mins ago", "unread": True},
            {"id": 2, "icon": "🔥", "title": "Class 90% Full", "desc": "HIIT Burn at 6:00 AM has 18/20 enrolled", "time": "25 mins ago", "unread": True},
            {"id": 3, "icon": "⚙️", "title": "Maintenance Reminder", "desc": "Cable machine scheduled for routine inspection", "time": "1 hour ago", "unread": True},
            {"id": 4, "icon": "💳", "title": "Payment Recorded", "desc": "₱24,000 processed via GCash", "time": "3 hours ago", "unread": False},
        ]

        # 10. CHAT MESSAGES BETWEEN COACH DAN AND MAYA
        m1 = ChatMessage(1, trainer_dan.id, "Coach Dan", "trainer", maya.id, "Great form on bench press today! Keep that core tight. 💪", "09:15 AM")
        m2 = ChatMessage(2, maya.id, "Maya Santos", "member", trainer_dan.id, "Thanks Coach! Feeling the burn on that last set.", "09:30 AM")
        m3 = ChatMessage(3, trainer_dan.id, "Coach Dan", "trainer", maya.id, "Remember to hydrate and get plenty of rest tonight!", "02:45 PM")
        self.chat_messages.extend([m1, m2, m3])

    # Internal Counter Helpers
    def _get_next_user_id(self) -> int:
        uid = self._user_counter
        self._user_counter += 1
        return uid

    def _get_next_class_id(self) -> int:
        cid = self._class_counter
        self._class_counter += 1
        return cid

    def _get_next_equipment_id(self) -> int:
        eid = self._equipment_counter
        self._equipment_counter += 1
        return eid

    def _get_next_payment_id(self) -> int:
        pid = self._payment_counter
        self._payment_counter += 1
        return pid

    def _get_next_workout_id(self) -> int:
        wid = self._workout_counter
        self._workout_counter += 1
        return wid

    def _get_next_goal_id(self) -> int:
        gid = self._goal_counter
        self._goal_counter += 1
        return gid

    # ==========================
    # USER CRUD OPERATIONS
    # ==========================
    def get_users(self) -> List[User]:
        return self.users

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        for u in self.users:
            if u.id == user_id:
                return u
        return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        email_clean = email.strip().lower()
        for u in self.users:
            if u.email.lower() == email_clean:
                return u
        return None

    def get_members(self) -> List[MemberUser]:
        return [u for u in self.users if isinstance(u, MemberUser)]

    def get_trainers(self) -> List[TrainerUser]:
        return [u for u in self.users if isinstance(u, TrainerUser)]

    def add_member(self, name: str, email: str, password: str, phone: str = "",
                   plan: str = "Monthly", trainer_name: str = "Unassigned",
                   expires: str = "Oct 2027", status: str = "Active") -> MemberUser:
        """Create and add a new MemberUser to the list."""
        if self.get_user_by_email(email):
            raise ValueError(f"User with email '{email}' already exists.")

        code_num = 1200 + len(self.get_members()) + 1
        member_code = f"#MF-{code_num}"

        member = MemberUser(
            user_id=self._get_next_user_id(),
            name=name,
            email=email,
            password=password,
            phone=phone,
            member_code=member_code,
            plan=plan,
            trainer_name=trainer_name,
            expires=expires,
            status=status
        )
        self.users.append(member)
        return member

    def add_trainer(self, name: str, email: str, password: str, phone: str = "",
                    specialty: str = "General Fitness", bio: str = "") -> TrainerUser:
        """Create and add a new TrainerUser to the list."""
        if self.get_user_by_email(email):
            raise ValueError(f"User with email '{email}' already exists.")

        trainer = TrainerUser(
            user_id=self._get_next_user_id(),
            name=name,
            email=email,
            password=password,
            phone=phone,
            specialty=specialty,
            bio=bio
        )
        self.users.append(trainer)
        return trainer

    def update_member(self, user_id: int, name: str, email: str, phone: str,
                      plan: str, trainer_name: str, expires: str, status: str) -> bool:
        """Update existing MemberUser in the Python list."""
        user = self.get_user_by_id(user_id)
        if not user or not isinstance(user, MemberUser):
            return False

        # Email uniqueness check
        existing = self.get_user_by_email(email)
        if existing and existing.id != user_id:
            raise ValueError(f"Email '{email}' is already taken by another account.")

        user.name = name
        user.email = email
        user.phone = phone
        user.plan = plan
        user.trainer_name = trainer_name
        user.expires = expires
        user.status = status
        return True

    def delete_user(self, user_id: int) -> bool:
        """Remove user from Python list."""
        user = self.get_user_by_id(user_id)
        if user:
            self.users.remove(user)
            return True
        return False

    # ==========================
    # CLASS CRUD OPERATIONS
    # ==========================
    def get_classes(self) -> List[GymClass]:
        return self.classes

    def get_class_by_id(self, class_id: int) -> Optional[GymClass]:
        for c in self.classes:
            if c.id == class_id:
                return c
        return None

    def add_class(self, title: str, trainer: str, time_slot: str,
                  day: str, studio: str, capacity: int) -> GymClass:
        """Add a new GymClass to the list."""
        gym_class = GymClass(
            class_id=self._get_next_class_id(),
            title=title,
            trainer=trainer,
            time_slot=time_slot,
            day=day,
            studio=studio,
            capacity=capacity
        )
        self.classes.append(gym_class)
        return gym_class

    def update_class(self, class_id: int, title: str, trainer: str,
                     time_slot: str, day: str, studio: str, capacity: int) -> bool:
        """Update existing GymClass in the Python list."""
        gym_class = self.get_class_by_id(class_id)
        if not gym_class:
            return False
        gym_class.title = title
        gym_class.trainer = trainer
        gym_class.time_slot = time_slot
        gym_class.day = day
        gym_class.studio = studio
        gym_class.capacity = capacity
        return True

    def delete_class(self, class_id: int) -> bool:
        """Delete GymClass from list."""
        gym_class = self.get_class_by_id(class_id)
        if gym_class:
            self.classes.remove(gym_class)
            return True
        return False

    # ==========================
    # EQUIPMENT CRUD OPERATIONS
    # ==========================
    def get_equipment(self) -> List[EquipmentItem]:
        return self.equipment

    def get_equipment_by_id(self, eq_id: int) -> Optional[EquipmentItem]:
        for eq in self.equipment:
            if eq.id == eq_id:
                return eq
        return None

    def add_equipment(self, name: str, units: int, status: str, category: str) -> EquipmentItem:
        eq = EquipmentItem(
            eq_id=self._get_next_equipment_id(),
            name=name,
            units=units,
            status=status,
            category=category
        )
        self.equipment.append(eq)
        return eq

    def update_equipment(self, eq_id: int, name: str, units: int, status: str, category: str) -> bool:
        eq = self.get_equipment_by_id(eq_id)
        if not eq:
            return False
        eq.name = name
        eq.units = units
        eq.status = status
        eq._category = category
        return True

    def delete_equipment(self, eq_id: int) -> bool:
        eq = self.get_equipment_by_id(eq_id)
        if eq:
            self.equipment.remove(eq)
            return True
        return False

    # ==========================
    # PAYMENT CRUD OPERATIONS
    # ==========================
    def get_payments(self) -> List[PaymentRecord]:
        return self.payments

    def add_payment(self, member_name: str, member_code: str, plan: str,
                    amount: float, method: str = "GCash") -> PaymentRecord:
        record = PaymentRecord(
            pay_id=self._get_next_payment_id(),
            member_name=member_name,
            member_code=member_code,
            plan=plan,
            amount=amount,
            date=datetime.now().strftime("%b %d, %Y"),
            method=method,
            status="Completed"
        )
        self.payments.insert(0, record)
        return record

    def get_total_revenue(self) -> float:
        return sum(p.amount for p in self.payments)

    # ==========================
    # WORKOUT & GOAL OPERATIONS
    # ==========================
    def get_workout_for_member(self, member_id: int) -> Optional[WorkoutPlan]:
        for w in self.workouts:
            if w.member_id == member_id:
                return w
        # Fallback to general workout if not specifically assigned
        return self.workouts[0] if self.workouts else None

    def add_workout_plan(self, member_id: int, title: str, duration_min: int,
                         assigned_by: str, notes: str = "") -> WorkoutPlan:
        w = WorkoutPlan(
            plan_id=self._get_next_workout_id(),
            title=title,
            duration_min=duration_min,
            total_exercises=6,
            completed_exercises=0,
            assigned_by=assigned_by,
            member_id=member_id,
            notes=notes
        )
        self.workouts.append(w)
        return w

    def get_goals_for_member(self, member_id: int) -> List[FitnessGoal]:
        member_goals = [g for g in self.goals if g.member_id == member_id]
        if not member_goals and self.goals:
            # Return demo goals if newly created member
            return self.goals[:3]
        return member_goals

    def update_goal(self, goal_id: int, current_val: float, target_val: float) -> bool:
        for g in self.goals:
            if g.id == goal_id:
                g.current_val = current_val
                g.target_val = target_val
                return True
        return False

    def add_goal(self, member_id: int, title: str, current_val: float, target_val: float, unit: str = "kg") -> FitnessGoal:
        goal = FitnessGoal(self._get_next_goal_id(), member_id, title, current_val, target_val, unit)
        self.goals.append(goal)
        return goal

    def delete_goal(self, goal_id: int) -> bool:
        for g in self.goals:
            if g.id == goal_id:
                self.goals.remove(g)
                return True
        return False

    # ==========================
    # CHAT OPERATIONS
    # ==========================
    def add_chat_message(self, sender_id: int, sender_name: str, sender_role: str,
                         recipient_id: int, message: str) -> ChatMessage:
        mid = self._msg_counter
        self._msg_counter += 1
        msg = ChatMessage(mid, sender_id, sender_name, sender_role, recipient_id, message)
        self.chat_messages.append(msg)
        return msg

    def get_chat_history(self, user_id1: int, user_id2: int) -> List[ChatMessage]:
        return [
            m for m in self.chat_messages
            if (m.sender_id == user_id1 and m.recipient_id == user_id2) or
               (m.sender_id == user_id2 and m.recipient_id == user_id1)
        ]

    def get_chat_for_user(self, user_id: int) -> List[ChatMessage]:
        return [m for m in self.chat_messages if m.sender_id == user_id or m.recipient_id == user_id]

    # ==========================
    # NOTIFICATION OPERATIONS
    # ==========================
    def get_notifications(self) -> List[dict]:
        return self.notifications

    def add_notification(self, icon: str, title: str, desc: str):
        nid = len(self.notifications) + 1
        self.notifications.insert(0, {
            "id": nid,
            "icon": icon,
            "title": title,
            "desc": desc,
            "time": "Just now",
            "unread": True
        })

    def mark_notifications_read(self):
        for n in self.notifications:
            n["unread"] = False

    def clear_notifications(self):
        self.notifications.clear()

