/**
 * MayeeFitness Hub - Interactive Front-end JavaScript
 * Handles modals, quick actions, role tab switching, live filters, and demo logins.
 */

document.addEventListener("DOMContentLoaded", function () {
  // 1. Password Visibility Toggle
  const togglePassBtns = document.querySelectorAll(".auth-input-toggle-pw");
  togglePassBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      const input = this.parentElement.querySelector("input");
      if (input.type === "password") {
        input.type = "text";
        this.innerHTML = "👁️";
      } else {
        input.type = "password";
        this.innerHTML = "🔒";
      }
    });
  });

  // 2. Login Role Tab Switcher (Image 3)
  const rolePills = document.querySelectorAll(".role-pill-btn");
  const roleInput = document.getElementById("selectedRoleTab");
  const emailInput = document.getElementById("loginEmail");
  const passwordInput = document.getElementById("loginPassword");

  if (rolePills.length > 0 && roleInput) {
    rolePills.forEach((pill) => {
      pill.addEventListener("click", function () {
        rolePills.forEach((p) => p.classList.remove("active"));
        this.classList.add("active");
        const role = this.getAttribute("data-role");
        roleInput.value = role;

        // Auto-fill demo credentials for convenience
        if (role === "admin") {
          emailInput.value = "admin@mayeefitness.com";
          passwordInput.value = "admin";
        } else if (role === "trainer") {
          emailInput.value = "dan@mayeefitness.com";
          passwordInput.value = "coach";
        } else {
          emailInput.value = "maya@mayeefitness.com";
          passwordInput.value = "member";
        }
      });
    });
  }

  // 3. Quick Demo Chips on Login
  const demoChips = document.querySelectorAll(".demo-chip");
  demoChips.forEach((chip) => {
    chip.addEventListener("click", function () {
      const email = this.getAttribute("data-email");
      const pass = this.getAttribute("data-pass");
      const role = this.getAttribute("data-role");

      if (emailInput && passwordInput) {
        emailInput.value = email;
        passwordInput.value = pass;
      }
      if (roleInput) {
        roleInput.value = role;
      }
      rolePills.forEach((p) => {
        if (p.getAttribute("data-role") === role) {
          p.classList.add("active");
        } else {
          p.classList.remove("active");
        }
      });
    });
  });

  // 4. Modal Dialog Controller
  window.openModal = function (modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.classList.add("open");
    }
  };

  window.closeModal = function (modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.classList.remove("open");
    }
  };

  // Close modal when clicking outside content
  document.querySelectorAll(".modal-overlay").forEach((modal) => {
    modal.addEventListener("click", function (e) {
      if (e.target === this) {
        this.classList.remove("open");
      }
    });
  });

  // 5. Populate Edit Member Modal
  window.openEditMemberModal = function (id, name, email, phone, plan, trainer, expires, status) {
    const form = document.getElementById("editMemberForm");
    if (form) {
      form.action = `/members/edit/${id}`;
      document.getElementById("editMemberName").value = name;
      document.getElementById("editMemberEmail").value = email;
      document.getElementById("editMemberPhone").value = phone;
      document.getElementById("editMemberPlan").value = plan;
      document.getElementById("editMemberTrainer").value = trainer;
      document.getElementById("editMemberExpires").value = expires;
      document.getElementById("editMemberStatus").value = status;
      openModal("editMemberModal");
    }
  };

  // 6. Populate Edit Class Modal
  window.openEditClassModal = function (id, title, trainer, timeSlot, day, studio, capacity) {
    const form = document.getElementById("editClassForm");
    if (form) {
      form.action = `/classes/edit/${id}`;
      document.getElementById("editClassTitle").value = title;
      document.getElementById("editClassTrainer").value = trainer;
      document.getElementById("editClassTime").value = timeSlot;
      document.getElementById("editClassDay").value = day;
      document.getElementById("editClassStudio").value = studio;
      document.getElementById("editClassCapacity").value = capacity;
      openModal("editClassModal");
    }
  };

  // 7. Populate Edit Equipment Modal
  window.openEditEquipmentModal = function (id, name, units, status, category) {
    const form = document.getElementById("editEquipmentForm");
    if (form) {
      form.action = `/equipment/edit/${id}`;
      document.getElementById("editEqName").value = name;
      document.getElementById("editEqUnits").value = units;
      document.getElementById("editEqStatus").value = status;
      document.getElementById("editEqCategory").value = category;
      openModal("editEquipmentModal");
    }
  };

  // 8. Populate Edit Goal Modal
  window.openEditGoalModal = function (id, title, currentVal, targetVal) {
    const form = document.getElementById("editGoalForm");
    if (form) {
      form.action = `/goals/update/${id}`;
      document.getElementById("editGoalTitle").innerText = title;
      document.getElementById("editGoalCurrent").value = currentVal;
      document.getElementById("editGoalTarget").value = targetVal;
      openModal("editGoalModal");
    }
  };

  // 9. Client-side Real-time Search Filter for Tables
  const tableSearch = document.getElementById("clientTableSearch");
  if (tableSearch) {
    tableSearch.addEventListener("keyup", function () {
      const term = this.value.toLowerCase();
      const rows = document.querySelectorAll(".filterable-row");
      rows.forEach((row) => {
        const text = row.innerText.toLowerCase();
        if (text.includes(term)) {
          row.style.display = "";
        } else {
          row.style.display = "none";
        }
      });
    });
  }
});
