/**
 * ============================================
 * FADE-IN ON SCROLL (IntersectionObserver + safe fallback)
 * ============================================
 *
 * Replaces the scroll-only approach with IntersectionObserver where supported.
 * IntersectionObserver reliably notifies when elements enter/leave the viewport,
 * so "fast scroll" cases (short intersections) are detected correctly.
 *
 * Fallback: For older browsers without IntersectionObserver, a throttled
 * scroll-based approach is included (improved from the prior version).
 *
 * NOTES:
 * - Elements to animate: .fade-in-section
 * - Visible class added: .is-visible (CSS should contain transitions)
 * - Tweak rootMargin or threshold below to change when animations trigger.
 *
 * Author: Arash Mirshahi (keeps attribution)
 * Updated: 2025-12-17 (IntersectionObserver fallback + robustness)
 * ============================================
 */

/* ------------------------------
   Configuration: tweak these
   ------------------------------ */
const OBSERVER_ROOT = null;                            // viewport
const OBSERVER_ROOT_MARGIN = '0px 0px -50px 0px';       // trigger slightly before element fully visible
const OBSERVER_THRESHOLD = 0.05;                       // fraction of element visible to consider it "in view" (Work on 4K screens too)

/* Fallback scroll throttle timing (ms) — only used by the scroll fallback */
const SCROLL_THROTTLE_MS = 100;

/* ------------------------------
   Utility: detect reduced motion preference
   ------------------------------ */
const prefersReducedMotion = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (prefersReducedMotion) {
    // If user prefers reduced motion, we will still add the is-visible class
    // immediately (CSS should handle skipping transitions). This avoids waiting.
    console.log('ℹ️ User prefers reduced motion — fade-in elements will be revealed without animation.');
}

/* ------------------------------
   CSS expectation (for reference)
   ------------------------------
   Make sure your CSS includes something like:

   .fade-in-section { opacity: 0; transform: translateY(8px); transition: opacity .45s ease, transform .45s ease; }
   .fade-in-section.is-visible { opacity: 1; transform: none; }
*/

/* ------------------------------
   Main logic
   ------------------------------ */

/**
 * Mark an element visible and perform cleanup (remove observer/unobserve).
 * Ensures we don't re-check elements unnecessarily.
 */
function revealElement(el, observerInstance) {
    el.classList.add('is-visible');

    // If using an IntersectionObserver, unobserve this element
    if (observerInstance && typeof observerInstance.unobserve === 'function') {
        observerInstance.unobserve(el);
    }
}

/* ================================
   IntersectionObserver Implementation
   ================================ */
function initWithIntersectionObserver() {

    // Create the observer with configured options
    const options = {
        root: OBSERVER_ROOT,
        rootMargin: OBSERVER_ROOT_MARGIN,
        threshold: OBSERVER_THRESHOLD
    };

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            // entry.isIntersecting is true when the intersection conditions are met
            if (entry.isIntersecting) {
                revealElement(entry.target, obs);
            }
        });
    }, options);

    // Observe current fade-in elements
    const els = Array.from(document.querySelectorAll('.fade-in-section:not(.is-visible)'));
    els.forEach(el => {
        // If user prefers reduced motion, reveal immediately (no animation)
        if (prefersReducedMotion) {
            revealElement(el, null);
        } else {
            observer.observe(el);
        }
    });

    // Edge-case safety: if new fade-in elements are added dynamically later,
    // you may want to call observeNewFadeElements() (helper below) to attach them.
    // Return the observer so tests / cleanup can use it.
    return observer;
}

/**
 * Helper for dynamically added elements: observe any new .fade-in-section elements
 * that are not yet visible.
 */
function observeNewFadeElements(observerInstance) {
    if (!observerInstance) return;
    const newEls = Array.from(document.querySelectorAll('.fade-in-section:not(.is-visible)'));
    newEls.forEach(el => observerInstance.observe(el));
}

/* ================================
   Scroll-based Fallback (for old browsers)
   ================================ */

