// JavaScript für Versicherungsmakler Finder - Enhanced Version 2.7 (Ultra-Schnelle Loader)
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Versicherungsmakler Finder v2.7 - Ultra-Schnelle Loader');
    
    // Verhindere mehrfache Initialisierung
    if (window.appInitialized) {
        console.log('ℹ️ App bereits initialisiert, überspringe...');
        return;
    }
    window.appInitialized = true;
    
    // Moderne Page Loader mit Emergency Fallback - nur einmal
    initializePageLoader();
    
    // Debug: Check if loader still exists after initialization (verkürzt)
    setTimeout(() => {
        const loader = document.querySelector('.page-loader');
        const transitionOverlay = document.querySelector('.transition-overlay');
        
        if (loader) {
            console.warn('⚠️ Page loader still exists after 1.5 seconds! Force removing...');
            loader.style.opacity = '0';
            loader.style.visibility = 'hidden';
            setTimeout(() => {
                if (loader.parentNode) {
                    loader.remove();
                    console.log('✅ Emergency loader removal successful');
                }
            }, 200);
        }
        
        if (transitionOverlay) {
            console.warn('⚠️ Transition overlay still exists after 1.5 seconds! Force removing...');
            transitionOverlay.style.opacity = '0';
            transitionOverlay.style.visibility = 'hidden';
            setTimeout(() => {
                if (transitionOverlay.parentNode) {
                    transitionOverlay.remove();
                    console.log('✅ Emergency transition overlay removal successful');
                }
            }, 200);
        }
        
        if (!loader && !transitionOverlay) {
            console.log('✅ All loading overlays properly handled');
        }
    }, 1500);
    
    // Additional emergency cleanup after 3 seconds (verkürzt)
    setTimeout(() => {
        const allOverlays = document.querySelectorAll('.page-loader, .transition-overlay, .theme-switch-overlay');
        if (allOverlays.length > 0) {
            console.warn('🚨 Found stuck overlays after 3 seconds, force cleaning:', allOverlays.length);
            allOverlays.forEach(overlay => {
                if (overlay.parentNode) {
                    overlay.remove();
                }
            });
            console.log('🧹 Emergency cleanup completed');
        } else {
            console.log('✨ No stuck overlays found - clean state');
        }
    }, 3000);
    
    // Smooth page enter animation
    initializePageEnterAnimation();
    
    // Animation Delays für Karten setzen
    const brokerCards = document.querySelectorAll('.broker-card');
    brokerCards.forEach((card, index) => {
        card.style.setProperty('--animation-order', index);
        card.classList.add('gpu-accelerated');
    });
    
    // Tooltip für bessere UX
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Enhanced Form Validation
    initializeFormValidation();
    
    // Smooth Scrolling für interne Links
    initializeSmoothScrolling();
    
    // Auto-dismiss Alerts nach 5 Sekunden
    initializeAutoAlerts();
    
    // Search Progress Tracking
    initializeSearchProgress();
    
    // Intersection Observer für Performance
    initializeIntersectionObserver();
    
    // Keyboard Shortcuts
    initializeKeyboardShortcuts();
    
    // Service Worker für Offline-Fähigkeiten
    if ('serviceWorker' in navigator) {
        registerServiceWorker();
    }
});

