// static/portfolio/js/script.js - Corrected Version

document.addEventListener('DOMContentLoaded', function () {

    // 1. Initialize AOS library for scroll animations
    AOS.init({
        duration: 800,
        once: false, // Set to true to animate only once
        offset: 50,
        delay: 100,
    });

    // --- 2. Theme Toggler ---
    const themeToggleButton = document.getElementById('theme-toggle');
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    // Read initial theme preference
    // Default to 'light' if nothing is saved and system preference isn't dark
    const getInitialTheme = () => {
        const storedTheme = localStorage.getItem('theme');
        if (storedTheme) {
            return storedTheme;
        }
        return prefersDarkScheme.matches ? 'dark' : 'light';
    };

    let currentTheme = getInitialTheme();

    // Function to apply theme
    function applyTheme(theme) {
        if (theme === 'dark') {
            document.body.classList.add('dark-theme');
            document.body.classList.remove('light-theme');
            if (themeToggleButton) {
                themeToggleButton.innerHTML = '<i class="fas fa-sun"></i>'; // Sun icon
                themeToggleButton.setAttribute('aria-label', 'Switch to light theme');
            }
        } else {
            document.body.classList.add('light-theme');
            document.body.classList.remove('dark-theme');
            if (themeToggleButton) {
                themeToggleButton.innerHTML = '<i class="fas fa-moon"></i>'; // Moon icon
                themeToggleButton.setAttribute('aria-label', 'Switch to dark theme');
            }
        }
        // No need to save to localStorage here, it's saved on button click or initial load persistence
    }

    // Apply the initial theme
    applyTheme(currentTheme);
    // Save the initial theme determination to localStorage if not already set
    if (!localStorage.getItem('theme')) {
        localStorage.setItem('theme', currentTheme);
    }


    // Add event listener to the theme toggle button
    if (themeToggleButton) {
        themeToggleButton.addEventListener('click', function () {
            // Determine the new theme based on the current class
            currentTheme = document.body.classList.contains('dark-theme') ? 'light' : 'dark';
            applyTheme(currentTheme);
            localStorage.setItem('theme', currentTheme); // Save the user's explicit choice
        });
    }

    // Optional: Listen for changes in system color scheme preference
    // This version respects manual toggle: only updates if no theme was MANUALLY set via button click.
    prefersDarkScheme.addEventListener('change', (e) => {
         const storedTheme = localStorage.getItem('theme');
         // Check if theme was set by explicit user action. If yes, don't override with system change.
         // This simple check assumes if 'theme' exists in storage, it was an explicit choice (either initial load based on storage/pref, or button click)
         // To truly only react if user *never* clicked the button is more complex.
         // For now, we won't automatically change if localStorage is set.
         if (!storedTheme) { // Only react if the theme hasn't been explicitly set/saved yet
             const systemTheme = e.matches ? 'dark' : 'light';
             applyTheme(systemTheme);
             // Optionally save this system-driven change: localStorage.setItem('theme', systemTheme);
         }
    });
    // --- End Theme Toggler ---


    // --- 3. Typing Effect for Hero Subtitle ---
    const heroSubtitleElement = document.getElementById('hero-subtitle');
    let typeTimer; // Variable to hold the setTimeout timer ID

    function typeWriter(el, wordsArray) {
        if (!el || !wordsArray || wordsArray.length === 0) {
            console.warn("Typewriter: Target element or words array missing.");
            return; // Exit if element or words are missing
        }

        let currentWordIndex = 0;
        let isDeleting = false;
        let currentText = '';
        let typingSpeed = 120;
        let deletingSpeed = 60;
        let delayBetweenWords = 1500;

        function type() {
            const currentWord = wordsArray[currentWordIndex].trim(); // Trim whitespace
            let typeDelay = typingSpeed;

            if (isDeleting) {
                // Deleting text
                currentText = currentWord.substring(0, currentText.length - 1);
                typeDelay = deletingSpeed;
            } else {
                // Typing text
                currentText = currentWord.substring(0, currentText.length + 1);
            }

            el.textContent = currentText;

            if (!isDeleting && currentText === currentWord) {
                // Word fully typed, pause before deleting
                typeDelay = delayBetweenWords;
                isDeleting = true;
            } else if (isDeleting && currentText === '') {
                // Word fully deleted, move to next word
                isDeleting = false;
                currentWordIndex = (currentWordIndex + 1) % wordsArray.length; // Loop
                typeDelay = typingSpeed / 2; // Short pause before typing next
            }

            // Clear previous timer before setting a new one
            clearTimeout(typeTimer);
            typeTimer = setTimeout(type, typeDelay);
        }
        type(); // Start the typing process
    }

    // Get text for typewriter from data attributes (set in HTML/Django view)
    if (heroSubtitleElement) {
        const lang = document.documentElement.lang || 'en'; // Get current language
        const textAttr = lang === 'ar' ? 'data-text-ar' : 'data-text-en';
        const textToType = heroSubtitleElement.getAttribute(textAttr);

        if (textToType) {
            const words = textToType.split('|').map(s => s.trim()).filter(s => s); // Split by '|', trim, remove empty
             if (words.length > 0) {
                 // Clear initial content before starting type animation
                 heroSubtitleElement.textContent = "";
                 typeWriter(heroSubtitleElement, words);
             } else {
                 console.warn(`Typewriter: No words found in ${textAttr} attribute.`);
             }
        } else {
            console.warn(`Typewriter: Attribute ${textAttr} not found on #hero-subtitle.`);
            // Optionally keep the static text if attribute is missing
            // heroSubtitleElement.textContent = "Default Static Text";
        }
    }
    // --- End Typing Effect ---


    // --- 4. GSAP Animations (Optional) ---
    // Ensure GSAP is loaded (check might be needed if conditionally loaded)
    if (typeof gsap !== 'undefined') {
        // Animate Hero section elements
        gsap.from("#home .display-3", { opacity: 0, y: 50, duration: 0.8, delay: 0.4, ease: "power2.out" });
        gsap.from("#home #hero-subtitle", { opacity: 0, y: 50, duration: 0.8, delay: 0.6, ease: "power2.out" });
        // Ensure the paragraph selector is reliable (using ID or class if possible)
        gsap.from("#home .fs-5", { opacity: 0, y: 50, duration: 0.8, delay: 0.8, ease: "power2.out" }); // Example selector, adjust if needed
        gsap.from("#home .btn", { opacity: 0, y: 50, duration: 0.8, delay: 1.0, stagger: 0.2, ease: "power2.out" });
        gsap.from("#home img.rounded-circle", { opacity: 0, scale: 0.8, duration: 1, delay: 1.2, ease: "elastic.out(1, 0.5)" });

        // Example: ScrollTrigger for skills (Uncomment and include ScrollTrigger plugin if needed)
        /*
        if (gsap.ScrollTrigger) {
            gsap.utils.toArray('#skills .skill-item').forEach((item, index) => {
                gsap.from(item, {
                    opacity: 0,
                    y: 40,
                    duration: 0.6,
                    ease: "power1.out",
                    scrollTrigger: {
                        trigger: item,
                        start: "top 90%",
                        // toggleActions: "play none none reset", // Example: Reset animation if scrolled past
                        // markers: true, // For debugging
                    }
                });
            });
        } else {
             console.warn("GSAP ScrollTrigger plugin not loaded.");
        }
        */
    }
    // --- End GSAP Animations ---


    // --- 5. Smooth Scrolling for Navbar Links ---
    document.querySelectorAll('nav .nav-link[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            try {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    let navbarHeight = 0;
                    const navbar = document.querySelector('.navbar.sticky-top');
                    if (navbar) {
                        navbarHeight = navbar.offsetHeight;
                    }

                    const elementPosition = targetElement.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - navbarHeight - 10; // Added small offset

                    window.scrollTo({
                        top: offsetPosition,
                        behavior: "smooth"
                    });

                    // Close mobile navbar menu after click (Bootstrap 5)
                    const navbarToggler = document.querySelector('.navbar-toggler');
                    const navbarCollapse = document.getElementById('navbarNav'); // Use ID selector
                    if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                        const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
                        if (bsCollapse) {
                           bsCollapse.hide();
                        } else {
                           // Fallback or handle case where instance not found
                           new bootstrap.Collapse(navbarCollapse, { toggle: false }).hide();
                        }
                    }
                } else {
                    console.warn(`Smooth scroll target not found for selector: ${targetId}`);
                }
            } catch (error) {
                console.error(`Error during smooth scroll for ${targetId}:`, error);
            }
        });
    });
    // --- End Smooth Scrolling ---


    // --- 6. Contact Form Submission (Formspree) ---
    const contactForm = document.getElementById('contact-form');
    const formStatus = document.getElementById('form-status');

    async function handleFormSubmit(event) {
        event.preventDefault();
        const form = event.target;
        const data = new FormData(form);

        // Clear previous status
        if (formStatus) {
             formStatus.textContent = '';
             formStatus.className = 'mb-3 text-center'; // Reset classes
        }


        try {
            const response = await fetch(form.action, {
                method: form.method,
                body: data,
                headers: {
                    'Accept': 'application/json'
                }
            });

            if (response.ok) {
                if (formStatus) {
                    formStatus.textContent = "Message sent successfully! Thank you."; // Generic English
                    formStatus.classList.add('text-success');
                }
                form.reset(); // Clear the form fields
                 // Uncheck radio buttons
                document.querySelectorAll('.rating input[type="radio"]').forEach(radio => radio.checked = false);
            } else {
                // Try to parse error from Formspree response
                response.json().then(data => {
                    const errorMsg = data.errors ? data.errors.map(err => err.message).join(', ') : "Oops! There was a problem submitting your form.";
                    if (formStatus) {
                         formStatus.textContent = errorMsg;
                         formStatus.classList.add('text-danger');
                    }
                }).catch(() => {
                     // Fallback error message if parsing fails
                     if (formStatus) {
                         formStatus.textContent = "Oops! There was a problem submitting your form.";
                         formStatus.classList.add('text-danger');
                     }
                });
            }
        } catch (error) {
            console.error("Form submission error:", error);
            if (formStatus) {
                 formStatus.textContent = "Oops! There was a problem submitting your form.";
                 formStatus.classList.add('text-danger');
            }
        }
    }

    if (contactForm) {
        // Add basic client-side validation feedback if desired (Bootstrap 5 handles some via HTML5 attributes)
        contactForm.addEventListener('submit', function(event) {
             if (!contactForm.checkValidity()) {
               event.preventDefault();
               event.stopPropagation();
               // Optional: Add status message about validation failure
               // if (formStatus) {
               //      formStatus.textContent = "Please fill out all required fields correctly.";
               //      formStatus.className = 'mb-3 text-center text-danger';
               // }
             } else {
                // Only call handleFormSubmit if basic HTML5 validation passes
                handleFormSubmit(event);
             }
             contactForm.classList.add('was-validated'); // Trigger Bootstrap validation styles
           }, false); // Use false for event capturing phase is default

    } else {
        console.warn("Contact form with id 'contact-form' not found.");
    }
    // --- End Contact Form ---

}); // End DOMContentLoaded