/**
 * This fallback mirrors the robust version we discussed previously:
 * - Maintains a dynamic list of pending elements (not yet .is-visible)
 * - Performs checks on throttled scroll + on resize/load/image-load
 * - Slightly relaxed trigger so elements show a bit earlier
 *
 * It's kept as a fallback so the website still works on older user agents.
 */
function initWithScrollFallback() {

    let pending = [];           // elements still waiting to be revealed
    let windowHeight = window.innerHeight;
    let scheduled = false;

    function refreshPending() {
        pending = Array.from(document.querySelectorAll('.fade-in-section:not(.is-visible)'));
    }

    function isInView(el) {
        const rect = el.getBoundingClientRect();
        // Trigger when element's top reaches 85% of viewport height (similar to observer rootMargin)
        const triggerMultiplier = 0.85;
        return (rect.top <= windowHeight * triggerMultiplier && rect.bottom >= 0);
    }

    function checkAndReveal() {
        if (pending.length === 0) return;

        for (let i = pending.length - 1; i >= 0; i--) {
            const el = pending[i];
            if (el.classList.contains('is-visible')) {
                pending.splice(i, 1);
                continue;
            }
            if (isInView(el)) {
                revealElement(el, null);
                pending.splice(i, 1);
            }
        }
    }

    function onScrollThrottled() {
        if (scheduled) return;
        scheduled = true;
        requestAnimationFrame(() => {
            refreshPending();   // rebuild pending list (keeps it fresh)
            checkAndReveal();
            setTimeout(() => scheduled = false, SCROLL_THROTTLE_MS);
        });
    }

    // Init
    refreshPending();
    if (prefersReducedMotion) {
        // Reveal everything immediately if reduced-motion is set
        pending.forEach(el => revealElement(el, null));
        pending = [];
        return null;
    }

    // Initial check (in case some are already visible)
    checkAndReveal();

    // Add listeners if there are still pending items
    if (pending.length > 0) {
        window.addEventListener('scroll', onScrollThrottled, { passive: true });
        window.addEventListener('resize', function () {
            windowHeight = window.innerHeight;
            refreshPending();
            checkAndReveal();
        });

        // Recheck after a short timeout (to catch late layout shifts)
        setTimeout(() => {
            windowHeight = window.innerHeight;
            refreshPending();
            checkAndReveal();
        }, 140);

        // Recheck on window load (images/fonts finished)
        window.addEventListener('load', function () {
            windowHeight = window.innerHeight;
            refreshPending();
            checkAndReveal();
        });

        // Recheck after images load (useful for layout shifts)
        const imgs = Array.from(document.images || []);
        imgs.forEach(img => {
            if (!img.complete) {
                img.addEventListener('load', function () {
                    windowHeight = window.innerHeight;
                    refreshPending();
                    checkAndReveal();
                }, { once: true });
            }
        });
    }

    // Return a small API object so tests / future cleanup may remove listeners if desired.
    return {
        stop: function () {
            window.removeEventListener('scroll', onScrollThrottled);
        }
    };
}

/* ================================
   Bootstrap on DOM ready
   ================================ */
document.addEventListener('DOMContentLoaded', function () {
    // If user prefers reduced motion, reveal all items immediately and skip observers
    if (prefersReducedMotion) {
        const all = Array.from(document.querySelectorAll('.fade-in-section:not(.is-visible)'));
        all.forEach(el => revealElement(el, null));
        return;
    }

    // Use IntersectionObserver when available (modern, precise)
    if ('IntersectionObserver' in window) {
        console.log('⚡ Using IntersectionObserver for fade-in animations');
        const observer = initWithIntersectionObserver();

        // Optional: if your app injects content dynamically (AJAX, frameworks),
        // you can call observeNewFadeElements(observer) to attach them later.

    } else {
        // Fallback path for older browsers
        console.log('⚠️ IntersectionObserver not available — using scroll fallback');
        initWithScrollFallback();
    }
});