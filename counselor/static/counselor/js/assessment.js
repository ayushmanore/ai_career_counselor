
class AssessmentInterface {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 4;
        this.formData = {};
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.initializeValidation();
        this.setupProgressTracking();
    }
    
    bindEvents() {
        // Form submission
        document.getElementById('assessmentForm')?.addEventListener('submit', (e) => {
            this.handleFormSubmission(e);
        });
        
        // Input validation
        document.querySelectorAll('input[type="number"]').forEach(input => {
            input.addEventListener('input', (e) => {
                this.validateNumericInput(e.target);
            });
        });
        
        // Real-time suggestions
        document.querySelectorAll('input[name^="score_"]').forEach(input => {
            input.addEventListener('change', () => {
                this.updateLiveRecommendations();
            });
        });
    }
    
    validateNumericInput(input) {
        const value = parseInt(input.value);
        const min = parseInt(input.min);
        const max = parseInt(input.max);
        
        if (value < min || value > max) {
            input.classList.add('is-invalid');
            this.showValidationError(input, `Value must be between ${min} and ${max}`);
        } else {
            input.classList.remove('is-invalid');
            this.hideValidationError(input);
        }
    }
    
    showValidationError(input, message) {
        let feedback = input.nextElementSibling;
        if (!feedback || !feedback.classList.contains('invalid-feedback')) {
            feedback = document.createElement('div');
            feedback.className = 'invalid-feedback';
            input.parentNode.insertBefore(feedback, input.nextSibling);
        }
        feedback.textContent = message;
    }
    
    hideValidationError(input) {
        const feedback = input.nextElementSibling;
        if (feedback && feedback.classList.contains('invalid-feedback')) {
            feedback.remove();
        }
    }
    
    handleFormSubmission(e) {
        const form = e.target;
        const submitBtn = form.querySelector('button[type="submit"]');
        
        // Show loading state
        this.showLoadingState(submitBtn);
        
        // Validate form
        if (!this.validateForm(form)) {
            e.preventDefault();
            this.hideLoadingState(submitBtn);
            return false;
        }
        
        // Show AI processing animation
        this.showAIProcessing();
    }
    
    showLoadingState(button) {
        const originalText = button.innerHTML;
        button.setAttribute('data-original-text', originalText);
        button.innerHTML = '<span class="loading-spinner me-2"></span>Analyzing with AI...';
        button.disabled = true;
    }
    
    hideLoadingState(button) {
        const originalText = button.getAttribute('data-original-text');
        button.innerHTML = originalText;
        button.disabled = false;
    }
    
    showAIProcessing() {
        // Create AI processing overlay
        const overlay = document.createElement('div');
        overlay.className = 'ai-processing-overlay';
        overlay.innerHTML = `
            <div class="ai-processing-content">
                <div class="ai-brain-animation">
                    <i class="fas fa-brain fa-3x text-primary mb-3"></i>
                </div>
                <h4>AI Analysis in Progress</h4>
                <p class="text-muted">Processing your academic profile...</p>
                <div class="progress mb-3" style="height: 8px;">
                    <div class="progress-bar progress-bar-striped progress-bar-animated" 
                         style="width: 100%"></div>
                </div>
                <small class="text-muted">Using Forward Chaining & FOPL Rules</small>
            </div>
        `;
        
        // Add overlay styles
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        `;
        
        const content = overlay.querySelector('.ai-processing-content');
        content.style.cssText = `
            background: white;
            padding: 40px;
            border-radius: 15px;
            text-align: center;
            max-width: 400px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        `;
        
        document.body.appendChild(overlay);
        
        // Add brain pulsing animation
        const brain = overlay.querySelector('.ai-brain-animation i');
        brain.style.animation = 'pulse 1.5s infinite';
    }
    
    validateForm(form) {
        let isValid = true;
        const requiredFields = form.querySelectorAll('[required]');
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                field.classList.add('is-invalid');
                this.showValidationError(field, 'This field is required');
                isValid = false;
            }
        });
        
        return isValid;
    }
    
    updateLiveRecommendations() {
        // Collect current form data
        const formData = new FormData(document.getElementById('assessmentForm'));
        const subjectScores = {};
        
        for (let [key, value] of formData.entries()) {
            if (key.startsWith('score_') && value) {
                subjectScores[key.replace('score_', '')] = parseInt(value);
            }
        }
        
        // Show preview if enough data
        if (Object.keys(subjectScores).length >= 3) {
            this.showLivePreview(subjectScores);
        }
    }
    
    showLivePreview(subjectScores) {
        // Simple preview logic (not full AI)
        const topSubjects = Object.entries(subjectScores)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 3);
        
        let previewHTML = `
            <div class="alert alert-info mt-3">
                <h6><i class="fas fa-eye me-2"></i>Live Preview</h6>
                <p class="mb-1">Based on your top subjects:</p>
                <small>
        `;
        
        topSubjects.forEach(([subject, score]) => {
            previewHTML += `<span class="badge bg-primary me-1">${subject.replace('_', ' ')} (${score})</span>`;
        });
        
        previewHTML += `
                </small>
                <p class="mb-0 mt-2">
                    <small class="text-muted">Complete the full assessment for detailed AI recommendations!</small>
                </p>
            </div>
        `;
        
        // Remove existing preview
        const existingPreview = document.querySelector('.live-preview');
        if (existingPreview) {
            existingPreview.remove();
        }
        
        // Add new preview
        const form = document.getElementById('assessmentForm');
        const preview = document.createElement('div');
        preview.className = 'live-preview';
        preview.innerHTML = previewHTML;
        form.appendChild(preview);
    }
    
    setupProgressTracking() {
        // Track form completion progress
        const formInputs = document.querySelectorAll('#assessmentForm input, #assessmentForm select');
        let completedFields = 0;
        
        formInputs.forEach(input => {
            input.addEventListener('input', () => {
                completedFields = Array.from(formInputs).filter(inp => inp.value).length;
                const progress = (completedFields / formInputs.length) * 100;
                this.updateProgressIndicator(progress);
            });
        });
    }
    
    updateProgressIndicator(progress) {
        let indicator = document.querySelector('.progress-indicator');
        
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.className = 'progress-indicator fixed-bottom bg-white border-top p-2';
            indicator.innerHTML = `
                <div class="container">
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">Assessment Progress</small>
                        <small class="text-primary progress-text">0%</small>
                    </div>
                    <div class="progress mt-1" style="height: 4px;">
                        <div class="progress-bar" style="width: 0%"></div>
                    </div>
                </div>
            `;
            document.body.appendChild(indicator);
        }
        
        const progressBar = indicator.querySelector('.progress-bar');
        const progressText = indicator.querySelector('.progress-text');
        
        progressBar.style.width = progress + '%';
        progressText.textContent = Math.round(progress) + '%';
        
        if (progress >= 80) {
            indicator.classList.add('bg-success', 'text-white');
            progressText.textContent = 'Ready to Submit!';
        }
    }
}

// Results page functionality - COMPLETE VERSION
class ResultsInterface {
    constructor() {
        this.init();
    }
    
    init() {
        this.animateResults();
        this.setupInteractiveElements();
        this.addExplanationFeatures();
    }
    
    animateResults() {
        // Animate recommendation cards
        const cards = document.querySelectorAll('.recommendation-card');
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('fade-in-up');
            }, index * 200);
        });
        
        // Animate progress bars
        setTimeout(() => {
            const progressBars = document.querySelectorAll('.progress-bar');
            progressBars.forEach(bar => {
                const width = bar.style.width;
                bar.style.width = '0%';
                setTimeout(() => {
                    bar.style.transition = 'width 1.5s ease-in-out';
                    bar.style.width = width;
                }, 100);
            });
        }, 500);
    }
    
    setupInteractiveElements() {
        // Add click handlers for detailed explanations
        document.querySelectorAll('.recommendation-card').forEach(card => {
            card.addEventListener('click', (e) => {
                if (!e.target.closest('.btn')) {
                    this.showDetailedExplanation(card);
                }
            });
        });
        
        // Setup share functionality
        const shareBtn = document.querySelector('[onclick="shareResults()"]');
        if (shareBtn && navigator.share) {
            shareBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.shareResults();
            });
        }
    }
    
    showDetailedExplanation(card) {
        const reasoning = card.querySelector('.card-text').textContent;
        const careerName = card.querySelector('.card-title').textContent;
        
        // Create modal for detailed explanation
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="fas fa-lightbulb me-2"></i>Why ${careerName}?
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <h6>AI Reasoning Process:</h6>
                        <p>${reasoning}</p>
                        
                        <h6>Knowledge Base Rules Applied:</h6>
                        <ul class="list-unstyled">
                            <li><i class="fas fa-check text-success me-2"></i>Subject performance analysis</li>
                            <li><i class="fas fa-check text-success me-2"></i>Personality trait matching</li>
                            <li><i class="fas fa-check text-success me-2"></i>Career interest alignment</li>
                            <li><i class="fas fa-check text-success me-2"></i>Forward chaining inference</li>
                        </ul>
                        
                        <div class="alert alert-info">
                            <strong>Note:</strong> This recommendation is based on First-Order Predicate Logic 
                            rules and your provided assessment data. Consider it as one factor in your 
                            career decision-making process.
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
        
        // Clean up when modal is hidden
        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
    }
    
    addExplanationFeatures() {
        // Add tooltips to technical terms
        const techTerms = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        techTerms.forEach(term => {
            new bootstrap.Tooltip(term);
        });
    }
    
    shareResults() {
        if (navigator.share) {
            navigator.share({
                title: 'My AI Career Assessment Results',
                text: 'Check out my personalized career recommendations!',
                url: window.location.href
            }).catch(err => console.log('Error sharing:', err));
        } else {
            // Fallback: copy to clipboard
            navigator.clipboard.writeText(window.location.href).then(() => {
                this.showNotification('Link copied to clipboard!', 'success');
            });
        }
    }
    
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 1060; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-hide after 3 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 3000);
    }
}

// Initialize based on current page
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('assessmentForm')) {
        new AssessmentInterface();
    } else if (document.querySelector('.recommendation-card')) {
        new ResultsInterface();
    }
    
    // Initialize Bootstrap components
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});