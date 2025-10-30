/**
 * Loading Spinner Helper - AI Soccer Project
 *
 * Provides utility functions to show/hide loading spinners
 * and manage loading states across the application.
 *
 * Usage:
 *   Loading.show('spinner-id', { text: 'Carregando...', subtitle: 'Aguarde' })
 *   Loading.hide('spinner-id')
 *   Loading.showPage('Processando dados...')
 *   Loading.hidePage()
 *   Loading.button(buttonElement, true)
 */

const Loading = {
  /**
   * Default configuration
   */
  config: {
    defaultId: 'page-loading',
    defaultText: 'Carregando...',
    defaultSubtitle: 'Por favor, aguarde',
    fadeSpeed: 200,
  },

  /**
   * Show loading spinner
   * @param {string} loadingId - ID of the loading element
   * @param {object} options - Configuration options
   */
  show(loadingId, options = {}) {
    const element = document.getElementById(loadingId);
    if (!element) {
      console.warn(`Loading element with id '${loadingId}' not found`);
      return;
    }

    // Update text if provided
    if (options.text) {
      const textElement = element.querySelector('p.text-lg');
      if (textElement) {
        textElement.textContent = options.text;
      }
    }

    // Update subtitle if provided
    if (options.subtitle) {
      const subtitleElement = element.querySelector('p.text-sm');
      if (subtitleElement) {
        subtitleElement.textContent = options.subtitle;
      }
    }

    // Show element with fade in
    element.classList.remove('hidden');
    element.style.opacity = '0';

    requestAnimationFrame(() => {
      element.style.transition = `opacity ${this.config.fadeSpeed}ms ease-in-out`;
      element.style.opacity = '1';
    });

    // Prevent scrolling when overlay is shown
    if (element.classList.contains('fixed')) {
      document.body.style.overflow = 'hidden';
    }
  },

  /**
   * Hide loading spinner
   * @param {string} loadingId - ID of the loading element
   * @param {function} callback - Optional callback after hide
   */
  hide(loadingId, callback) {
    const element = document.getElementById(loadingId);
    if (!element) {
      console.warn(`Loading element with id '${loadingId}' not found`);
      return;
    }

    // Fade out
    element.style.opacity = '0';

    setTimeout(() => {
      element.classList.add('hidden');
      element.style.opacity = '';
      element.style.transition = '';

      // Re-enable scrolling
      if (element.classList.contains('fixed')) {
        document.body.style.overflow = '';
      }

      if (callback && typeof callback === 'function') {
        callback();
      }
    }, this.config.fadeSpeed);
  },

  /**
   * Show page-level loading overlay
   * @param {string} text - Loading text
   * @param {string} subtitle - Loading subtitle
   */
  showPage(text, subtitle) {
    this.show(this.config.defaultId, {
      text: text || this.config.defaultText,
      subtitle: subtitle || this.config.defaultSubtitle,
    });
  },

  /**
   * Hide page-level loading overlay
   * @param {function} callback - Optional callback after hide
   */
  hidePage(callback) {
    this.hide(this.config.defaultId, callback);
  },

  /**
   * Toggle loading state on a button
   * @param {HTMLElement} button - Button element
   * @param {boolean} loading - Loading state
   * @param {string} loadingText - Text to show when loading
   */
  button(button, loading, loadingText = 'Carregando...') {
    if (!button) {
      console.warn('Button element not provided');
      return;
    }

    if (loading) {
      // Store original content
      button.dataset.originalContent = button.innerHTML;
      button.disabled = true;
      button.classList.add('opacity-60', 'cursor-not-allowed');

      // Create spinner HTML
      const spinnerHTML = `
        <span class="inline-flex items-center space-x-2">
          <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>${loadingText}</span>
        </span>
      `;

      button.innerHTML = spinnerHTML;
    } else {
      // Restore original content
      if (button.dataset.originalContent) {
        button.innerHTML = button.dataset.originalContent;
        delete button.dataset.originalContent;
      }

      button.disabled = false;
      button.classList.remove('opacity-60', 'cursor-not-allowed');
    }
  },

  /**
   * Show loading on form submit
   * @param {HTMLFormElement} form - Form element
   * @param {object} options - Configuration options
   */
  form(form, options = {}) {
    if (!form) {
      console.warn('Form element not provided');
      return;
    }

    const submitButton = form.querySelector('[type="submit"]');

    form.addEventListener('submit', (e) => {
      // Show button loading
      if (submitButton) {
        this.button(submitButton, true, options.buttonText || 'Enviando...');
      }

      // Show page loading if configured
      if (options.showPageLoading !== false) {
        this.showPage(
          options.text || 'Processando formulário...',
          options.subtitle || 'Por favor, aguarde'
        );
      }

      // If preventDefault is needed (for AJAX), caller should handle it
    });
  },

  /**
   * Show loading for AJAX requests
   * @param {string} loadingId - Loading element ID
   * @param {Promise} promise - Promise to wait for
   * @param {object} options - Configuration options
   */
  async wrap(loadingId, promise, options = {}) {
    try {
      this.show(loadingId, options);
      const result = await promise;
      this.hide(loadingId);
      return result;
    } catch (error) {
      this.hide(loadingId);
      throw error;
    }
  },

  /**
   * Create a card loading skeleton
   * @param {HTMLElement} container - Container element
   * @param {number} count - Number of skeleton items
   */
  skeleton(container, count = 3) {
    if (!container) {
      console.warn('Container element not provided');
      return;
    }

    const skeletonHTML = `
      <div class="animate-pulse space-y-4">
        ${Array(count).fill().map(() => `
          <div class="bg-slate-800 border border-slate-700 rounded-xl p-6">
            <div class="flex items-center space-x-4 mb-4">
              <div class="h-12 w-12 bg-slate-700 rounded-full"></div>
              <div class="flex-1 space-y-2">
                <div class="h-4 bg-slate-700 rounded w-3/4"></div>
                <div class="h-3 bg-slate-700 rounded w-1/2"></div>
              </div>
            </div>
            <div class="space-y-2">
              <div class="h-3 bg-slate-700 rounded"></div>
              <div class="h-3 bg-slate-700 rounded w-5/6"></div>
            </div>
          </div>
        `).join('')}
      </div>
    `;

    container.innerHTML = skeletonHTML;
  },

  /**
   * Initialize loading for all forms with data-loading attribute
   */
  init() {
    // Auto-handle forms with data-loading
    document.querySelectorAll('form[data-loading]').forEach(form => {
      const options = {
        text: form.dataset.loadingText,
        subtitle: form.dataset.loadingSubtitle,
        buttonText: form.dataset.loadingButton,
        showPageLoading: form.dataset.loadingPage !== 'false',
      };

      this.form(form, options);
    });

    // Auto-handle links with data-loading
    document.querySelectorAll('a[data-loading]').forEach(link => {
      link.addEventListener('click', (e) => {
        // Don't show loading for # links or javascript: links
        if (link.getAttribute('href') === '#' ||
            link.getAttribute('href')?.startsWith('javascript:')) {
          return;
        }

        this.showPage(
          link.dataset.loadingText || 'Carregando página...',
          link.dataset.loadingSubtitle
        );
      });
    });

    console.log('Loading helper initialized');
  },
};

// Auto-initialize on DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => Loading.init());
} else {
  Loading.init();
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Loading;
}