// Page Loader Management - Only on first visit
function initializePageLoader() {
    // Verhindere mehrfache Loader-Initialisierung
    if (window.pageLoaderInitialized) {
        console.log('ℹ️ Page Loader bereits initialisiert, überspringe...');
        return;
    }
    window.pageLoaderInitialized = true;
    
    const loader = document.querySelector('.page-loader');
    if (loader) {
        console.log('🔄 Page Loader gefunden, initialisiere...');
        
        // Check if this is the first visit to the site
        const hasVisitedBefore = sessionStorage.getItem('vmf_visited');
        
        if (!hasVisitedBefore) {
            // First visit - show loader
            console.log('👋 Erster Besuch - zeige Loader');
            sessionStorage.setItem('vmf_visited', 'true');
            
            // Multiple strategies to hide the loader
            let loaderHidden = false;
            
            function hideLoader() {
                if (loaderHidden) return;
                loaderHidden = true;
                
                console.log('Hiding page loader...');
                loader.classList.add('hide');
                setTimeout(() => {
                    if (loader.parentNode) {
                        loader.remove();
                    }
                }, 500);
            }
            
            // Strategy 1: Hide after window load event (ultra-schnell)
            window.addEventListener('load', () => {
                setTimeout(hideLoader, 150);
            });
            
            // Strategy 2: Fallback - hide after DOMContentLoaded + timeout (ultra-schnell)
            if (document.readyState === 'complete') {
                // Page already loaded
                setTimeout(hideLoader, 100);
            } else {
                document.addEventListener('DOMContentLoaded', () => {
                    setTimeout(hideLoader, 200);
                });
            }
            
            // Strategy 3: Emergency fallback - force hide after 5 seconds
            setTimeout(() => {
                if (!loaderHidden) {
                    console.log('Force hiding loader (emergency fallback)');
                    hideLoader();
                }
            }, 5000);
            
        } else {
            // Not first visit - remove loader immediately
            console.log('Removing loader (not first visit)');
            loader.remove();
        }
    }
    
    // Initialize smooth page transitions
    initializePageTransitions();
}

// Smooth page enter animation
function initializePageEnterAnimation() {
    const main = document.querySelector('main');
    if (main) {
        // Check if coming from another page via smooth transition
        const hasVisitedBefore = sessionStorage.getItem('vmf_visited');
        
        if (hasVisitedBefore) {
            // Animate page enter
            main.style.opacity = '0';
            main.style.transform = 'translateY(20px)';
            
            // Smooth enter after short delay
            setTimeout(() => {
                main.style.opacity = '1';
                main.style.transform = 'translateY(0)';
            }, 50);
        }
    }
}

// Smooth Page Transitions
function initializePageTransitions() {
    // Add transition wrapper to main content
    const main = document.querySelector('main');
    if (main) {
        main.style.transition = 'opacity 0.3s ease-in-out, transform 0.3s ease-in-out';
        main.style.transform = 'translateY(0)';
        main.style.opacity = '1';
    }
    
    // Create transition overlay
    createTransitionOverlay();
    
    // Handle navbar link clicks
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link:not(.dropdown-toggle), .navbar-brand');
    navLinks.forEach(link => {
        // Skip external links and anchors
        if (link.href && !link.href.includes('#') && link.hostname === window.location.hostname) {
            link.addEventListener('click', function(e) {
                // Only handle if it's a different page
                if (this.href !== window.location.href) {
                    e.preventDefault();
                    smoothPageTransition(this.href);
                }
            });
        }
    });
}

// Create transition overlay element
function createTransitionOverlay() {
    // Remove any existing overlays first
    const existingOverlay = document.querySelector('.transition-overlay');
    if (existingOverlay) {
        existingOverlay.remove();
    }
    
    const overlay = document.createElement('div');
    overlay.className = 'transition-overlay';
    overlay.innerHTML = `
        <div class="transition-loader">
            <div class="transition-spinner"></div>
            <div class="transition-text">Seite wird geladen...</div>
        </div>
    `;
    document.body.appendChild(overlay);
    
    // Auto-remove overlay after 5 seconds as emergency fallback
    setTimeout(() => {
        if (overlay.parentNode) {
            console.log('🚨 Emergency: Force removing stuck transition overlay');
            overlay.remove();
        }
    }, 5000);
}

// Execute smooth transition to new page
function smoothPageTransition(url) {
    const main = document.querySelector('main');
    
    createTransitionOverlay();
    const overlay = document.querySelector('.transition-overlay');
    
    if (main && overlay) {
        // Show overlay
        overlay.classList.add('active');
        
        // Fade out current content
        main.style.opacity = '0';
        main.style.transform = 'translateY(-10px)';
        
        // Navigate after short delay
        setTimeout(() => {
            window.location.href = url;
        }, 150);
    } else {
        // Fallback: direct navigation
        window.location.href = url;
    }
}

