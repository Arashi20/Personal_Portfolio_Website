/**
 * ============================================
 * FADE-IN ON SCROLL ANIMATION (Simplified)
 * ============================================
 * 
 * PURPOSE: 
 * Makes sections fade in smoothly as the user scrolls down the page. 
 * 
 * HOW IT WORKS:
 * 1. Elements with 'fade-in-section' class start invisible (CSS:  opacity: 0)
 * 2. On page load, we check which elements are in viewport → show them
 * 3. On every scroll, we check again → show newly visible elements
 * 4. Once an element is shown, we stop checking it (performance)
 * 
 * WHY THIS VERSION: 
 * - No IntersectionObserver complexity
 * - Direct scroll event listener (more reliable)
 * - Immediate feedback (no delay)
 * - Works on ALL browsers (even old ones)
 * 
 * AUTHOR: Arash Mirshahi
 * DATE: 2025-12-12
 * ============================================
 */

// ============================================
// GLOBAL VARIABLES
// ============================================

let fadeElements = [];  // Will store all elements to animate
let windowHeight = 0;   // Viewport height (calculated on load)

// ============================================
// HELPER FUNCTION: Check if element is in viewport
// ============================================

/**
 * Checks if an element is currently visible in the viewport.
 * 
 * @param {HTMLElement} element - The element to check
 * @returns {boolean} - True if element is in viewport, false otherwise
 */
function isElementInViewport(element) {
    const rect = element.getBoundingClientRect();
    
    /**
     * Element is considered "in viewport" if: 
     * - Its top edge is less than 80% down the screen (starts animating before fully visible)
     * - Its bottom edge is above the top of the screen (not scrolled past)
     * 
     * The 0.8 multiplier means:  trigger when element is 80% of the way down the screen. 
     * Adjust this value to change when animations start: 
     * - 1.0 = element must be fully in viewport
     * - 0.8 = element starts animating when 20% from bottom (recommended)
     * - 0.5 = element starts animating halfway down screen (very early)
     */
    return (
        rect.top <= windowHeight * 0.8 &&  // Top of element is within trigger zone
        rect.bottom >= 0                   // Bottom of element hasn't scrolled past top
    );
}

// ============================================
// MAIN FUNCTION: Show visible elements
// ============================================

/**
 * Loops through all fade-in elements and shows the ones in viewport.
 * This function is called: 
 * - Once when page loads
 * - Every time user scrolls
 */
function showVisibleElements() {
    
    // DEBUG: Log that function is running
    console.log('🔍 Checking for visible elements...');
    
    /**
     * Loop through fadeElements array BACKWARDS. 
     * Why backwards? So we can safely remove elements from the array
     * while looping (removing from end doesn't affect earlier indexes).
     */
    for (let i = fadeElements.length - 1; i >= 0; i--) {
        const element = fadeElements[i];
        
        // Check if this element is now in the viewport
        if (isElementInViewport(element)) {
            
            // DEBUG: Log which element is being shown
            console. log('✨ Showing:', element.tagName, element.className);
            
            // Add the 'is-visible' class → triggers CSS transition
            element.classList.add('is-visible');
            
            /**
             * Remove this element from the array. 
             * Once an element is visible, we don't need to check it anymore.
             * This improves performance (fewer elements to check on each scroll).
             */
            fadeElements.splice(i, 1);
        }
    }
    
    // DEBUG: Log how many elements are still waiting to be shown
    console.log(`📊 ${fadeElements.length} elements still waiting to fade in`);
    
    /**
     * PERFORMANCE OPTIMIZATION: 
     * If all elements have been shown, remove the scroll listener.
     * No point listening to scroll events if there's nothing left to animate.
     */
    if (fadeElements.length === 0) {
        console.log('✅ All elements visible - removing scroll listener');
        window.removeEventListener('scroll', handleScroll);
    }
}

// ============================================
// SCROLL HANDLER (with throttling)
// ============================================

/**
 * Variables for throttling scroll events. 
 * Without throttling, showVisibleElements() would run 100+ times per second
 * while scrolling (huge performance hit).
 */
