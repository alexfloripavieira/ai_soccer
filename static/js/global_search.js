/**
 * Global Search with Dynamic AJAX
 * Provides real-time search suggestions and results
 */

// Debounce function to limit API calls
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Initialize search functionality
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.querySelector('input[name="q"]');
  const searchForm = document.querySelector('form[action*="search"]');
  const resultsContainer = document.getElementById('search-results');
  const loadingIndicator = document.getElementById('search-loading');

  if (!searchInput) return;

  // Auto-focus search input when pressing '/' key
  document.addEventListener('keydown', function(e) {
    if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
      e.preventDefault();
      searchInput.focus();
    }

    // Clear search with ESC key
    if (e.key === 'Escape' && document.activeElement === searchInput) {
      searchInput.value = '';
      searchInput.blur();
    }
  });

  // Debounced search function
  const performSearch = debounce(async function(query) {
    if (!query || query.length < 2) {
      return;
    }

    // Show loading indicator
    if (loadingIndicator) {
      loadingIndicator.classList.remove('hidden');
    }

    try {
      const response = await fetch(`/search/?q=${encodeURIComponent(query)}`, {
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
        }
      });

      if (!response.ok) {
        throw new Error('Search request failed');
      }

      // For AJAX requests, we could return JSON, but for now we'll just submit the form
      // This is a placeholder for future AJAX implementation

    } catch (error) {
      console.error('Search error:', error);
    } finally {
      // Hide loading indicator
      if (loadingIndicator) {
        loadingIndicator.classList.add('hidden');
      }
    }
  }, 300);

  // Listen to input changes
  searchInput.addEventListener('input', function(e) {
    const query = e.target.value.trim();

    if (query.length >= 2) {
      performSearch(query);
    }
  });

  // Handle form submission
  if (searchForm) {
    searchForm.addEventListener('submit', function(e) {
      const query = searchInput.value.trim();

      if (!query) {
        e.preventDefault();
        searchInput.focus();
      }
    });
  }

  // Add search animation
  searchInput.addEventListener('focus', function() {
    this.parentElement.classList.add('ring-2', 'ring-green-500');
  });

  searchInput.addEventListener('blur', function() {
    this.parentElement.classList.remove('ring-2', 'ring-green-500');
  });
});

// Highlight search terms in results
function highlightSearchTerms(text, query) {
  if (!query || !text) return text;

  const regex = new RegExp(`(${query})`, 'gi');
  return text.replace(regex, '<mark class="bg-yellow-300/30 text-yellow-200 px-1 rounded">$1</mark>');
}

// Export for use in other scripts if needed
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { debounce, highlightSearchTerms };
}
