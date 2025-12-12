/**
 * FADE-IN ON SCROLL ANIMATION
 * 
 * PURPOSE: 
 * Makes sections fade in smoothly as the user scrolls down the page. 
 * This creates a modern, interactive feel without being distracting.
 * 
 * HOW IT WORKS:
 * 1. We mark sections with the class 'fade-in-section'
 * 2. By default, these sections are invisible (opacity: 0)
 * 3. When they enter the viewport, we add the 'is-visible' class
 * 4. CSS handles the actual fade-in transition
 * 
 * BROWSER SUPPORT:
 * Uses IntersectionObserver (supported in all modern browsers)
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Select all elements that should fade in
    const fadeElements = document.querySelectorAll('. fade-in-section');
    
    // Configuration for when to trigger the animation
    const options = {
        root: null,              // Use the viewport as the container
        threshold: 0.15,         // Trigger when 15% of the element is visible
        rootMargin: '0px 0px -100px 0px'  // Start animation 100px before element enters viewport
    };
    
    // Callback function that runs when an element enters/leaves viewport
    const fadeInOnScroll = (entries, observer) => {
        entries. forEach(entry => {
            if (entry.isIntersecting) {
                // Element is in viewport – add the visible class
                entry.target.classList.add('is-visible');
                
                // Optional: Stop observing this element (animation only happens once)
                // Remove the line below if you want elements to fade out when scrolling back up
                observer.unobserve(entry. target);
            }
        });
    };
    
    // Create the observer
    const observer = new IntersectionObserver(fadeInOnScroll, options);
    
    // Start observing all fade elements
    fadeElements.forEach(element => {
        observer.observe(element);
    });
});