// Enhanced Form Validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        // Real-time validation
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', Utils.debounce(function() {
                if (this.classList.contains('is-invalid') || this.classList.contains('is-valid')) {
                    validateField(this);
                }
            }, 300));
        });
        
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            
            let isValid = true;
            inputs.forEach(input => {
                if (!validateField(input)) {
                    isValid = false;
                }
            });
            
            if (isValid) {
                handleFormSubmission(this);
            } else {
                // Scroll to first error
                const firstError = form.querySelector('.is-invalid');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstError.focus();
                }
            }
        });
    });
}

function validateField(field) {
    const isValid = field.checkValidity();
    
    // Custom validation rules
    if (field.name === 'location') {
        const value = field.value.trim();
        // German postal code or city validation
        if (value && !Utils.isValidGermanPostalCode(value) && value.length < 2) {
            field.setCustomValidity('Bitte geben Sie eine gültige Postleitzahl (5 Ziffern) oder einen Ortsnamen ein.');
            field.classList.add('is-invalid');
            field.classList.remove('is-valid');
            return false;
        } else {
            field.setCustomValidity('');
        }
    }
    
    if (isValid && field.value.trim() !== '') {
        field.classList.add('is-valid');
        field.classList.remove('is-invalid');
    } else {
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');
    }
    
    return isValid;
}

function handleFormSubmission(form) {
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    
    // Show loading state
    Utils.setButtonLoading(submitBtn, true);
    
    // Show progress bar
    showSearchProgress();
    
    // Submit form after brief delay for UX
    setTimeout(() => {
        form.submit();
    }, 500);
}

// Smooth Scrolling
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Auto-dismiss Alerts
function initializeAutoAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        // Add dismiss animation
        setTimeout(() => {
            if (alert.classList.contains('show')) {
                alert.style.animation = 'slideInRight 0.3s ease-out reverse';
                setTimeout(() => {
                    if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
                        const bsAlert = new bootstrap.Alert(alert);
                        bsAlert.close();
                    }
                }, 300);
            }
        }, 5000);
    });
}

// Search Progress Tracking
function initializeSearchProgress() {
    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', function() {
            showSearchProgress();
        });
    }
}

