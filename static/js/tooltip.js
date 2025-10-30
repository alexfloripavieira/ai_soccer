/**
 * Tooltip System for AI Soccer Forms
 *
 * Provides interactive tooltips that appear on hover/focus
 * with intelligent positioning and mobile support.
 */

(function() {
  'use strict';

  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTooltips);
  } else {
    initTooltips();
  }

  function initTooltips() {
    const tooltipTriggers = document.querySelectorAll('.tooltip-trigger');

    tooltipTriggers.forEach(trigger => {
      const tooltipId = trigger.getAttribute('data-tooltip-id');
      const tooltipContent = document.getElementById(tooltipId);

      if (!tooltipContent) return;

      let hideTimeout;
      let isHovered = false;

      // Show tooltip on hover (desktop)
      trigger.addEventListener('mouseenter', function() {
        clearTimeout(hideTimeout);
        isHovered = true;
        showTooltip(tooltipContent, trigger);
      });

      // Hide tooltip when mouse leaves
      trigger.addEventListener('mouseleave', function() {
        isHovered = false;
        hideTimeout = setTimeout(() => {
          if (!isHovered) {
            hideTooltip(tooltipContent);
          }
        }, 200);
      });

      // Toggle tooltip on click/tap (mobile)
      trigger.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();

        // Close all other tooltips first
        document.querySelectorAll('.tooltip-content').forEach(tooltip => {
          if (tooltip !== tooltipContent && !tooltip.classList.contains('hidden')) {
            hideTooltip(tooltip);
          }
        });

        // Toggle current tooltip
        if (tooltipContent.classList.contains('hidden')) {
          showTooltip(tooltipContent, trigger);
        } else {
          hideTooltip(tooltipContent);
        }
      });

      // Show tooltip on focus (accessibility)
      trigger.addEventListener('focus', function() {
        clearTimeout(hideTimeout);
        showTooltip(tooltipContent, trigger);
      });

      // Hide tooltip on blur
      trigger.addEventListener('blur', function() {
        hideTimeout = setTimeout(() => {
          hideTooltip(tooltipContent);
        }, 200);
      });

      // Keep tooltip visible when hovering over it
      tooltipContent.addEventListener('mouseenter', function() {
        clearTimeout(hideTimeout);
        isHovered = true;
      });

      tooltipContent.addEventListener('mouseleave', function() {
        isHovered = false;
        hideTimeout = setTimeout(() => {
          hideTooltip(tooltipContent);
        }, 200);
      });
    });

    // Close all tooltips when clicking outside
    document.addEventListener('click', function(e) {
      if (!e.target.closest('.tooltip-wrapper')) {
        document.querySelectorAll('.tooltip-content').forEach(tooltip => {
          hideTooltip(tooltip);
        });
      }
    });

    // Close tooltips on ESC key
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        document.querySelectorAll('.tooltip-content').forEach(tooltip => {
          hideTooltip(tooltip);
        });
      }
    });
  }

  function showTooltip(tooltipContent, trigger) {
    tooltipContent.classList.remove('hidden');

    // Adjust position if tooltip goes off screen
    adjustTooltipPosition(tooltipContent, trigger);
  }

  function hideTooltip(tooltipContent) {
    tooltipContent.classList.add('hidden');
  }

  function adjustTooltipPosition(tooltipContent, trigger) {
    // Get viewport and tooltip dimensions
    const rect = tooltipContent.getBoundingClientRect();
    const triggerRect = trigger.getBoundingClientRect();
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;

    // Check if tooltip goes off the left edge
    if (rect.left < 10) {
      tooltipContent.style.left = '10px';
      tooltipContent.style.transform = 'translateX(0)';
    }
    // Check if tooltip goes off the right edge
    else if (rect.right > viewportWidth - 10) {
      tooltipContent.style.left = 'auto';
      tooltipContent.style.right = '10px';
      tooltipContent.style.transform = 'translateX(0)';
    }
    // Default centered position
    else {
      tooltipContent.style.left = '50%';
      tooltipContent.style.right = 'auto';
      tooltipContent.style.transform = 'translateX(-50%)';
    }

    // Check if tooltip goes off the top edge (show below instead)
    if (rect.top < 10 && triggerRect.bottom + rect.height + 20 < viewportHeight) {
      tooltipContent.style.bottom = 'auto';
      tooltipContent.style.top = 'calc(100% + 8px)';

      // Flip arrow to point up
      const arrow = tooltipContent.querySelector('div > div');
      if (arrow) {
        arrow.style.top = 'auto';
        arrow.style.bottom = '100%';
        arrow.style.borderTop = 'none';
        arrow.style.borderBottom = '8px solid rgb(30, 41, 59)'; // slate-800
        arrow.style.marginBottom = '-1px';
        arrow.style.marginTop = '0';
      }
    } else {
      // Default position (above)
      tooltipContent.style.top = 'auto';
      tooltipContent.style.bottom = 'calc(100% + 8px)';

      // Reset arrow to point down
      const arrow = tooltipContent.querySelector('div > div');
      if (arrow) {
        arrow.style.bottom = 'auto';
        arrow.style.top = '100%';
        arrow.style.borderBottom = 'none';
        arrow.style.borderTop = '8px solid rgb(30, 41, 59)'; // slate-800
        arrow.style.marginTop = '-1px';
        arrow.style.marginBottom = '0';
      }
    }
  }

  // Re-adjust tooltip positions on window resize
  let resizeTimeout;
  window.addEventListener('resize', function() {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
      document.querySelectorAll('.tooltip-content:not(.hidden)').forEach(tooltip => {
        const trigger = document.querySelector(`[data-tooltip-id="${tooltip.id}"]`);
        if (trigger) {
          adjustTooltipPosition(tooltip, trigger);
        }
      });
    }, 100);
  });

})();
