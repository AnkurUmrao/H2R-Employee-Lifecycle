// SAP H2R Portal — UI JavaScript

// Auto-dismiss flash messages after 4s
document.addEventListener("DOMContentLoaded", () => {
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.transition = "opacity 0.4s";
      alert.style.opacity = "0";
      setTimeout(() => alert.remove(), 400);
    }, 4000);
  });

  // Leave date validation: end >= start
  const startDate = document.querySelector("input[name='start_date']");
  const endDate   = document.querySelector("input[name='end_date']");
  if (startDate && endDate) {
    startDate.addEventListener("change", () => {
      if (endDate.value && endDate.value < startDate.value) {
        endDate.value = startDate.value;
      }
      endDate.min = startDate.value;
    });
  }

  // Animate KPI values
  document.querySelectorAll(".kpi-value").forEach(el => {
    el.style.opacity = "0";
    el.style.transform = "translateY(10px)";
    el.style.transition = "opacity 0.4s, transform 0.4s";
    setTimeout(() => {
      el.style.opacity = "1";
      el.style.transform = "translateY(0)";
    }, 100);
  });
});