function showSearchProgress() {
    const progressHTML = `
        <div id="searchProgress" class="search-progress">
            <div class="progress mb-3">
                <div class="progress-bar progress-bar-striped progress-bar-animated" 
                     role="progressbar" style="width: 0%"></div>
            </div>
            <div class="progress-text">Suche wird gestartet...</div>
        </div>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertAdjacentHTML('afterbegin', progressHTML);
        animateSearchProgress();
    }
}

function animateSearchProgress() {
    const progressBar = document.querySelector('#searchProgress .progress-bar');
    const progressText = document.querySelector('#searchProgress .progress-text');
    
    if (!progressBar || !progressText) return;
    
    const steps = [
        { progress: 20, text: 'Standort wird ermittelt...' },
        { progress: 40, text: 'Google Maps API wird abgefragt...' },
        { progress: 60, text: 'Versicherungsmakler werden gesucht...' },
        { progress: 80, text: 'Zusätzliche Details werden geladen...' },
        { progress: 95, text: 'Ergebnisse werden aufbereitet...' }
    ];
    
    let currentStep = 0;
    
    const interval = setInterval(() => {
        if (currentStep < steps.length) {
            const step = steps[currentStep];
            progressBar.style.width = step.progress + '%';
            progressText.textContent = step.text;
            currentStep++;
        } else {
            progressBar.style.width = '100%';
            progressText.textContent = 'Suche abgeschlossen!';
            clearInterval(interval);
        }
    }, 800);
}

// Intersection Observer für Performance
function initializeIntersectionObserver() {
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            rootMargin: '50px',
            threshold: 0.1
        });
        
        // Observe cards that are initially out of view
        document.querySelectorAll('.broker-card').forEach(card => {
            observer.observe(card);
        });
    }
}

// Keyboard Shortcuts
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // ESC: Close modals and dropdowns
        if (e.key === 'Escape') {
            closeAllModalsAndDropdowns();
        }
        
        // Ctrl+K: Focus search
        if (e.ctrlKey && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('#location, input[name="location"]');
            if (searchInput) {
                searchInput.focus();
                searchInput.select();
                Utils.showToast('Suchfeld fokussiert - Ctrl+K', 'info');
            }
        }
        
        // Ctrl+E: Export Excel
        if (e.ctrlKey && e.key === 'e') {
            e.preventDefault();
            exportToExcel();
        }
        
        // Ctrl+J: Export JSON
        if (e.ctrlKey && e.key === 'j') {
            e.preventDefault();
            exportToJson();
        }
        
        // Ctrl+A: Select all brokers (on results page)
        if (e.ctrlKey && e.key === 'a' && document.querySelectorAll('.broker-card').length > 0) {
            e.preventDefault();
            toggleAllBrokerSelection();
        }
    });
}

function closeAllModalsAndDropdowns() {
    // Close Bootstrap modals
    const openModals = document.querySelectorAll('.modal.show');
    openModals.forEach(modal => {
        const bsModal = bootstrap.Modal.getInstance(modal);
        if (bsModal) bsModal.hide();
    });
    
    // Close dropdowns
    const openDropdowns = document.querySelectorAll('.dropdown-menu.show');
    openDropdowns.forEach(dropdown => {
        dropdown.classList.remove('show');
    });
}

// Service Worker Registration
async function registerServiceWorker() {
    try {
        const registration = await navigator.serviceWorker.register('/sw.js');
        console.log('Service Worker registriert:', registration);
    } catch (error) {
        console.log('Service Worker Registrierung fehlgeschlagen:', error);
    }
}

// Enhanced Utility Functions
const Utils = {
    // Debounce function with improved performance
    debounce: function(func, wait, immediate) {
        let timeout;
        return function executedFunction() {
            const context = this;
            const args = arguments;
            const later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    },
    
    // Throttle function for scroll events
    throttle: function(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    },
    
    // Enhanced loading state for buttons
    setButtonLoading: function(button, loading = true) {
        if (loading) {
            button.dataset.originalText = button.innerHTML;
            button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Wird geladen...';
            button.disabled = true;
            button.classList.add('btn-loading');
        } else {
            button.innerHTML = button.dataset.originalText || button.innerHTML;
            button.disabled = false;
            button.classList.remove('btn-loading');
        }
    },
    
    // Enhanced toast with different positions
    showToast: function(message, type = 'info', position = 'bottom-end') {
        const toastContainer = document.getElementById('toast-container') || this.createToastContainer(position);
        
        const icons = {
            'success': 'check-circle',
            'error': 'exclamation-triangle',
            'warning': 'exclamation-circle',
            'info': 'info-circle'
        };
        
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : type} border-0 show`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-${icons[type] || 'info-circle'} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        toastContainer.appendChild(toast);
        
        if (typeof bootstrap !== 'undefined' && bootstrap.Toast) {
            const bsToast = new bootstrap.Toast(toast, {
                autohide: true,
                delay: 5000
            });
            bsToast.show();
        }
        
        // Auto-remove after animation
        setTimeout(() => {
            if (toast.parentNode) {
                toast.style.animation = 'slideInRight 0.3s ease-out reverse';
                setTimeout(() => toast.remove(), 300);
            }
        }, 5000);
    },
    
    createToastContainer: function(position = 'bottom-end') {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = `toast-container position-fixed ${position.replace('-', '-0 ')} p-3`;
        container.style.zIndex = '9999';
        document.body.appendChild(container);
        return container;
    },
    
    // Enhanced localStorage with compression
    storage: {
        set: function(key, value, compress = false) {
            try {
                let dataToStore = JSON.stringify(value);
                if (compress && typeof LZString !== 'undefined') {
                    dataToStore = LZString.compress(dataToStore);
                }
                localStorage.setItem(key, dataToStore);
                return true;
            } catch (e) {
                console.warn('LocalStorage nicht verfügbar:', e);
                return false;
            }
        },
        
        get: function(key, compressed = false) {
            try {
                let value = localStorage.getItem(key);
                if (value) {
                    if (compressed && typeof LZString !== 'undefined') {
                        value = LZString.decompress(value);
                    }
                    return JSON.parse(value);
                }
                return null;
            } catch (e) {
                console.warn('LocalStorage Fehler:', e);
                return null;
            }
        },
        
        remove: function(key) {
            try {
                localStorage.removeItem(key);
                return true;
            } catch (e) {
                console.warn('LocalStorage Fehler:', e);
                return false;
            }
        },
        
        clear: function() {
            try {
                localStorage.clear();
                return true;
            } catch (e) {
                console.warn('LocalStorage Fehler:', e);
                return false;
            }
        }
    },
    
    // Enhanced form data helper
    getFormData: function(form) {
        const formData = new FormData(form);
        const data = {};
        for (let [key, value] of formData.entries()) {
            if (data[key]) {
                if (Array.isArray(data[key])) {
                    data[key].push(value);
                } else {
                    data[key] = [data[key], value];
                }
            } else {
                data[key] = value;
            }
        }
        return data;
    },
    
    // Enhanced German postal code validation
    isValidGermanPostalCode: function(postalCode) {
        return /^[0-9]{5}$/.test(postalCode.trim());
    },
    
    // Enhanced phone number formatting
    formatPhoneNumber: function(phone) {
        // German phone number formatting
        const cleaned = phone.replace(/[^\d\+]/g, '');
        if (cleaned.startsWith('+49')) {
            return cleaned.replace('+49', '+49 ').replace(/(\d{3,4})(\d{3,4})/, '$1 $2');
        }
        return cleaned;
    },
    
    // Enhanced clipboard functionality
    async copyToClipboard(text) {
        try {
            if (navigator.clipboard && navigator.clipboard.writeText) {
                await navigator.clipboard.writeText(text);
                this.showToast('In Zwischenablage kopiert', 'success');
                return true;
            } else {
                // Fallback für ältere Browser
                const textArea = document.createElement('textarea');
                textArea.value = text;
                textArea.style.position = 'fixed';
                textArea.style.opacity = '0';
                textArea.style.pointerEvents = 'none';
                document.body.appendChild(textArea);
                textArea.focus();
                textArea.select();
                
                const success = document.execCommand('copy');
                document.body.removeChild(textArea);
                
                if (success) {
                    this.showToast('In Zwischenablage kopiert', 'success');
                }
                return success;
            }
        } catch (err) {
            console.error('Clipboard error:', err);
            this.showToast('Fehler beim Kopieren', 'error');
            return false;
        }
    },
    
    // Animate number counting
    animateNumber: function(element, start, end, duration = 1000) {
        const range = end - start;
        const startTime = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function (ease-out)
            const easedProgress = 1 - Math.pow(1 - progress, 3);
            const current = Math.round(start + (range * easedProgress));
            
            element.textContent = current.toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        requestAnimationFrame(animate);
    },
    
    // Format file size
    formatFileSize: function(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    
    // Generate unique ID
    generateId: function() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }
};