let isScrolling = false;  // Flag to track if we're currently processing a scroll

/**
 * Throttled scroll handler. 
 * This ensures showVisibleElements() only runs once every 100ms,
 * even if the user scrolls continuously.
 */
function handleScroll() {
    
    // If we're already processing a scroll event, ignore this one
    if (isScrolling) return;
    
    // Set the flag to prevent multiple simultaneous calls
    isScrolling = true;
    
    /**
     * Use requestAnimationFrame for smooth performance.
     * This tells the browser to run our function at the optimal time
     * (synced with screen refresh rate, usually 60fps).
     */
    requestAnimationFrame(() => {
        showVisibleElements();
        
        /**
         * After 100ms, reset the flag so the next scroll can be processed.
         * This throttles the function to run at most 10 times per second.
         */
        setTimeout(() => {
            isScrolling = false;
        }, 100);
    });
}

// ============================================
// INITIALIZATION
// ============================================

/**
 * Wait for DOM to fully load before running our code.
 * This ensures all HTML elements exist before we try to select them.
 */
document. addEventListener('DOMContentLoaded', function() {
    
    // DEBUG:  Confirm script has loaded
    console.log('🎬 Fade-in animation script loaded');
    
    // ========================================
    // 1. SELECT ALL ELEMENTS TO ANIMATE
    // ========================================
    
    /**
     * Find all elements with the 'fade-in-section' class.
     * Convert NodeList to Array so we can use array methods (like splice).
     */
    fadeElements = Array.from(document. querySelectorAll('.fade-in-section'));
    
    // DEBUG: Log how many elements were found
    console.log(`🎯 Found ${fadeElements. length} elements to animate`);
    
    // If no elements found, show warning and exit
    if (fadeElements.length === 0) {
        console.warn('⚠️ No elements with class "fade-in-section" found.');
        return;
    }
    
    // ========================================
    // 2. GET VIEWPORT HEIGHT
    // ========================================
    
    /**
     * Store the viewport height for calculations.
     * We do this once instead of recalculating on every scroll (performance).
     */
    windowHeight = window.innerHeight;
    console.log(`📏 Viewport height: ${windowHeight}px`);
    
    // ========================================
    // 3. CHECK INITIAL VISIBILITY
    // ========================================
    
    /**
     * Check which elements are already visible when page loads.
     * This handles the case where user refreshes in the middle of the page.
     */
    console.log('🔎 Checking initial visibility...');
    showVisibleElements();
    
    // ========================================
    // 4. ADD SCROLL LISTENER
    // ========================================
    
    /**
     * Listen for scroll events (only if there are still elements to show).
     * We use our throttled handler to avoid performance issues.
     */
    if (fadeElements.length > 0) {
        console.log('👂 Adding scroll listener');
        window.addEventListener('scroll', handleScroll, { passive: true });
        
        /**
         * The { passive: true } option tells the browser: 
         * "This scroll handler won't call preventDefault(), so you can
         * optimize scrolling performance."
         */
    }
    
    // ========================================
    // 5. HANDLE WINDOW RESIZE
    // ========================================
    
    /**
     * If user resizes the window, update the stored viewport height.
     * This ensures calculations stay accurate on mobile (orientation change)
     * or desktop (window resize).
     */
    window.addEventListener('resize', function() {
        windowHeight = window.innerHeight;
        console.log(`📐 Viewport resized to:  ${windowHeight}px`);
        
        // Recheck visibility after resize (elements might now be in view)
        showVisibleElements();
    });
    
    console.log('✅ Animation system initialized');
});


// ============================================
// ACCESSIBILITY:  Respect reduced motion preference
// ============================================

/**
 * Check if user has "reduce motion" enabled in their OS settings.
 * If so, log a message (the CSS already handles skipping animations).
 */
if (window.matchMedia('(prefers-reduced-motion:  reduce)').matches) {
    console.log('ℹ️ User prefers reduced motion - animations will be instant (handled by CSS)');
}