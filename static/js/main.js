// ============================================================
//  IncluCV — main.js
//  Handles: multi-step form, progress sidebar, print prep
// ============================================================

// ── Multi-step form navigation ───────────────────────────────

const sectionOrder = ['personal', 'disability', 'professional', 'experience', 'education'];

/**
 * Move to the next form section.
 * @param {string} currentId - the section we're leaving
 * @param {string} nextId    - the section we're going to
 */
function nextSection(currentId, nextId) {
  // Basic validation: check required fields in the current section
  const currentSection = document.getElementById('section-' + currentId);
  const requiredFields = currentSection.querySelectorAll('[required]');
  let allFilled = true;

  requiredFields.forEach(field => {
    if (!field.value.trim()) {
      field.style.borderColor = '#e05252';
      field.focus();
      allFilled = false;
    } else {
      field.style.borderColor = '';
    }
  });

  if (!allFilled) {
    showToast('Please fill in all required fields before continuing.');
    return;
  }

  // Hide current section
  currentSection.classList.remove('active');

  // Show next section
  const nextSection = document.getElementById('section-' + nextId);
  nextSection.classList.add('active');

  // Update sidebar
  updateSidebar(currentId, nextId);

  // Scroll to top of form
  nextSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Go back to the previous section.
 */
function prevSection(currentId, prevId) {
  document.getElementById('section-' + currentId).classList.remove('active');
  document.getElementById('section-' + prevId).classList.add('active');
  updateSidebar(null, prevId);
  document.getElementById('section-' + prevId).scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Update the left sidebar progress indicator.
 */
function updateSidebar(doneId, activeId) {
  if (doneId) {
    const doneItem = document.querySelector(`.prog-item[data-section="${doneId}"]`);
    if (doneItem) {
      doneItem.classList.remove('active');
      doneItem.classList.add('done');
    }
  }

  document.querySelectorAll('.prog-item').forEach(item => item.classList.remove('active'));

  const activeItem = document.querySelector(`.prog-item[data-section="${activeId}"]`);
  if (activeItem) activeItem.classList.add('active');
}

// ── Toast notification ───────────────────────────────────────

function showToast(message) {
  // Remove existing toast if any
  const existing = document.getElementById('toast');
  if (existing) existing.remove();

  const toast = document.createElement('div');
  toast.id = 'toast';
  toast.textContent = message;
  toast.style.cssText = `
    position: fixed;
    bottom: 2rem;
    left: 50%;
    transform: translateX(-50%);
    background: #e05252;
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 999px;
    font-size: 0.88rem;
    font-weight: 500;
    z-index: 9999;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    animation: slideUp 0.25s ease;
  `;

  document.body.appendChild(toast);

  // Auto remove after 3 seconds
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.3s';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

// ── Loading state on form submit ─────────────────────────────

const form = document.getElementById('resumeForm');
if (form) {
  form.addEventListener('submit', function () {
    const btn = form.querySelector('.btn-generate');
    if (btn) {
      btn.textContent = '⏳ Generating your documents...';
      btn.disabled = true;
      btn.style.opacity = '0.7';
    }
  });
}

// ── Result page: checkbox interactions ───────────────────────

document.querySelectorAll('.check-item input[type="checkbox"]').forEach(checkbox => {
  checkbox.addEventListener('change', function () {
    const label = this.closest('.check-item');
    if (this.checked) {
      label.style.textDecoration = 'line-through';
      label.style.opacity = '0.5';
    } else {
      label.style.textDecoration = '';
      label.style.opacity = '';
    }
  });
});

// ── Print: make guide readable ───────────────────────────────

window.addEventListener('beforeprint', function () {
  // Already handled by CSS @media print — nothing extra needed
  console.log('Printing IncluCV documents...');
});

// ── Sidebar click to jump sections (builder page only) ───────

document.querySelectorAll('.prog-item').forEach(item => {
  item.addEventListener('click', function () {
    // Only allow jumping to completed (done) sections
    if (this.classList.contains('done')) {
      const targetId = this.dataset.section;
      document.querySelectorAll('.form-section').forEach(s => s.classList.remove('active'));
      document.getElementById('section-' + targetId).classList.add('active');
      document.querySelectorAll('.prog-item').forEach(p => p.classList.remove('active'));
      this.classList.add('active');
    }
  });
});