// Enhanced API Client
const APIClient = {
    baseURL: '',
    defaultTimeout: 10000,
    
    async request(url, options = {}) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.defaultTimeout);
        
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            signal: controller.signal
        };
        
        const config = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers
            }
        };
        
        try {
            const response = await fetch(url, config);
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                throw new Error(`HTTP Error: ${response.status} ${response.statusText}`);
            }
            
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            } else {
                return await response.text();
            }
        } catch (error) {
            clearTimeout(timeoutId);
            if (error.name === 'AbortError') {
                throw new Error('Request timeout');
            }
            console.error('API Request Error:', error);
            throw error;
        }
    },
    
    get(url, options = {}) {
        return this.request(url, { ...options, method: 'GET' });
    },
    
    post(url, data, options = {}) {
        return this.request(url, {
            ...options,
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    put(url, data, options = {}) {
        return this.request(url, {
            ...options,
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    
    delete(url, options = {}) {
        return this.request(url, { ...options, method: 'DELETE' });
    }
};

// Enhanced Export Functions
function exportToExcel() {
    const exportBtn = document.querySelector('[onclick*="exportToExcel"], .btn-excel');
    if (exportBtn) {
        Utils.setButtonLoading(exportBtn, true);
    }
    
    window.location.href = '/export/excel';
    
    setTimeout(() => {
        if (exportBtn) {
            Utils.setButtonLoading(exportBtn, false);
        }
        Utils.showToast('Excel-Export wurde gestartet', 'success');
    }, 1000);
}

function exportToJson() {
    const exportBtn = document.querySelector('[onclick*="exportToJson"], .btn-json');
    if (exportBtn) {
        Utils.setButtonLoading(exportBtn, true);
    }
    
    window.location.href = '/export/json';
    
    setTimeout(() => {
        if (exportBtn) {
            Utils.setButtonLoading(exportBtn, false);
        }
        Utils.showToast('JSON-Export wurde gestartet', 'success');
    }, 1000);
}

// Broker Selection Management
function toggleAllBrokerSelection() {
    const checkboxes = document.querySelectorAll('.broker-checkbox');
    const allChecked = Array.from(checkboxes).every(cb => cb.checked);
    
    checkboxes.forEach(checkbox => {
        checkbox.checked = !allChecked;
        highlightBrokerCard(checkbox);
    });
    
    Utils.showToast(`Alle Makler ${allChecked ? 'abgewählt' : 'ausgewählt'}`, 'info');
}

function highlightBrokerCard(checkbox) {
    const card = checkbox.closest('.broker-card');
    if (card) {
        if (checkbox.checked) {
            card.classList.add('border-primary', 'shadow-strong');
        } else {
            card.classList.remove('border-primary', 'shadow-strong');
        }
    }
}

// Performance Monitoring
const PerformanceMonitor = {
    init: function() {
        if ('performance' in window) {
            window.addEventListener('load', () => {
                setTimeout(() => this.logPageLoadTime(), 100);
            });
            
            // Monitor long tasks
            if ('PerformanceObserver' in window) {
                this.observeLongTasks();
            }
        }
    },
    
    logPageLoadTime: function() {
        const perfData = performance.getEntriesByType('navigation')[0];
        if (perfData && perfData.loadEventEnd > 0 && perfData.fetchStart > 0) {
            const loadTime = Math.round(perfData.loadEventEnd - perfData.fetchStart);
            
            // Nur positive Werte anzeigen
            if (loadTime > 0) {
                console.log(`🚀 Seitenladezeit: ${loadTime}ms`);
                
                // Visual feedback for fast loading (nur einmalig)
                if (loadTime < 2000 && !window.loadTimeToastShown) {
                    window.loadTimeToastShown = true;
                    Utils.showToast(`Schnelle Ladezeit: ${loadTime}ms`, 'success');
                }
            } else {
                console.log('🚀 Seite geladen (Ladezeit noch nicht verfügbar)');
            }
        }
    },
    
    observeLongTasks: function() {
        try {
            const observer = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    if (entry.duration > 50) {
                        console.warn(`⚠️ Long task detected: ${Math.round(entry.duration)}ms`);
                    }
                }
            });
            observer.observe({ entryTypes: ['longtask'] });
        } catch (e) {
            console.log('Long task observer not supported');
        }
    }
};

// Initialize performance monitoring
PerformanceMonitor.init();

// Note: Global error handlers removed to prevent interference with UI interactions
// Errors are logged to console for debugging

// Export für andere Module
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { Utils, APIClient, PerformanceMonitor };
}
